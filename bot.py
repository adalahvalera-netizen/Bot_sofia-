import os
import telebot
import requests

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "hf_F0pCcJGOoKUkqTBhbCPiakSmkxP..."  # Tu token actual

# Usamos la API web directa de Hugging Face para evitar errores de librerías
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
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
        bot.reply_to(message, f"¡Mucho gusto, {texto}! ¿En qué te puedo ayudar hoy?")
        return
    
    try:
        # Petición directa a la IA
        payload = {
            "inputs": f"Responde de forma amigable y útil: {texto}",
            "parameters": {"max_new_tokens": 300, "temperature": 0.7}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        resultado = response.json()
        
        if isinstance(resultado, list) and len(resultado) > 0 and "generated_text" in resultado[0]:
            respuesta_ia = resultado[0]["generated_text"]
            # Limpiamos el texto para que no repita el prompt inicial
            if "Responde de forma amigable y útil:" in respuesta_ia:
                respuesta_ia = respuesta_ia.split("Responde de forma amigable y útil:")[-1].strip()
        elif isinstance(resultado, dict) and "error" in resultado:
            respuesta_ia = "¡Hola! Dame unos segundos mientras el modelo de IA despierta y vuelve a escribirme."
        else:
            respuesta_ia = "¡Entendido! ¿Qué más te gustaría saber?"

        bot.reply_to(message, respuesta_ia)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "¡Hola! Estoy aquí. ¿De qué te gustaría hablar?")

print("Bot listo y conectado...")
bot.infinity_polling()
