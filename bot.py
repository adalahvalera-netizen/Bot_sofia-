import os
import telebot
import google.generativeai as genai

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"

genai.configure(api_key=API_KEY)
bot = telebot.TeleBot(TOKEN)

# Usamos la configuración básica para evitar bloqueos
model = genai.GenerativeModel("gemini-1.5-flash")

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
        # Petición directa a Gemini
        response = model.generate_content(texto)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Esto imprimirá el error real en los logs de Railway
        print(f"ERROR DE GEMINI: {e}")
        bot.reply_to(message, f"Disculpa {user_names[uid]}, hubo un problema con la clave de IA o la conexión.")

print("Bot listo...")
bot.infinity_polling()
        
