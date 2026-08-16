import os
import telebot
import requests

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "AQ.Ab8RN6JI1KcoEmGrIPtbW-UEa0Y..." # Pon aquí tu clave completa

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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": texto}]
            }]
        }
        
        response = requests.post(url, json=data, headers=headers)
        resultado = response.json()
        
        respuesta_ia = resultado['candidates'][0]['content']['parts'][0]['text']
        bot.reply_to(message, respuesta_ia)
        
    except Exception as e:
        print(f"Error detallado: {e}")
        bot.reply_to(message, f"Disculpa {user_names[uid]}, hubo un problema al procesar la respuesta.")

print("Bot listo...")
bot.infinity_polling()
