import os
import google.generativeai as genai
import telebot

# Tus credenciales directas
TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
GOOGLE_API_KEY = "AQ.Ab8RN6LpJX7HdcI1Q2563A92sm1oqV0g5gmfk8LKasJ_7P_kHg"

# Configurar la IA de Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Usar el modelo actual recomendado
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicializar el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message,
      f"¡Hola {message.from_user.first_name}! Soy Sofía, tu asistente de IA."
      " ¿De qué te gustaría hablar o qué quieres que investiguemos hoy?",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    # Enviar el mensaje del usuario a Gemini
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(
        message,
        f"¡Vaya {message.from_user.first_name}! Ocurrió un pequeño error al"
        f" conectar con mi cerebro de IA. Detalle: {e}",
    )


# Iniciar el bot de forma continua
print("Bot iniciado correctamente y escuchando...")
bot.infinity_polling()
