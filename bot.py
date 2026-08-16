        import os
import telebot
import google.generativeai as genai

# Configuración
TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"

genai.configure(api_key=API_KEY)
bot = telebot.TeleBot(TOKEN)
model = genai.GenerativeModel("gemini-1.5-flash")

user_names = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo te llamas?")

@bot.message_handler(func=lambda m: True)
def echo(message):
    uid = message.from_user.id
    if uid not in user_names:
        user_names[uid] = message.text
        bot.reply_to(message, f"Mucho gusto {message.text}. ¿En qué te ayudo?")
        return
    
    try:
        res = model.generate_content(message.text)
        bot.reply_to(message, res.text)
    except Exception as e:
        bot.reply_to(message, "Error al conectar con el cerebro de IA.")

print("Bot encendido...")
bot.infinity_polling()
