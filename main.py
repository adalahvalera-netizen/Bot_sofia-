import os
import urllib.request
import urllib.parse
import json
import re
import telebot
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
import openpyxl
from gtts import gTTS
import cohere

# --- CONFIGURACIÓN ---
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "").strip()

bot = telebot.TeleBot(TELEGRAM_TOKEN)
co = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None
modo_usuario = {}

# --- IA COHERE ---
def consultar_ia_gratis(prompt_usuario):
    if not COHERE_API_KEY or not co:
        return "Falta agregar la variable COHERE_API_KEY en Railway."
    try:
        instrucciones = (
            "Eres Sofía, una asistente virtual amigable creada y desarrollada por Abdallah. "
            "Responde de forma útil, clara y natural en español."
        )
        response = co.chat(message=prompt_usuario, preamble=instrucciones)
        return response.text.strip()
    except Exception as e:
        return f"Error al consultar la IA ({str(e)})."

# --- LIMPIADOR Y GENERADORES DE ARCHIVOS ---
def limpiar_markdown_pdf(texto):
    texto = re.sub(r'#{1,6}\s*(.*)', r'<b>\1</b>', texto)
    texto = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
    return re.sub(r'---', '', texto)

def generar_pdf(nombre_archivo, titulo, contenido):
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    styles = getSampleStyleSheet()
    texto_limpio = limpiar_markdown_pdf(contenido).replace('\n', '<br/>')
    story = [Paragraph(f"<b>{titulo}</b>", styles['Heading1']), Spacer(1, 12), Paragraph(texto_limpio, styles['BodyText'])]
    doc.build(story)

def generar_word_texto(nombre_archivo, titulo, texto):
    doc = Document()
    doc.add_heading(titulo, level=1)
    for parrafo in texto.split('\n'):
        if parrafo.strip():
            doc.add_paragraph(re.sub(r'\*\*(.*?)\*\*', r'\1', re.sub(r'#{1,6}\s*', '', parrafo)).strip())
    doc.save(nombre_archivo)

def generar_excel(nombre_archivo):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Area", "Estado", "Creado Por"])
    ws.append(["Educación Física", "Activo", "Abdallah"])
    wb.save(nombre_archivo)

