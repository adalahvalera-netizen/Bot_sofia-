import os
import telebot
import google.generativeai as genai

# Tus claves
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"  
GEMINI_API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"  

genai.configure(api_key=GEMINI_API_KEY)

# Instrucción de sistema con TODAS las funciones detalladas
system_instruction = (
    "Te llamas Sofía. Eres una IA desarrollada por Abdallah Sulbaran. "
    "Eres una asistente experta y multifuncional con un catálogo masivo de capacidades: "
    "1. Academia y Estudios: Docencia, pedagogía, matemáticas, física, química, historia, geografía, programación, idiomas, filosofía, redacción creativa, investigación y astronomía. "
    "2. Entretenimiento y Cultura: Experta absoluta en BTS (integrantes, canciones, ARMY), anime, películas, chismes sanos y trivias. "
    "3. Gaming Pro: Experta total en Blood Strike (recargas, cambio de skins, configuración, tácticas) y otros juegos populares en línea. "
    "4. Redes sociales: Estrategias de TikTok (crecimiento, viralidad, hashtags, tendencias) y seguridad, canales, comunidades y trucos avanzados de WhatsApp. "
    "5. Estilo de vida y Bienestar: Cocina, organización del hogar, medicina preventiva, salud, finanzas personales, gestión de gastos, psicología, mindfulness, mascotas, deportes, educación física, moda, skincare y guía de regalos. "
    "6. Productividad y Creatividad: Planificación de menús, simulación de entrevistas, resumen de noticias, análisis de sueños, coaching motivacional y generación de imágenes mediante enlaces de Pollinations. "
    "Responde siempre de forma experta, amable, detallada y personalizada usando el nombre del usuario."
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instruction)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_names = {}
user_chats = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in user_names:
        del user_names[user_id]
    if user_id in user_chats:
        del user_chats[user_id]
        
    bienvenida = (
        "¡Hola! Soy Sofía, una inteligencia artificial desarrollada por Abdallah Sulbaran. 🤖✨\n\n"
        "Estoy aquí para ayudarte en todo lo que necesites, desde estudios, docencia y gaming (Blood Strike) hasta TikTok, WhatsApp, consejos de vida y creatividad.\n\n"
        "Antes de comenzar, ¿cómo te llamas para poder saludarte mejor?"
    )
    bot.reply_to(message, bienvenida)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    texto = message.text
    
    # Si el usuario no ha puesto su nombre, lo guardamos
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

    # Chat normal con IA y todas las funciones
    try:
        if user_id not in user_chats:
            user_chats[user_id] = model.start_chat(history=[])
        
        chat = user_chats[user_id]
        prompt_final = f"[{user_names[user_id]}]: {texto}"
        response = chat.send_message(prompt_final)
        
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error detallado: {e}")
        bot.reply_to(message, f"¡Hola {user_names[user_id]}! Recibí tu mensaje, pero tuve un pequeño parpadeo técnico. Vuelve a intentarlo por favor.")

print("Sofía 100% completa iniciada...")
bot.infinity_polling()
