import os
import google.generativeai as genai
import telebot

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
GOOGLE_API_KEY = "AQ.Ab8RN6LpJX7HdcI1Q2563A92sm1oqV0g5gmfk8LkasJ_7P_kHg"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, f"¡Hola {message.from_user.first_name}! Soy Sofía, tu asistente de IA. ¿De qué te gustaría hablar hoy?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {e}")

bot.infinity_polling()
