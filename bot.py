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
    bot.reply_to(message, "¡Hola! Soy Sofía, una inteligencia artificial desarrollada por Abdallah Sulbaran. 🤖✨\n\nEstoy aquí para ayudarte en estudios, docencia, gaming (Blood Strike), TikTok, WhatsApp, consejos de vida, BTS y mucho más.\n\n¿Cómo te llamas para poder saludarte mejor?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    texto = message.text
    
    if texto.startswith("/"): 
        return

    if user_id not in user_names:
        user_names[user_id] = texto
        bot.reply_to(message, f"¡Mucho gusto, {texto}! Ahora que nos conocemos, ¿en qué te puedo ayudar hoy?")
        return

    # Detector de imágenes
    if any(kw in texto.lower() for kw in ["dibuja", "crea una imagen", "generar una imagen", "haz una imagen"]):
        prompt = texto.replace(" ", "%20")
        bot.reply_to(message, f"¡Claro, {user_names[user_id]}! Aquí tienes tu imagen:\nhttps://image.pollinations.ai/prompt/{prompt}")
        return

    # Instrucciones detalladas con todas las funciones integradas
    instrucciones = (
        f"Te llamas Sofía y fuiste desarrollada por Abdallah Sulbaran. "
        f"Estás hablando con {user_names[user_id]}. "
        "Eres una asistente experta y multifuncional en: "
        "1. Academia y Estudios: Docencia, matemáticas, física, química, historia, programación, redacción e idiomas. "
        "2. Entretenimiento: Experta en BTS, anime, películas y trivias. "
        "3. Gaming Pro: Experta total en Blood Strike (estrategias, skins, recargas) y juegos en línea. "
        "4. Redes sociales: Estrategias de TikTok (viralidad, hashtags) y trucos avanzados de WhatsApp. "
        "5. Estilo de vida: Cocina, salud, finanzas personales, motivación, deportes y bienestar. "
        "Responde de forma experta, amable y personalizada. Mensaje del usuario: "
    )

    try:
        response = model.generate_content(f"{instrucciones} {texto}")
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"Disculpa {user_names[user_id]}, tuve un pequeño parpadeo técnico. Vuelve a intentarlo por favor.")

bot.infinity_polling()
