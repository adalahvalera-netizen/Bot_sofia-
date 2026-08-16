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
        # Usamos un servicio público de chat gratuito
        url = "https://api.duckduckgo.com/"
        params = {
            "q": message.text,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # Obtenemos una respuesta más limpia o directa
        answer = data.get("AbstractText") or data.get("Answer")
        
        if not answer and data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if "Text" in topic:
                    answer = topic["Text"]
                    break
                    
        if answer:
            bot.reply_to(message, answer)
        else:
            bot.reply_to(message, f"Entendido, {message.from_user.first_name}. ¿Podrías darme más detalles sobre lo que me comentas?")
            
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {e}")

bot.infinity_polling()
