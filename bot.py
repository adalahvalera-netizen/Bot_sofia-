import os
import telebot
import google.generativeai as genai

# Tus claves
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"  
GEMINI_API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"  

genai.configure(api_key=GEMINI_API_KEY)

# Instrucción de sistema (el cerebro de Sofía)
system_instruction = (
    "Te llamas Sofía. Eres una IA desarrollada por Abdallah Sulbaran. "
    "Tu objetivo es ser la asistente más útil y completa. "
    "Cuando un usuario nuevo te escriba y te diga su nombre, recuerda usarlo para interactuar de forma personalizada. "
    "Tu capacidad abarca: "
    "1. Academia: Docencia, matemáticas, ciencias, programación e idiomas. "
    "2. Entretenimiento: Experta en BTS, anime, películas y trivias. "
    "3. Gaming: Estrategias, skins y recargas de Blood Strike y otros juegos. "
    "4. Redes: Estrategias de TikTok y trucos de WhatsApp. "
    "5. Estilo de vida: Cocina, salud, finanzas, motivación, mascotas y deportes. "
    "6. Creatividad: Generación de imágenes mediante enlaces. "
    "Responde siempre como una asistente experta, amable y eficiente."
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instruction)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Diccionarios para memoria y nombres
chat_histories = {}
user_names = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bienvenida = (
        "¡Hola! Soy Sofía, una inteligencia artificial desarrollada por Abdallah Sulbaran. 🤖✨\n\n"
        "Estoy aquí para ayudarte en todo lo que necesites, desde estudios y gaming hasta consejos de vida y creatividad.\n\n"
        "Antes de comenzar, ¿cómo te llamas para poder saludarte mejor?"
    )
    bot.reply_to(message, bienvenida)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    texto = message.text
    
    # Lógica para capturar el nombre si el usuario aún no lo ha dicho
    if user_id not in user_names:
        user_names[user_id] = texto
        bot.reply_to(message, f"¡Mucho gusto, {texto}! Ahora que nos conocemos, ¿en qué puedo ayudarte hoy? Recuerda que puedo ayudarte con estudios, gaming (como Blood Strike), redes sociales, consejos de vida ¡y más!")
        return

    # Lógica para imágenes
    if any(keyword in texto.lower() for keyword in ["dibuja", "crea una imagen", "generar una imagen", "haz una imagen"]):
        prompt = texto.replace(" ", "%20")
        link = f"https://image.pollinations.ai/prompt/{prompt}"
        bot.reply_to(message, f"¡Claro, {user_names[user_id]}! Aquí tienes tu imagen:\n{link}")
    else:
        # Chat normal con IA
        try:
            if user_id not in chat_histories:
                chat_histories[user_id] = model.start_chat(history=[])
            
            # Incluimos el nombre del usuario en el contexto
            contexto = f"El usuario se llama {user_names[user_id]}. Mensaje: {texto}"
            response = chat_histories[user_id].send_message(contexto)
            bot.reply_to(message, response.text)
        except Exception as e:
            print(f"Error: {e}")
            bot.reply_to(message, "Ocurrió un error, pero ya estoy trabajando en ello.")

print("Sofía pública con registro de nombres iniciada...")
bot.infinity_polling()