# --- DESCARGAR MÚSICA VÍA PIPED API (EVITA BLOQUEOS DE YOUTUBE) ---
def descargar_musica_robusta(busqueda):
    archivo_salida = "cancion.mp3"
    if os.path.exists(archivo_salida):
        os.remove(archivo_salida)

    # Buscar en la API pública de Piped
    url_busqueda = f"https://pipedapi.kavin.rocks/search?q={urllib.parse.quote(busqueda)}&filter=music"
    req = urllib.request.Request(url_busqueda, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        datos = json.loads(response.read().decode())
        items = datos.get("items", [])
        if not items:
            raise Exception("No se encontraron resultados.")
        video_id = items[0]["url"].split("v=")[-1]

    # Obtener enlace de audio de Piped
    url_stream = f"https://pipedapi.kavin.rocks/streams/{video_id}"
    req_stream = urllib.request.Request(url_stream, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req_stream) as response:
        datos_stream = json.loads(response.read().decode())
        audio_streams = datos_stream.get("audioStreams", [])
        if not audio_streams:
            raise Exception("Sin stream de audio disponible.")
        
        url_download = audio_streams[0]["url"]

    # Descargar el archivo directamente
    urllib.request.urlretrieve(url_download, archivo_salida)
    return archivo_salida

# --- MANEJADORES DE MENSAJES ---
@bot.message_handler(commands=['start', 'help', 'modo'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("💬 Modo Solo Texto"), telebot.types.KeyboardButton("🎙️ Modo Texto + Voz"))
    bot.send_message(message.chat.id, "¡Hola! Soy Sofía, creada por Abdallah.\n\nElige cómo quieres que te responda:", reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "¡Recibí tu imagen! Qué gran foto me has mandado.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.send_message(message.chat.id, "🎥 Recibí tu video. Extrayendo el audio...")
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("video.mp4", 'wb') as f:
            f.write(downloaded_file)
        os.system("ffmpeg -i video.mp4 -q:a 0 -map a audio_extraido.mp3 -y")
        if os.path.exists("audio_extraido.mp3"):
            with open("audio_extraido.mp3", 'rb') as a:
                bot.send_audio(message.chat.id, a, title="Audio extraído", performer="Sofía Bot")
        for f in ["video.mp4", "audio_extraido.mp3"]:
            if os.path.exists(f): os.remove(f)
    except Exception as e:
        bot.reply_to(message, "Ocurrió un error al procesar el video.")

@bot.message_handler(func=lambda message: True)
def handle_conversation(message):
    user_id = message.chat.id
    user_text = message.text

    if user_text == "💬 Modo Solo Texto":
        modo_usuario[user_id] = "texto"
        bot.send_message(user_id, "✅ Modo activado: Sofía responderá solo en **Texto**.")
        return
    elif user_text == "🎙️ Modo Texto + Voz":
        modo_usuario[user_id] = "voz"
        bot.send_message(user_id, "✅ Modo activado: Sofía responderá con **Texto y Nota de Voz**.")
        return

    user_text_lower = user_text.lower()
    
    if "pdf" in user_text_lower:
        bot.send_chat_action(user_id, 'upload_document')
        tema = user_text_lower.replace("crea un pdf sobre", "").replace("crea un pdf de", "").replace("pdf", "").strip() or "Información General"
        contenido_ia = consultar_ia_gratis(f"Escribe una guía completa sobre: {tema}.")
        archivo = f"documento_{user_id}.pdf"
        generar_pdf(archivo, f"Documento sobre {tema.capitalize()}", contenido_ia)
        with open(archivo, "rb") as f:
            bot.send_document(user_id, f, caption=f"📄 PDF listo sobre: *{tema.capitalize()}*", parse_mode="Markdown")
        if os.path.exists(archivo): os.remove(archivo)
        return

    if "word" in user_text_lower or "doc" in user_text_lower:
        bot.send_chat_action(user_id, 'upload_document')
        tema = user_text_lower.replace("crea un word sobre", "").replace("word", "").replace("doc", "").strip() or "Documento"
        contenido_ia = consultar_ia_gratis(f"Redacta un documento sobre: {tema}.")
        archivo = f"documento_{user_id}.docx"
        generar_word_texto(archivo, tema.capitalize(), contenido_ia)
        with open(archivo, "rb") as f:
            bot.send_document(user_id, f, caption=f"📝 Word listo: *{tema.capitalize()}*", parse_mode="Markdown")
        if os.path.exists(archivo): os.remove(archivo)
        return

    if "excel" in user_text_lower or "tabla" in user_text_lower:
        bot.send_chat_action(user_id, 'upload_document')
        generar_excel("tabla.xlsx")
        with open("tabla.xlsx", "rb") as f: bot.send_document(user_id, f)
        if os.path.exists("tabla.xlsx"): os.remove("tabla.xlsx")
        return

    if "descarga" in user_text_lower or "cancion" in user_text_lower:
        bot.send_message(user_id, "🔍 Buscando y descargando tu música...")
        bot.send_chat_action(user_id, 'upload_document')
        try:
            busqueda = user_text_lower.replace("descarga la canción", "").replace("descarga", "").replace("cancion", "").strip()
            archivo_audio = descargar_musica_robusta(busqueda)
            if archivo_audio and os.path.exists(archivo_audio):
                with open(archivo_audio, "rb") as audio:
                    bot.send_audio(user_id, audio, title=busqueda.capitalize(), performer="Sofía Bot")
                os.remove(archivo_audio)
            else:
                bot.reply_to(message, "No se pudo procesar el archivo de audio.")
            return
        except Exception as e:
            bot.reply_to(message, f"Error en la descarga: {str(e)[:50]}")
            return

    if "dibuja" in user_text_lower or "crea una imagen" in user_text_lower:
        bot.send_message(user_id, "🎨 Creando tu imagen...")
        try:
            prompt = user_text_lower.replace("crea una imagen de", "").replace("dibuja", "").strip()
            prompt_en = consultar_ia_gratis(f"Translate to English only: {prompt}")
            url_imagen = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_en)}?width=1024&height=1024&nologo=true"
            bot.send_photo(user_id, url_imagen, caption=f"Aquí tienes: {prompt.capitalize()}")
            return
        except Exception as e:
            bot.reply_to(message, "No pude generar esa imagen.")
            return

    bot.send_chat_action(user_id, 'typing')
    respuesta_texto = consultar_ia_gratis(user_text)
    bot.send_message(user_id, respuesta_texto)
    
    if modo_usuario.get(user_id) == "voz":
        try:
            archivo_voz = f"voz_{user_id}.mp3"
            gTTS(text=respuesta_texto, lang='es').save(archivo_voz)
            with open(archivo_voz, "rb") as voice:
                bot.send_voice(user_id, voice)
            if os.path.exists(archivo_voz): os.remove(archivo_voz)
        except Exception as e:
            pass

if __name__ == "__main__":
    bot.infinity_polling()
            
