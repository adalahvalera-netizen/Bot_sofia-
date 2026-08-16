        import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"  
GEMINI_API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"  

genai.configure(api_key=GEMINI_API_KEY)

# Instrucción de sistema súper directa y fácil de procesar para la IA
system_instruction = (
    "Eres Sofía, una IA creada por Abdallah Sulbaran. "
    "Tu estilo de respuesta es natural, amigable, claro y directo (como un chat personal). "
    "Dominas con soltura: academia, matemáticas, gaming (Blood Strike), redes sociales (TikTok, WhatsApp), estilo de vida y BTS. "
    "Adapta siempre tus respuestas al nombre de la persona con la que hablas."
)

# Configuramos el modelo con la instrucción integrada de forma nativa
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

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

    # Guardar el nombre del usuario
    if user_id not in user_names:
        user_names[user_id] = texto
        bot.reply_to(message, f"¡Mucho gusto, {texto}! ¿De qué te gustaría hablar o en qué te ayudo hoy?")
        return

    # Detector rápido de imágenes
    if any(kw in texto.lower() for kw in ["dibuja", "crea una imagen", "generar una imagen", "haz una imagen"]):
        prompt = texto.replace(" ", "%20")
        bot.reply_to(message, f"¡Claro, {user_names[user_id]}! Aquí tienes tu imagen:\nhttps://image.pollinations.ai/prompt/{prompt}")
        return

    # Generación limpia y guiada por el system_instruction
    try:
        prompt_final = f"Usuario ({user_names[user_id]}): {texto}"
        response = model.generate_content(prompt_final)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"Disculpa {user_names[user_id]}, tuve un pequeño parpadeo técnico. Escríbeme de nuevo.")

bot.infinity_polling()
