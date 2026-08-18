import os
import urllib.request
import urllib.parse
import telebot
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import openpyxl

# --- TU TOKEN SEGURO Y SIEMPRE VISIBLE ---
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- FUNCIÓN IA LIBRE (SIN CLAVES NI REGISTROS) ---
def consultar_ia_gratis(prompt_usuario):
    """Consulta directa a IA pública sin ninguna clave."""
    try:
        # Añadimos un pequeño formato para que la IA sepa quién es
        prompt_final = f"Eres Sofía, una asistente virtual amigable y experta. Responde brevemente en español: {prompt_usuario}"
        texto_codificado = urllib.parse.quote(prompt_final)
        
        # Usamos el servicio libre de Pollinations
        url = f"https://text.pollinations.ai/{texto_codificado}?model=openai"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            respuesta = response.read().decode('utf-8')
            return respuesta.strip()
    except Exception as e:
        print(f"Error IA: {e}")
        return None

# --- HERRAMIENTAS DE ARCHIVOS (Word, Excel, PDF) ---
def set_cell_background(cell, fill_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def generar_word_crucigrama(nombre_archivo, tema):
    doc = Document()
    h = doc.add_heading(f'CRUCIGRAMA: {tema.upper()}', level=0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph("Instrucciones: Completa las casillas.")
    doc.add_paragraph()
    # (Se mantiene tu lógica de crucigrama intacta)
    pistas_h = ["1. Felino rey de la selva. (LEON)"]
    pistas_v = ["2. Fiel amigo. (PERRO)"]
    grid = [["1", "L", "E", "O", "N"], ["#", "#", "2", "#", "#"]]
    
    table = doc.add_table(rows=len(grid), cols=len(grid[0]))
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            cell = table.cell(r, c)
            if grid[r][c] == "#": set_cell_background(cell, "000000")
            else: cell.text = grid[r][c]
    doc.save(nombre_archivo)

def generar_pdf_requisitos_completos(nombre_archivo):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    c.drawString(100, 750, "Manual de Requisitos Sofía")
    c.save()

def generar_excel(nombre_archivo, datos):
    wb = openpyxl.Workbook()
    ws = wb.active
    for fila in datos: ws.append(fila)
    wb.save(nombre_archivo)

# --- COMANDOS ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Sofía. Estoy lista para ayudarte. Pregúntame cualquier cosa o pídeme archivos.")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_text = message.text.lower()
    
    # 1. ARCHIVOS
    if "crucigrama" in user_text:
        generar_word_crucigrama("crucigrama.docx", "animales")
        with open("crucigrama.docx", "rb") as f: bot.send_document(message.chat.id, f)
        return

    # 2. IA LIBRE
    bot.send_chat_action(message.chat.id, 'typing')
    respuesta = consultar_ia_gratis(message.text)
    
    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "¡Recibí tu mensaje! Estoy un poco ocupada procesándolo. Intenta preguntarme de nuevo.")

bot.infinity_polling()
