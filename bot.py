import os
import telebot
from huggingface_hub import InferenceClient

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "hf_F0pCcJGOoKUkqTBhbCPiakSmkxP..."  # Tu token actual

# Usamos este modelo que responde súper bien
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=API_KEY)
bot = telebot.TeleBot(TOKEN)
user_names = {}

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_names.pop(uid, None)
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo te llamas?")

@bot.message_handler(func=lambda m: True)
def echo(message):
    uid = message.from_user.id
    texto = message.text
    
    if uid not in user_names:
        user_names[uid] = texto
        bot.reply_to(message, f"¡Mucho gusto, {texto}! ¿En qué te puedo ayudar hoy?")
        return
    
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": texto}],
            max_tokens=500,
            temperature=0.7,
        )
        respuesta_ia = response.choices[0].message.content
        bot.reply_to(message, respuesta_ia)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"Disculpa {user_names[uid]}, hubo un error al procesar la respuesta.")

print("Bot listo...")
bot.infinity_polling()
