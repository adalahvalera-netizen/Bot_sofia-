import os
import telebot
from huggingface_hub import InferenceClient

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "hf_F0pCcJGOoKUkqTBhbCPiakSmkxP..."  # Tu token actual

# Cliente optimizado y estable
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2", token=API_KEY)
bot = telebot.TeleBot(TOKEN)
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_states[uid] = {"step": "waiting_name", "history": []}
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo te llamas?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    texto = message.text
    
    if uid not in user_states:
        user_states[uid] = {"step": "chat", "history": []}
    
    state = user_states[uid]
    
    if state["step"] == "waiting_name":
        state["name"] = texto
        state["step"] = "chat"
        bot.reply_to(message, f"¡Mucho gusto, {texto}! ¿En qué te puedo ayudar hoy?")
        return
    
    try:
        # Añadimos el mensaje al historial de conversación
        state["history"].append({"role": "user", "content": texto})
        
        # Generamos la respuesta con la IA
        response = client.chat_completion(
            messages=state["history"][-5:], # Mantiene los últimos 5 mensajes de contexto
            max_tokens=400,
            temperature=0.7,
        )
        
        respuesta_ia = response.choices[0].message.content
        state["history"].append({"role": "assistant", "content": respuesta_ia})
        
        bot.reply_to(message, respuesta_ia)
    except Exception as e:
        print(f"Error detallado: {e}")
        bot.reply_to(message, "¡Vaya! Tuve un pequeño mareo técnico, pero ya volví. ¿Qué me decías?")

print("Bot listo y operativo...")
bot.infinity_polling()
