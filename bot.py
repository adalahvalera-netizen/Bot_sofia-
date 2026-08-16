import os
import random
import requests
import telebot
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from docx import Document
import openpyxl

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- HERRAMIENTAS DE ARCHIVOS (Word, Excel, PDF, Imágenes) ---

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

def generar_word_crucigrama(nombre_archivo, titulo, crucigrama_data):
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_heading('Pistas:', level=1)
    for pista in crucigrama_data.get('pistas', []):
        doc.add_paragraph(pista, style='ListBullet')
    doc.add_page_break()
    doc.add_heading('Solución:', level=1)
    for sol in crucigrama_data.get('solucion', []):
        doc.add_paragraph(sol)
    doc.save(nombre_archivo)

def generar_excel(nombre_archivo, datos):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos Escolares"
    for fila in datos:
        ws.append(fila)
    wb.save(nombre_archivo)


# --- MANEJADOR DE CHAT Y CONVERSACIÓN NATURAL ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo estás? Aquí estoy lista para charlar, explicarte cualquier tema, hacerte resúmenes o crearte documentos e imágenes. ¿Qué hacemos hoy?")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_text = message.text.lower()
    original_text = message.text

    try:
        # 1. SALUDOS Y CONVERSACIÓN AMIGABLE
        if any(w in user_text for w in ["hola", "saludos", "que tal", "epale", "hey"]):
            respuestas_hola = [
                "¡Hola! ¿Cómo estás? Yo por aquí todo bien, lista para ayudarte. ¿Y tú qué tal, cómo va tu día?",
                "¡Ey, hola! Qué bueno leerte. ¿De qué te gustaría hablar hoy o qué tarea resolvemos?",
                "¡Hola, hola! ¿Cómo va todo por allá? Cuéntame qué planes tienes o en qué te echo una mano."
            ]
            bot.reply_to(message, random.choice(respuestas_hola))
            return

        elif any(w in user_text for w in ["como estas", "que haces", "como te encuentras", "y tu que tal"]):
            bot.reply_to(message, "¡Yo me encuentro excelente, gracias por preguntar! Aquí activa y procesando información para lo que necesites. ¿Y tú, qué cuentas de nuevo?")
            return

        elif "que puedes hacer" in user_text or "ayuda" in user_text:
            bot.reply_to(message, "¡Puedo hacer de todo! Te explico cualquier tema platicando, te hago resúmenes, y también te creo crucigramas en Word, tablas en Excel, PDFs o dibujos con IA. ¡Pídeme lo que quieras!")
            return

        # 2. HERRAMIENTAS DE ARCHIVOS (Word, Excel, PDF, Imágenes)
        elif "crucigrama" in user_text and "word" in user_text:
            tema = user_text.replace("crucigrama", "").replace("word", "").replace("crear", "").strip()
            if not tema: tema = "General"
            bot.reply_to(message, f"🧩 ¡Claro que sí! Estoy armando un crucigrama de '{tema}' con sus pistas y soluciones en Word...")
            
            simulated_data = {
                'pistas': [
                    "1. (Horizontal) El planeta rojo de nuestro sistema solar.",
                    "2. (Vertical) Satélite natural de la Tierra.",
                    "3. (Horizontal) Fuerza que nos mantiene unidos al suelo.",
                    "4. (Vertical) Nuestra estrella principal.",
                    "5. (Horizontal) Gran masa de agua salada."
                ],
                'solucion': ["1. MARTE", "2. LUNA", "3. GRAVEDAD", "4. SOL", "5. OCEANO"]
            }
            nombre_doc = "crucigrama_sofia.docx"
            generar_word_crucigrama(nombre_doc, f"Crucigrama: {tema.upper()}", simulated_data)
            
            with open(nombre_doc, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📄 ¡Listo! Aquí tienes tu archivo de Word.")
            os.remove(nombre_doc)
            return

        elif "requisitos" in user_text or "ficha tecnica" in user_text:
            bot.reply_to(message, "📋 Aquí tienes el manual completo de requisitos técnicos y deportivos en PDF:")
            nombre_pdf = "requisitos_sofia.pdf"
            generar_pdf_requisitos_completos(nombre_pdf)
            with open(nombre_pdf, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="✨ Tu manual en PDF.")
            os.remove(nombre_pdf)
            return

        elif "excel" in user_text or "tabla" in user_text:
            bot.reply_to(message, "📊 ¡Perfecto! Creando tu tabla en Excel de inmediato...")
            nombre_excel = "tabla_notas.xlsx"
            datos = [["Materia / Área", "Estado", "Observaciones"], ["Educación Física", "Aprobado", "Excelente desempeño"], ["Funciones", "Activas", "Búsquedas listas"]]
            generar_excel(nombre_excel, datos)
            with open(nombre_excel, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📊 Aquí tienes tu Excel listo.")
            os.remove(nombre_excel)
            return

        elif "imagen de" in user_text or "crea una imagen" in user_text:
            prompt = user_text.replace("imagen de", "").replace("crea una imagen de", "").strip()
            if not prompt:
                bot.reply_to(message, "Dime qué dibujo quieres que haga. Por ejemplo: *imagen de un paisaje futurista*.")
                return
            bot.reply_to(message, f"🎨 ¡Manos a la obra! Dibujando '{prompt}'...")
            try:
                image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
                bot.send_photo(message.chat.id, image_url, caption=f"✨ Resultado para: {prompt}")
            except:
                bot.reply_to(message, "Vaya, tuve un pequeño fallo creando la imagen, pero inténtalo de nuevo.")
            return

        # 3. BÚSQUEDA DIRECTA INTELIGENTE (Cualquier tema, personaje o ciencia)
        else:
            # Limpiamos palabras comunes para quedarnos con el núcleo de lo que quiere buscar
            busqueda = user_text.replace("dame un resumen de", "").replace("resumen de", "").replace("investigame", "").replace("investiga", "").replace("quien fue", "").replace("que son", "").replace("que es", "").strip()
            if not busqueda: busqueda = original_text

            api_url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(busqueda)}"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                data = response.json()
                extracto = data.get("extract")
                titulo_articulo = data.get("title", original_text)
                
                if extracto:
                    bot.reply_to(message, f"📖 Te cuento sobre **{titulo_articulo}**:\n\n{extracto}\n\n¿Te sirve este resumen o quieres que profundicemos en algo más?")
                    return

            # Si Wikipedia da error, probamos buscando el texto original tal cual lo escribió
            api_url_2 = f"https://es.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(original_text)}"
            response_2 = requests.get(api_url_2)
            if response_2.status_code == 200:
                data_2 = response_2.json()
                if data_2.get("extract"):
                    bot.reply_to(message, f"📖 Aquí tienes la información:\n\n{data_2.get('extract')}")
                    return

            bot.reply_to(message, f"¡Qué temazo ese! Aunque me costó un poquito ubicar los detalles exactos de '{original_text}', cuéntame más y lo analizamos juntos de una vez.")

    except Exception as e:
        bot.reply_to(message, "¡Vaya! Ocurrió un pequeño detalle técnico, pero aquí sigo firme contigo. ¿Qué hacemos ahora?")

bot.infinity_polling()
