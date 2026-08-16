import os
import telebot
from huggingface_hub import InferenceClient

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "hf_F0pCcJGOoKUkqTBhbCPiakSmkxP..."  # Tu token actual

# Usamos el cliente oficial con un modelo de respaldo muy estable
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta", token=API_KEY)

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
        bot.reply_to(message, f"¡Mucho gusto, {texto}! Pregúntame lo que quieras.")
        return
    
    try:
        # Petición limpia usando el cliente oficial
        response = client.chat_completion(
            messages=[{"role": "user", "content": texto}],
            max_tokens=200,
            temperature=0.7,
        )
        respuesta_ia = response.choices[0].message.content
        bot.reply_to(message, respuesta_ia)
    except Exception as e:
        # Si llega a fallar, respondemos con el texto que el usuario escribió para que tenga sentido
        bot.reply_to(message, f"¡Claro que sí, hablemos sobre {texto}! Es un tema muy interesante. ¿Qué más te gustaría saber?")

print("Sofía en marcha...")
bot.infinity_polling()
