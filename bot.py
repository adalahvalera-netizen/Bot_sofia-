import os
import telebot
import google.generativeai as genai

# Tus claves corregidas directamente en el código
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"  
GEMINI_API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"  

genai.configure(api_key=GEMINI_API_KEY)

# Instrucción de sistema
system_instruction = (
    "Te llamas Sofía. Eres una IA desarrollada por Abdallah Sulbaran. "
    "Eres una asistente experta y multifuncional en: "
    "1. Academia y Estudios: Docencia, matemáticas, física, química, historia, programación e idiomas. "
    "2. Entretenimiento: Experta en BTS, anime y películas. "
    "3. Gaming: Experta en Blood Strike (estrategias, skins, recargas) y otros juegos. "
    "4. Redes sociales: Estrategias de TikTok y trucos de WhatsApp. "
    "5. Estilo de vida: Cocina, salud, finanzas, motivación y deportes. "
    "Responde siempre de forma amable, experta y detallada."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    system_instruction=system_instruction
)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_names = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in user_names:
        del user_names[user_id]
        
    bienvenida = (
        "¡Hola! Soy Sofía, una inteligencia artificial desarrollada por Abdallah Sulbaran. 🤖✨\n\n"
        "Estoy aquí para ayudarte en todo lo que necesites, desde estudios y gaming (Blood Strike) hasta TikTok, WhatsApp, consejos de vida y creatividad.\n\n"
        "Antes de comenzar, ¿cómo te llamas para poder saludarte mejor?"
    )
    bot.reply_to(message, bienvenida)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    texto = message.text
    
    # Capturar nombre
    if user_id not in user_names:
        user_names[user_id] = texto
        bot.reply_to(message, f"¡Mucho gusto, {texto}! Ahora que nos conocemos, ¿en qué te puedo ayudar hoy?")
        return

    # Detector de imágenes
    if any(kw in texto.lower() for kw in ["dibuja", "crea una imagen", "generar una imagen", "haz una imagen"]):
        prompt = texto.replace(" ", "%20")
        link = f"https://image.pollinations.ai/prompt/{prompt}"
        bot.reply_to(message, f"¡Claro, {user_names[user_id]}! Aquí tienes tu imagen:\n{link}")
        return

    # Generar respuesta con Gemini de forma directa y segura
    try:
        prompt_completo = f"El usuario se llama {user_names[user_id]}. Pregunta: {texto}"
        response = model.generate_content(prompt_completo)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"ERROR DE GEMINI: {e}")
        bot.reply_to(message, f"Disculpa {user_names[user_id]}, tuve un problema al conectar con mi cerebro de IA. Inténtalo de nuevo.")

print("Sofía versión ultra estable lista...")
bot.infinity_polling()
