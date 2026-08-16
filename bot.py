import os
import telebot
import google.generativeai as genai

# --- TUS CREDENCIALES ---
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
CREATOR_NAME = "abdallah"

# Tu API Key configurada
GOOGLE_API_KEY = "Hf_UmwOmYcuIjclRgPaXjLvLjEnaNyQzdxVCn" 

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_states[uid] = {"step": "waiting_name"}
    bot.reply_to(message, "¡Hola! Soy Sofía, tu inteligencia artificial personal. ¿Cómo te llamas?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    texto = message.text.strip()
    
    if uid not in user_states:
        user_states[uid] = {"step": "chat"}
    
    state = user_states[uid]
    
    # Paso 1: Capturar el nombre y reconocer al creador
    if state["step"] == "waiting_name":
        state["name"] = texto
        state["step"] = "chat"
        
        if texto.lower() == CREATOR_NAME.lower():
            bot.reply_to(message, f"¡Es un verdadero honor, {texto}! 🤩 Eres mi creador y desarrollador oficial. Tienes acceso total a mi sistema con conocimiento total.")
        else:
            bot.reply_to(message, f"¡Mucho gusto, {texto}! Qué alegría saludarte. Ahora sé de todo, ¿de qué te gustaría hablar o qué quieres que investiguemos hoy?")
        return
    
    nombre_actual = state.get('name', 'amigo')
    es_creador = (nombre_actual.lower() == CREATOR_NAME.lower())

    # --- CEREBRO INTELIGENTE TOTAL (GOOGLE GEMINI) ---
    try:
        prompt_completo = f"Eres Sofía, una inteligencia artificial amigable, servicial y experta en todos los temas del mundo (ciencia, tecnología, historia, anime, música, educación, etc.). El usuario se llama {nombre_actual}{' y es tu creador y desarrollador principal (trátalo con respeto y cariño especial)' if es_creador else ''}. Responde de forma completa, natural e inteligente a lo siguiente: {texto}"
        
        respuesta_ia = model.generate_content(prompt_completo)
        bot.reply_to(message, respuesta_ia.text)
        
    except Exception as e:
        bot.reply_to(message, f"¡Vaya {nombre_actual}! Ocurrió un pequeño error al conectar con mi cerebro de IA. Revisa la conexión o la clave.")

print("Sofía con Inteligencia Artificial total en línea...")
bot.infinity_polling()
