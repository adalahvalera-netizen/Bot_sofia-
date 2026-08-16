import os
import random
import requests
import telebot
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import openpyxl

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- HERRAMIENTAS DE ARCHIVOS (Word, Excel, PDF) ---

def set_cell_background(cell, fill_color):
    """Aplica color de fondo a una celda de Word."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def generar_word_crucigrama(nombre_archivo, tema):
    doc = Document()
    
    h = doc.add_heading(f'CRUCIGRAMA: {tema.upper()}', level=0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph("Instrucciones: Completa las casillas correspondientes a cada pista horizontal y vertical.")
    doc.add_paragraph()

    if "animal" in tema.lower():
        pistas_h = [
            "1. Felino considerado el rey de la selva. (LEON)",
            "3. Mamífero más grande del planeta. (BALLENA)"
        ]
        pistas_v = [
            "2. Fiel amigo del hombre que ladra. (PERRO)",
            "4. Ave rápida que vuela en las alturas. (AGUILA)"
        ]
        grid = [
            ["1", "L", "E", "O", "N", "#"],
            ["#", "#", "2", "#", "#", "#"],
            ["#", "#", "P", "#", "#", "4"],
            ["3", "B", "A", "L", "L", "E", "N", "A"],
            ["#", "#", "R", "#", "#", "G"],
            ["#", "#", "R", "#", "#", "U"],
            ["#", "#", "O", "#", "#", "I"],
            ["#", "#", "#", "#", "#", "L"],
            ["#", "#", "#", "#", "#", "A"]
        ]
    else:
        pistas_h = [
            "1. Órgano principal del sistema circulatorio. (CORAZON)",
            "3. Capacidad física de resistencia. (CARDIO)"
        ]
        pistas_v = [
            "2. Conjunto de huesos del cuerpo. (ESQUELETO)",
            "4. Nutriente clave para los músculos. (PROTEINA)"
        ]
        grid = [
            ["1", "C", "O", "R", "A", "Z", "O", "N"],
            ["#", "#", "#", "#", "2", "#", "#", "#"],
            ["#", "#", "#", "#", "E", "#", "#", "#"],
            ["3", "C", "A", "R", "D", "I", "O", "#"],
            ["#", "#", "#", "#", "I", "#", "#", "#"],
            ["#", "#", "#", "#", "O", "#", "#", "#"]
        ]

    doc.add_heading('Cuadrícula del Crucigrama:', level=1)
    
    filas = len(grid)
    columnas = max(len(row) for row in grid)
    
    table = doc.add_table(rows=filas, cols=columnas)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for row_idx, row_data in enumerate(grid):
        for col_idx in range(columnas):
            cell = table.cell(row_idx, col_idx)
            cell.width = Inches(0.5)
            
            val = row_data[col_idx] if col_idx < len(row_data) else "#"
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            if val == "#":
                set_cell_background(cell, "000000")
            else:
                set_cell_background(cell, "FFFFFF")
                if val.isdigit():
                    run = p.add_run(val)
                    run.font.size = Pt(8)
                    run.font.bold = True
                else:
                    p.text = ""

    doc.add_paragraph()
    
    doc.add_heading('Pistas Horizontales:', level=2)
    for p in pistas_h:
        doc.add_paragraph(p, style='List Bullet')
        
    doc.add_heading('Pistas Verticales:', level=2)
    for p in pistas_v:
        doc.add_paragraph(p, style='List Bullet')
        
    doc.save(nombre_archivo)

def generar_pdf_requisitos_completos(nombre_archivo):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 1 * inch, "MANUAL DE REQUISITOS INTEGRALES")
    c.drawCentredString(width / 2.0, height - 1.3 * inch, "Asistente Virtual Sofía - Abdallah")
    c.line(1 * inch, height - 1.5 * inch, width - 1 * inch, height - 1.5 * inch)
    
    c.setFont("Helvetica-Bold", 14)
    y_pos = height - 1.9 * inch
    c.drawString(1 * inch, y_pos, "I. Requisitos para Educación Física y Técnica")
    
    c.setFont("Helvetica", 11)
    requisitos = [
        "• Indumentaria deportiva cómoda y calzado adecuado.",
        "• Hidratación y espacio seguro.",
        "• Entorno técnico: Python, pyTelegramBotAPI, reportlab, python-docx, openpyxl.",
        "• Alojamiento 24/7 en servidores en la nube (Railway)."
    ]
    y_pos -= 0.3 * inch
    for req in requisitos:
        c.drawString(1.2 * inch, y_pos, req)
        y_pos -= 0.25 * inch
    c.save()

def generar_excel(nombre_archivo, datos):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos Escolares"
    for fila in datos:
        ws.append(fila)
    wb.save(nombre_archivo)


# --- MANEJADOR DE CHAT ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo estás? Aquí estoy lista con crucigramas, guiones de video, imágenes y documentos. ¿Qué hacemos hoy?")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_text = message.text.lower()
    original_text = message.text

    try:
        # 1. SALUDOS Y CONVERSACIÓN
        if any(w in user_text for w in ["hola", "saludos", "que tal", "epale", "hey"]):
            bot.reply_to(message, "¡Hola! ¿Cómo estás? Lista para ayudarte con tus tareas, gráficos, imágenes o guiones de video.")
            return

        # RECONOCIMIENTO DEL CREADOR
        elif any(w in user_text for w in ["desarrollador", "quien te creo", "quién te creó", "quien soy yo", "quién soy yo", "quien me creo", "quién me creó"]):
            bot.reply_to(message, "¡A ti te conozco perfectamente! Fuiste tú quien me programó en GitHub. ¡Eres mi desarrollador, Abdallah! 😎")
            return

        # 2. NUEVO COMANDO: CREACIÓN DE GUIONES PARA VIDEOS (TIKTOK / REELS)
        elif any(w in user_text for w in ["video", "tiktok", "reel", "promocional", "redes sociales"]):
            topic = user_text
            for palabra in ["crea", "un", "de", "para", "video", "tiktok", "reel", "promocional", "redes", "sociales", "por", "favor"]:
                topic = topic.replace(palabra, "")
            topic = topic.strip().capitalize()
            if not topic: topic = "Tu Producto o Tema"

            guion = (
                f"🎬 **ESTRATEGIA Y GUION DE VIDEO: {topic.upper()}**\n\n"
                f"⏱️ **00:00 - 00:03 (El Gancho):**\n"
                f"• **Visual:** Muestra una toma dinámica o la foto principal de {topic}.\n"
                f"• **Texto en pantalla:** '¡Lo que no sabías sobre {topic}!' 🚀\n\n"
                f"⏱️ **00:03 - 00:10 (Contenido / Beneficios):**\n"
                f"• **Visual:** Cambio rápido de toma mostrando los detalles.\n"
                f"• **Voz en off:** Menciona los 2 aspectos más llamativos que resuelven una duda o necesidad.\n\n"
                f"⏱️ **00:10 - 00:15 (Llamado a la Acción):**\n"
                f"• **Visual:** Muestra tu logo o contacto.\n"
                f"• **Voz en off:** '¡Comenta o síguenos para más detalles!'\n\n"
                f"🎵 **Música sugerida:** Audio en tendencia de ritmo alegre/moderno.\n"
                f"🏷️ **Hashtags:** #{topic.replace(' ', '')} #Viral #RedesSociales #Ecuador"
            )
            bot.reply_to(message, guion)
            return

        # 3. HERRAMIENTAS DE ARCHIVOS E IMÁGENES
        elif "crucigrama" in user_text:
            clean_tema = user_text
            for palabra in ["crea", "un", "de", "en", "word", "crucigrama", "para", "por", "favor"]:
                clean_tema = clean_tema.replace(palabra, "")
            clean_tema = clean_tema.strip().capitalize()
            if not clean_tema:
                clean_tema = "General"

            bot.reply_to(message, f"🧩 Generando el crucigrama con su cuadrícula gráfica para '{clean_tema}' en Word...")
            
            nombre_doc = "crucigrama_sofia.docx"
            generar_word_crucigrama(nombre_doc, clean_tema)
            
            with open(nombre_doc, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📄 ¡Listo! Aquí tienes tu crucigrama con la cuadrícula dibujada.")
            os.remove(nombre_doc)
            return

        elif "requisitos" in user_text or "ficha tecnica" in user_text:
            bot.reply_to(message, "📋 Aquí tienes el manual en PDF:")
            nombre_pdf = "requisitos_sofia.pdf"
            generar_pdf_requisitos_completos(nombre_pdf)
            with open(nombre_pdf, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="✨ Tu manual en PDF.")
            os.remove(nombre_pdf)
            return

        elif "excel" in user_text or "tabla" in user_text:
            bot.reply_to(message, "📊 Creando tu tabla en Excel...")
            nombre_excel = "tabla_notas.xlsx"
            datos = [["Área / Tema", "Estado", "Observaciones"], ["Educación Física", "Activo", "Cuadrícula habilitada"], ["Sistema", "Optimizado", "Word con tablas dinámicas"]]
            generar_excel(nombre_excel, datos)
            with open(nombre_excel, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📊 Aquí tienes tu Excel.")
            os.remove(nombre_excel)
            return

        elif "imagen" in user_text or "dibujo" in user_text or "colorear" in user_text:
            prompt = user_text.replace("imagen de", "").replace("crea una imagen de", "").replace("imagen", "").replace("dibujo", "").replace("para colorear", "").strip()
            if not prompt: prompt = "paisaje"
            
            estilo_extra = " line art coloring book black and white for kids" if "colorear" in user_text else " high quality"
            prompt_final = prompt + estilo_extra

            bot.reply_to(message, f"🎨 Creando imagen para '{prompt}'...")
            try:
                image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_final)}"
                bot.send_photo(message.chat.id, image_url, caption=f"✨ Tu imagen: {prompt}")
            except:
                bot.reply_to(message, "Error al generar la imagen.")
            return

        # 4. RESPUESTA DIRECTA EN TEXTO
        else:
            bot.reply_to(message, f"📝 **Información sobre {original_text}:**\n\nEl tema abarca conceptos clave para tus guías o proyectos. ¿Quieres que generemos un archivo Word, Excel, PDF o un guion de video promocional sobre esto?")

    except Exception as e:
        bot.reply_to(message, "Hubo un pequeño detalle al procesar la solicitud, intenta nuevamente.")

bot.infinity_polling()
            
