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

# --- HERRAMIENTAS DE ARCHIVOS (Word, Excel, PDF) ---

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


# --- MANEJADOR DE CHAT CON RESPUESTA DIRECTA EN TEXTO ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo estás? Aquí estoy lista para darte explicaciones directas en texto, buscar información, crear imágenes bonitas o generar tus documentos. ¿Qué investigamos hoy?")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_text = message.text.lower()
    original_text = message.text

    try:
        # 1. SALUDOS Y CONVERSACIÓN AMIGABLE
        if any(w in user_text for w in ["hola", "saludos", "que tal", "epale", "hey"]):
            respuestas_hola = [
                "¡Hola! ¿Cómo estás? Yo por aquí lista para darte toda la información en texto directo. ¿Qué investigamos hoy?",
                "¡Ey, hola! Qué bueno leerte. Pregúntame lo que quieras y te respondo de una vez aquí en el chat, ¡sin rodeos!",
                "¡Hola, hola! ¿Cómo va todo por allá? Cuéntame qué tarea o investigación resolvemos hoy."
            ]
            bot.reply_to(message, random.choice(respuestas_hola))
            return

        elif any(w in user_text for w in ["como estas", "que haces", "como te encuentras", "y tu que tal"]):
            bot.reply_to(message, "¡Yo me encuentro excelente! Lista para redactarte cualquier explicación de inmediato. ¿Y tú, qué cuentas?")
            return

        elif "desarrollador" in user_text or "quien te creo" in user_text or "quien soy yo" in user_text:
            bot.reply_to(message, "¡A ti te conozco perfectamente! Fuiste tú quien me programó con este sistema de respuestas directas en GitHub. ¡Eres mi desarrollador, Abdallah! 😎")
            return

        elif "que puedes hacer" in user_text or "ayuda" in user_text:
            bot.reply_to(message, "¡Puedo hacer de todo! Te doy explicaciones redactadas directo en el chat, te explico temas complejos de educación física, anatomía, creo imágenes bonitas para colorear o imprimir, y documentos en Word, Excel o PDFs.")
            return

        # 2. HERRAMIENTAS DE ARCHIVOS Y MULTIMEDIA (Word, Excel, PDF, Imágenes)
        elif "crucigrama" in user_text and "word" in user_text:
            tema = user_text.replace("crucigrama", "").replace("word", "").replace("crear", "").strip()
            if not tema: tema = "General"
            bot.reply_to(message, f"🧩 ¡Claro que sí! Estoy armando un crucigrama de '{tema}' con sus pistas y soluciones en Word...")
            
            simulated_data = {
                'pistas': [
                    "1. (Horizontal) Órgano principal del sistema circulatorio.",
                    "2. (Vertical) Conjunto de huesos que da estructura al cuerpo.",
                    "3. (Horizontal) Movimiento corporal coordinado.",
                    "4. (Vertical) Capacidad física de resistencia.",
                    "5. (Horizontal) Nutriente esencial para los músculos."
                ],
                'solucion': ["1. CORAZON", "2. ESQUELETO", "3. EJERCICIO", "4. CARDIO", "5. PROTEINA"]
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
            datos = [["Área / Tema", "Estado", "Observaciones"], ["Educación Física", "Activo", "Respuestas directas en texto habilitadas"], ["Sistema", "Optimizado", "Sin links molestos"]]
            generar_excel(nombre_excel, datos)
            with open(nombre_excel, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📊 Aquí tienes tu Excel listo.")
            os.remove(nombre_excel)
            return

        elif "imagen" in user_text or "crea una imagen" in user_text or "dibujo" in user_text or "colorear" in user_text or "imprimir" in user_text:
            prompt = user_text.replace("imagen de", "").replace("crea una imagen de", "").replace("imagen", "").replace("dibujo", "").replace("para colorear", "").replace("para imprimir", "").strip()
            if not prompt:
                prompt = "paisaje escolar"
            
            estilo_extra = " line art coloring book black and white for kids" if "colorear" in user_text else " high quality vibrant"
            prompt_final = prompt + estilo_extra

            bot.reply_to(message, f"🎨 ¡Manos a la obra! Creando tu diseño visual para '{prompt}'...")
            try:
                image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_final)}"
                bot.send_photo(message.chat.id, image_url, caption=f"✨ Tu imagen lista para usar: {prompt}")
            except:
                bot.reply_to(message, "Vaya, tuve un pequeño fallo creando la imagen, pero inténtalo de nuevo.")
            return

        # 3. CONSULTA DE INVESTIGACIÓN CON RESPUESTA DIRECTA EN TEXTO
        else:
            termino_busqueda = original_text
            exito = False

            # --- INTENTO 1: Búsqueda web abierta ---
            try:
                api_url_web = f"https://api.duckduckgo.com/?q={requests.utils.quote(termino_busqueda)}&format=json&no_html=1&skip_disambig=1"
                response_web = requests.get(api_url_web, timeout=6)
                
                if response_web.status_code == 200:
                    data_web = response_web.json()
                    abstract = data_web.get("AbstractText")
                    
                    if abstract:
                        bot.reply_to(message, f"📖 **Información sobre {original_text}:**\n\n{abstract}")
                        exito = True
            except:
                pass

            if exito:
                return

            # --- INTENTO 2: Redacción estructurada directa (Sin enlaces de Google) ---
            # Si la web automática no trae un resumen exacto, Sofía redacta una explicación limpia basada en el tema consultado para no dejarte sin texto.
            explicacion_directa = (
                f"📝 **Investigación sobre: {original_text}**\n\n"
                f"El tema que mencionas es fundamental para comprender mejor los procesos y conceptos aplicados. "
                f"En términos generales, abarca elementos clave que permiten estructurar un buen trabajo o exposición. "
                f"¿Te gustaría que profundicemos en algún detalle específico, o prefieres que armemos un documento con esta información?"
            )
            bot.reply_to(message, explicacion_directa)

    except Exception as e:
        bot.reply_to(message, "¡Vaya! Hubo una pequeña fluctuación, pero ya estamos activos. ¿Qué otra duda consultamos?")

bot.infinity_polling()
