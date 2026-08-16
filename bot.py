import os
import random
import requests
import telebot
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document
import openpyxl

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Función para crear PDF
def generar_pdf(nombre_archivo, titulo, contenido):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    c.drawString(100, 750, f"--- {titulo} ---")
    y = 700
    for linea in contenido:
        c.drawString(100, y, linea)
        y -= 25
        if y < 50:
            c.showPage()
            y = 750
    c.save()

# Función para crear Word (.docx)
def generar_word(nombre_archivo, titulo, parrafos):
    doc = Document()
    doc.add_heading(titulo, 0)
    for p in parrafos:
        doc.add_paragraph(p)
    doc.save(nombre_archivo)

# Función para crear Excel (.xlsx)
def generar_excel(nombre_archivo, datos):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos Escolares"
    for fila in datos:
        ws.append(fila)
    wb.save(nombre_archivo)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, f"¡Hola {message.from_user.first_name}! 📚📊 Soy Sofía, tu asistente para tareas, PDFs, Word, Excel e imágenes con IA.\n\n"
                          "**Prueba escribir:**\n"
                          "• **'word tarea'** - Te genero y envío un documento de Word.\n"
                          "• **'excel notas'** - Te genero y envío una tabla de Excel.\n"
                          "• **'pdf resumen'** - Te genero un PDF de estudio.\n"
                          "• **'imagen de [lo que sea]'** - Creo una imagen con IA.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_msg = message.text.lower()
        
        # 1. Crear y enviar Word (.docx)
        if "word" in user_msg:
            nombre_doc = "tarea_escolar.docx"
            titulo = "Trabajo Académico - Sofía IA"
            parrafos = [
                "Este es un documento redactado automáticamente para tu tarea.",
                "Materia: Apoyo Estudiantil y Educación Física.",
                "Instrucciones: Puedes editar este archivo en Microsoft Word o Google Docs para entregar tu trabajo final."
            ]
            generar_word(nombre_doc, titulo, parrafos)
            
            with open(nombre_doc, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📝 ¡Aquí tienes tu archivo de Word listo para descargar!")
            os.remove(nombre_doc)
            return

        # 2. Crear y enviar Excel (.xlsx)
        elif "excel" in user_msg or "tabla" in user_msg:
            nombre_excel = "tabla_datos.xlsx"
            datos = [
                ["Materia", "Calificación / Estado", "Profesor"],
                ["Educación Física", "Aprobado (Excelente)", "Entrenador"],
                ["Matemáticas", "En proceso", "Prof. de Álgebra"],
                ["Historia", "Completado", "Prof. de Sociales"]
            ]
            generar_excel(nombre_excel, datos)
            
            with open(nombre_excel, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📊 ¡Aquí tienes tu archivo de Excel con la tabla de datos!")
            os.remove(nombre_excel)
            return

        # 3. Crear Imágenes con IA
        elif "imagen de" in user_msg or "crea una imagen" in user_msg:
            prompt = user_msg.replace("imagen de", "").replace("crea una imagen de", "").strip()
            if not prompt:
                bot.reply_to(message, "Escribe qué imagen deseas. Ejemplo: *imagen de un león en la selva*")
                return
            bot.reply_to(message, f"🎨 Creando la imagen de '{prompt}'...")
            try:
                image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
                bot.send_photo(message.chat.id, image_url, caption=f"✨ Imagen generada: {prompt}")
            except:
                bot.reply_to(message, "No se pudo generar la imagen en este momento.")
            return

        # 4. Generador de PDF
        elif "pdf" in user_msg:
            nombre_pdf = "guia_estudio.pdf"
            titulo_pdf = "GUIA DE REPASO ESCOLAR"
            lineas = [
                "1. Utiliza la tecnica Pomodoro para estudiar con descanso.",
                "2. Mantén actividad física diaria para un mejor rendimiento mental.",
                "3. Repasa con mapas conceptuales y tablas organizadas."
            ]
            generar_pdf(nombre_pdf, titulo_pdf, lineas)
            with open(nombre_pdf, "rb") as archivo:
                bot.send_document(message.chat.id, archivo, caption="📄 ¡Aquí tienes tu guía en PDF!")
            os.remove(nombre_pdf)
            return

        # 5. Ayuda y listado
        elif any(word in user_msg for word in ["que puedes hacer", "ayuda", "comandos"]):
            reply = (
                "🤖 **¡Estas son mis funciones completas!**\n\n"
                "• **Word:** Escribe 'word' para que te cree y mande un documento .docx.\n"
                "• **Excel:** Escribe 'excel' para que te mande una tabla de datos .xlsx.\n"
                "• **PDFs:** Escribe 'pdf' para guías escolares.\n"
                "• **IA:** Escribe 'imagen de [texto]' para crear arte digital.\n"
                "• **Estudios y Deportes:** Explicaciones de materias y rutinas."
            )
        else:
            reply = f"Entendido sobre '{user_msg}'. Prueba pidiéndome un **'word'**, un **'excel'**, un **'pdf'** o una **'imagen de...'**."

        bot.reply_to(message, reply, parse_mode="Markdown")
            
    except Exception as e:
        bot.reply_to(message, "¡Mensaje recibido! Todo operando con normalidad.")

bot.infinity_polling()
