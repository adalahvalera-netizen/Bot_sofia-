import os
import telebot
import google.generativeai as genai

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "AQ.Ab8RN6I-EYPGbLG_jAslbEzhMGzOaUwkGhuRwjCPZS_DwZhoDQ"

genai.configure(api_key=API_KEY)
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
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(texto)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error detallado: {e}")
        bot.reply_to(message, f"Disculpa {user_names[uid]}, hubo un pequeño problema con la IA.")

print("Bot listo...")
bot.infinity_polling()
