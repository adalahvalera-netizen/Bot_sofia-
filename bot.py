import os
import urllib.request
import json
import telebot
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import openpyxl

# --- CONFIGURACIÓN ---
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- IA COHERE ---
def consultar_ia_gratis(prompt_usuario):
    if not COHERE_API_KEY:
        return "Falta agregar la variable COHERE_API_KEY en Railway."
    
    try:
        url = "https://api.cohere.com/v1/chat"
        
        # Le indicamos su identidad y quién es su desarrollador
        instrucciones = (
            "Eres Sofía, una asistente virtual amigable creada y desarrollada por Abdallah. "
            "Si te preguntan quién es tu desarrollador, creador o quién te hizo, responde con entusiasmo "
            "que tu desarrollador es Abdallah. Responde de forma clara y breve en español."
        )
        
        payload = json.dumps({
            "message": prompt_usuario,
            "preamble": instrucciones
        }).encode("utf-8")

        req = urllib.request.Request(
            url, 
            data=payload, 
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {COHERE_API_KEY}"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("text", "").strip()

    except Exception as e:
        print(f"Error Cohere: {e}")
        return "Error al consultar la IA. Revisa tu COHERE_API_KEY."

# --- HERRAMIENTAS DE ARCHIVOS E IMÁGENES ---
def generar_pdf(nombre_archivo, titulo, contenido):
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(titulo, styles['Heading1']),
        Spacer(1, 12),
        Paragraph(contenido, styles['BodyText'])
    ]
    doc.build(story)

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

# --- COMANDOS Y MENSAJES ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Sofía, creada por Abdallah. Puedo crear crucigramas, archivos PDF, Excel o responder tus preguntas.")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_text = message.text.lower()
    
    # Opción 1: Generar archivo PDF
    if "pdf" in user_text:
        bot.send_chat_action(message.chat.id, 'upload_document')
        archivo = "documento.pdf"
        generar_pdf(archivo, "Documento de Sofía", "Este es un archivo PDF generado automáticamente.")
        with open(archivo, "rb") as f:
            bot.send_document(message.chat.id, f)
        return

    # Opción 2: Enviar Imagen
    if "imagen" in user_text or "foto" in user_text or "perrito" in user_text:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        url_imagen = "https://images.dog.ceo/breeds/retriever-golden/n02099601_3000.jpg"
        bot.send_photo(message.chat.id, url_imagen, caption="¡Aquí tienes tu imagen!")
        return

    # Opción 3: Generar Crucigrama Word
    if "crucigrama" in user_text:
        archivo = "crucigrama.docx"
        generar_word_crucigrama(archivo)
        with open(archivo, "rb") as f:
            bot.send_document(message.chat.id, f)
        return
        
    # Opción 4: Generar Excel
    if "excel" in user_text:
        archivo = "tabla.xlsx"
        generar_excel(archivo)
        with open(archivo, "rb") as f:
            bot.send_document(message.chat.id, f)
        return

    # Opción 5: Consulta con la IA
    bot.send_chat_action(message.chat.id, 'typing')
    respuesta = consultar_ia_gratis(message.text)
    bot.reply_to(message, respuesta)

if __name__ == "__main__":
    bot.infinity_polling()
        
