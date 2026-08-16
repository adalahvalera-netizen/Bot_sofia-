import os
import telebot
import requests

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "hf_F0pCcJGOoKUkqTBhbCPiakSmkxP..."  # Tu token actual

# Usamos este modelo de Hugging Face que es sumamente ligero y responde al instante
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
        bot.reply_to(message, f"¡Mucho gusto, {texto}! ¿De qué te gustaría hablar hoy?")
        return
    
    try:
        payload = {
            "inputs": f"Usuario dice: {texto}. Responde de forma amigable.",
            "parameters": {"max_new_tokens": 250, "temperature": 0.7}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        resultado = response.json()
        
        if isinstance(resultado, list) and len(resultado) > 0 and "generated_text" in resultado[0]:
            respuesta_ia = resultado[0]["generated_text"]
            # Limpiamos el texto para quedarnos solo con la respuesta de la IA
            if "Responde de forma amigable." in respuesta_ia:
                respuesta_ia = respuesta_ia.split("Responde de forma amigable.")[-1].strip()
        elif isinstance(resultado, dict) and "error" in resultado:
            respuesta_ia = f"¡Vaya! El servidor de IA está calentando motores. Intenta enviarme el mensaje de nuevo, {state.get('name', 'amigo')}."
        else:
            respuesta_ia = "¡Qué interesante! Cuéntame más sobre eso."

        bot.reply_to(message, respuesta_ia)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "¡Ey, sigo aquí! Inténtalo otra vez.")

print("Bot listo y fluido...")
bot.infinity_polling()
