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
        # Usamos una API pública gratuita que responde sin claves de Google
        url = f"https://api.duckduckgo.com/?q={requests.utils.quote(message.text)}&format=json"
        response = requests.get(url)
        data = response.json()
        
        # Buscamos una respuesta resumida
        answer = data.get("AbstractText")
        if not answer:
            # Si no hay resumen directo, buscamos en los temas relacionados
            topics = data.get("RelatedTopics", [])
            for topic in topics:
                if "Text" in topic:
                    answer = topic["Text"]
                    break
        
        if answer:
            bot.reply_to(message, answer)
        else:
            bot.reply_to(message, "¡Hola! Entendido sobre tu mensaje. ¿Te puedo ayudar con algo más específico?")
            
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error al procesar tu solicitud: {e}")

bot.infinity_polling()
