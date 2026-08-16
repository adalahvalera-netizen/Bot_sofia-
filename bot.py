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

# Memoria temporal para el modo tutor paso a paso (como arreglar una PC, etc.)
user_states = {}

# --- FUNCIONES DE ARCHIVOS (Tus herramientas avanzadas) ---

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


# --- MANEJADOR DE CONVERSACIÓN Y PERSONALIDAD ESTILO GEMINI ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"¡Hola, {message.from_user.first_name}! 👋 Soy **Sofía**, tu asistente virtual. Estoy aquí para conversar contigo de forma natural, ayudarte con tus dudas paso a paso, explicarte temas complejos o crearte archivos (Word, Excel, PDF, imágenes). ¿De qué te gustaría hablar o qué tarea resolvemos hoy?")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_id = message.chat.id
    user_text = message.text.lower()

    try:
        # 1. MODO TUTOR PASO A PASO (Ej: Reparar computadora o guías complejas)
        if "arreglar" in user_text and ("computadora" in user_text or "pc" in user_text or "laptop" in user_text):
            user_states[user_id] = {"paso": 1, "tema": "reparacion_pc"}
            bot.reply_to(message, "¡Claro que sí! Con gusto te acompaño paso a paso para revisar tu computadora. Para empezar, cuéntame: ¿Qué problema presenta exactamente? (Por ejemplo: ¿No enciende, la pantalla se pone negra, está muy lenta o hace algún ruido extraño?)")
            return

        # Continuación del flujo paso a paso si el usuario está en medio de una tutoría
        if user_id in user_states and user_states[user_id]["tema"] == "reparacion_pc":
            paso = user_states[user_id]["paso"]
            if paso == 1:
            # Puedes usar tu consulta o continuar la guía
                bot.reply_to(message, "Comprendo el síntoma. Antes de pasar a revisar hardware interno, ¿has verificado que los cables de corriente estén firmemente conectados y que la regleta o tomacorriente funcione con otro aparato?")
                user_states[user_id]["paso"] = 2
            elif paso == 2:
                bot.reply_to(message, "Perfecto. Si ya descartamos la energía básica, el siguiente paso es un reinicio forzado o revisar si los ventiladores giran al presionar el botón de encendido. Dime qué notas al intentar encenderla ahora.")
                user_states[user_id]["paso"] = 3
            else:
                bot.reply_to(message, "¡Muy bien! Vamos avanzando con calma. Si prefieres que hagamos otra cosa o consultemos un documento, solo dímelo.")
                user_states.pop(user_id, None) # Limpiamos estado
            return

        # 2. CONVERSACIÓN NATURAL (Saludos y charlas amigables)
        if any(saludo in user_text for saludo in ["hola", "buenos días", "buenas tardes", "qué tal", "cómo estás"]):
            bot.reply_to(message, "¡Hola! Estoy excelente, procesando información y lista para ayudarte en lo que necesites. ¿Y tú qué tal? ¿Cómo va tu día?")
            return

        # 3. HERRAMIENTAS Y COMANDOS (Integrados con naturalidad)
        if "crucigrama" in user_text and "word" in user_text:
            tema = user_text.replace("crucigrama", "").replace("word", "").replace("crear", "").strip()
            if not tema: tema = "General"
            bot.reply_to(message, f"🧩 ¡Me parece una gran idea! Estoy redactando un crucigrama de '{tema}' con sus pistas y soluciones en un documento de Word para ti. Dame un segundito...")
            
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
                bot.send_document(message.chat.id, archivo, caption="📄 ¡Listo! Aquí tienes tu archivo de Word con el crucigrama preparado.")
            os.remove(nombre_doc)
            return

        elif "requisitos" in user_text or "ficha tecnica" in user_text:
            bot.reply_to(message, "📋 Claro que sí, preparé un archivo PDF con la guía de requisitos técnicos y deportivos detallada. Aquí te lo comparto:")
            nombre_pdf = "requisitos_sofia.pdf"
            generar_pdf_requisitos_completos(nombre_pdf)
            with open(nombre_pdf, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="✨ Tu manual técnico y deportivo en PDF.")
            os.remove(nombre_pdf)
            return

        elif "excel" in user_text or "tabla" in user_text:
            bot.reply_to(message, "📊 ¡Claro! Voy a armarte esa tabla en Excel de inmediato.")
            nombre_excel = "tabla_notas.xlsx"
            datos = [["Materia / Área", "Estado", "Observaciones"], ["Educación Física", "Aprobado", "Excelente desempeño"], ["Tecnología / IA", "En marcha", "Creando funciones avanzadas"]]
            generar_excel(nombre_excel, datos)
            with open(nombre_excel, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📊 Aquí tienes tu archivo de Excel listo.")
            os.remove(nombre_excel)
            return

        elif "imagen de" in user_text or "crea una imagen" in user_text:
            prompt = user_text.replace("imagen de", "").replace("crea una imagen de", "").strip()
            if not prompt:
                bot.reply_to(message, "Claro, dime qué te gustaría que dibuje. Por ejemplo: *imagen de un paisaje futurista*.")
                return
            bot.reply_to(message, f"🎨 ¡Manos a la obra! Estoy generando tu imagen de '{prompt}'...")
            try:
                image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
                bot.send_photo(message.chat.id, image_url, caption=f"✨ Aquí tienes el resultado para: {prompt}")
            except:
                bot.reply_to(message, "Vaya, tuve un pequeño inconveniente técnico generando la imagen, pero podemos intentarlo de nuevo.")
            return

        # 4. RESPUESTA INTELIGENTE ABIERTA (Respaldo web si pregunta cualquier cosa)
        else:
            api_url = f"https://api.duckduckgo.com/?q={requests.utils.quote(message.text)}&format=json"
            res = requests.get(api_url).json()
            abstract = res.get("AbstractText")
            
            if abstract:
                bot.reply_to(message, f"Estuve investigando sobre eso y te cuento: {abstract}")
            else:
                bot.reply_to(message, f"Es un tema muy interesante lo que mencionas sobre '{message.text}'. Cuéntame más detalles o dime si prefieres que redactemos un documento, armemos un Excel, un crucigrama o busquemos más datos al respecto.")

    except Exception as e:
        bot.reply_to(message, "¡Vaya! Ocurrió un pequeño detalle técnico, pero mis sistemas siguen activos. ¿Qué hacemos ahora?")

bot.infinity_polling()
               
            
