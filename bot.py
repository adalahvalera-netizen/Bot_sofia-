import os
import telebot
import google.generativeai as genai

# Obtenemos las variables de entorno que guardamos en Railway
TELEGRAM_TOKEN = os.environ.get("8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I")
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6LdVyO9hrXi1NlvAGDX9iPOd9n6Lk4dmfvaRNDDvY142A")

# Configuramos la IA de Gemini con el modelo actual y rápido
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.7,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", generation_config=generation_config
)

# Inicializamos el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Mensaje de bienvenida para cuando le escribas /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "¡Hola! Soy Sofía, tu asistente virtual con Inteligencia Artificial."
      " Escríbeme lo que quieras y charlamos.",
  )


# Manejador para cualquier texto libre que le escribas
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    # Enviamos el texto del usuario directamente a Gemini
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(
        message, "Lo siento, ocurrió un error al procesar tu mensaje con la IA."
    )


# Ejecutamos el bot
print("Bot iniciado correctamente...")
bot.infinity_polling()

