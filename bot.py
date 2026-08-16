        import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"  
GEMINI_API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"  

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_names = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    user_names.pop(user_id, None)
    bot.reply_to(message, "¡Hola! Soy Sofía, una inteligencia artificial desarrollada por Abdallah Sulbaran. 🤖✨\n\n¿Cómo te llamas para poder saludarte mejor?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    texto = message.text
    
    if texto.startswith("/"): 
        return

    if user_id not in user_names:
        user_names[user_id] = texto
        bot.reply_to(message, f"¡Mucho gusto, {texto}! ¿En qué te puedo ayudar hoy?")
        return

    # Detector de imágenes
    if any(kw in texto.lower() for kw in ["dibuja", "crea una imagen", "generar una imagen", "haz una imagen"]):
        prompt = texto.replace(" ", "%20")
        bot.reply_to(message, f"¡Claro, {user_names[user_id]}! Aquí tienes tu imagen:\nhttps://image.pollinations.ai/prompt/{prompt}")
        return

    prompt_seguro = (
        f"Estás hablando con {user_names[user_id]}. "
        "Te llamas Sofía y fuiste desarrollada por Abdallah Sulbaran. "
        "Eres experta en academia, matemáticas, gaming (Blood Strike), TikTok, WhatsApp, estilo de vida y BTS. "
        "Responde de forma natural, amigable y experta a lo siguiente: " + texto
    )

    try:
        response = model.generate_content(prompt_seguro)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error detectado: {e}")
        bot.reply_to(message, f"Hola {user_names[user_id]}, recibí tu mensaje. ¿Podrías repetirlo?")

bot.infinity_polling()
