import requests
import telebot

TELEGRAM_TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, f"¡Hola {message.from_user.first_name}! Soy Sofía, tu asistente de IA. ¿De qué te gustaría hablar hoy?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Usamos una API de IA pública y gratuita que no requiere claves
        prompt = message.text
        url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
        
        response = requests.get(url)
        if response.status_code == 200:
            answer = response.text
            bot.reply_to(message, answer)
        else:
            bot.reply_to(message, "Lo siento, tuve un pequeño problema procesando tu mensaje. Inténtalo de nuevo.")
            
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {e}")

bot.infinity_polling()
