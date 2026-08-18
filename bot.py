import os
import urllib.request
import json
import telebot
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

# --- CONFIGURACIÓN ---
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- IA GOOGLE GEMINI ---
def consultar_ia_gratis(prompt_usuario):
    if not GEMINI_API_KEY:
        return "Falta agregar la variable GEMINI_API_KEY en Railway."
    
    try:
        # Usamos el modelo actualizado v1beta gemini-2.5-flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = json.dumps({
            "contents": [{
                "parts": [{"text": f"Eres Sofía, una asistente virtual amigable. Responde brevemente: {prompt_usuario}"}]
            }]
        }).encode("utf-8")

        req = urllib.request.Request(
            url, 
            data=payload, 
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        print(f"Error Gemini: {e}")
        return f"Error al consultar la IA: {str(e)[:40]}"

# --- HERRAMIENTAS DE ARCHIVOS ---
def set_cell_background(cell, fill_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def generar_word_crucigrama(nombre_archivo):
    doc = Document()
    doc.add_heading('CRUCIGRAMA: ANIMALES', level=0)
    grid = [["1", "L", "E", "O", "N"], ["#", "#", "2", "#", "#"]]
    table = doc.add_table(rows=len(grid), cols=len(grid[0]))
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            cell = table.cell(r, c)
            if grid[r][c] == "#": set_cell_background(cell, "000000")
            else: cell.text = grid[r][c]
    doc.save(nombre_archivo)

def generar_excel(nombre_archivo):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Area", "Estado"])
    ws.append(["Educación Física", "Activo"])
    wb.save(nombre_archivo)

# --- COMANDOS ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Sofía. Puedo crear crucigramas, tablas o responderte.")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_text = message.text.lower()
    
    if "crucigrama" in user_text:
        archivo = "crucigrama.docx"
        generar_word_crucigrama(archivo)
        with open(archivo, "rb") as f:
            bot.send_document(message.chat.id, f)
        return
        
    if "excel" in user_text:
        archivo = "tabla.xlsx"
        generar_excel(archivo)
        with open(archivo, "rb") as f:
            bot.send_document(message.chat.id, f)
        return

    bot.send_chat_action(message.chat.id, 'typing')
    respuesta = consultar_ia_gratis(message.text)
    bot.reply_to(message, respuesta)

if __name__ == "__main__":
    bot.infinity_polling()
    
