import os
import telebot
import requests

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "hf_F0pCcJGOoKUkqTBhbCPiakSmkxP..."  # Tu token actual

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
headers = {"Authorization": f"Bearer {API_KEY}"}

bot = telebot.TeleBot(TOKEN)
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_states[uid] = {"step": "waiting_name"}
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo te llamas?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    texto = message.text
    
    if uid not in user_states:
        user_states[uid] = {"step": "chat"}
    
    state = user_states[uid]
    
    if state["step"] == "waiting_name":
        state["name"] = texto
        state["step"] = "chat"
        bot.reply_to(message, f"¡Mucho gusto, {texto}! Pregúntame lo que quieras o cuéntame sobre algún tema.")
        return
    
    try:
        payload = {
            "inputs": f"Responde de forma amigable a esto: {texto}",
            "parameters": {"max_new_tokens": 200}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        resultado = response.json()
        
        if isinstance(resultado, list) and len(resultado) > 0 and "generated_text" in resultado[0]:
            respuesta_ia = resultado[0]["generated_text"]
            if "Responde de forma amigable a esto:" in respuesta_ia:
                respuesta_ia = respuesta_ia.split("Responde de forma amigable a esto:")[-1].strip()
        elif isinstance(resultado, dict) and "error" in resultado:
            respuesta_ia = f"¡Hola {state.get('name', 'amigo')}! Dame un segundito y vuelve a enviarme el mensaje."
        else:
            respuesta_ia = f"¡Qué buen tema, {state.get('name', '')}! Cuéntame más detalles sobre eso."

        bot.reply_to(message, respuesta_ia)
    except Exception as e:
        bot.reply_to(message, "¡Aquí estoy! Escríbeme de nuevo para continuar.")

print("Sofía lista...")
bot.infinity_polling()
