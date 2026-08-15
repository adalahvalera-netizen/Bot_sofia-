import os
import google.generativeai as genai
import telebot

TELEGRAM_BOT_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
GOOGLE_API_KEY = "AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A"

# Configurar Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicializar Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message,
      "¡Hola! Soy Sofía, tu asistente virtual con Inteligencia"
      " Artificial. ¿En qué te puedo ayudar hoy?",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(
        message, "Lo siento, ocurrió un error al procesar tu mensaje con la IA."
    )


print("Bot de Sofía iniciado correctamente...")
bot.infinity_polling()
