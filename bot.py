import os
import requests
import telebot

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
GOOGLE_API_KEY = "AQ.Ab8RN6LpJX7HdcI1Q2563A92sm1oqV0g5gmfk8LkasJ_7P_kHg"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, f"¡Hola {message.from_user.first_name}! Soy Sofía, tu asistente de IA. ¿De qué te gustaría hablar hoy?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": message.text}]
            }]
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # Extraer la respuesta del texto de Gemini
        reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
        bot.reply_to(message, reply_text)
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error al procesar tu solicitud: {e}")

bot.infinity_polling()
