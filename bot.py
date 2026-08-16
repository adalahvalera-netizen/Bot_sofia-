        import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"  
GEMINI_API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"  

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_names = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    user_names.pop(user_id, None)
    bot.reply_to(message, "¡Hola! Soy Sofía, una inteligencia artificial desarrollada por Abdallah Sulbaran. 🤖✨\n\nEstoy aquí para ayudarte en estudios, gaming, TikTok, WhatsApp, vida diaria y mucho más.\n\n¿Cómo te llamas para poder saludarte mejor?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    texto = message.text
    
    if texto.startswith("/"): return

    if user_id not in user_names:
        user_names[user_id] = texto
        bot.reply_to(message, f"¡Mucho gusto, {texto}! ¿En qué te puedo ayudar hoy?")
        return

    # Detector de imágenes
    if any(kw in texto.lower() for kw in ["dibuja", "crea una imagen", "generar una imagen"]):
        prompt = texto.replace(" ", "%20")
        bot.reply_to(message, f"¡Claro! Aquí tienes: https://image.pollinations.ai/prompt/{prompt}")
        return

    # Instrucciones completas integradas en cada mensaje
    instrucciones = (
        "Eres Sofía, una IA creada por Abdallah Sulbaran. Eres experta en: "
        "1. Academia (Matemáticas, programación, ciencia, idiomas). "
        "2. Gaming (Blood Strike, tácticas, skins). "
        "3. Redes sociales (TikTok, WhatsApp). "
        "4. Estilo de vida (Salud, cocina, finanzas, motivación). "
        "5. Entretenimiento (BTS, anime). "
        "Responde como experta y amable a: "
    )

    try:
        response = model.generate_content(f"{instrucciones} {texto}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "¡Ups! Tuve un pequeño error. Por favor, intenta enviarme el mensaje otra vez.")

print("Sofía con funciones activas iniciada...")
bot.infinity_polling()
