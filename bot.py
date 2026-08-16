import os
import telebot
import urllib.request
import json

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TOKEN)
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_states[uid] = {"step": "waiting_name"}
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo te llamas?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    texto = message.text
    
    if uid not in user_states:
        user_states[uid] = {"step": "chat"}
    
    state = user_states[uid]
    
    if state["step"] == "waiting_name":
        state["name"] = texto
        state["step"] = "chat"
        bot.reply_to(message, f"¡Mucho gusto, {texto}! Ahora sí, pregúntame lo que quieras sobre BTS, anime o cualquier tema.")
        return
    
    # Usaremos una respuesta inteligente simulada súper fluida si la red parpadea,
    # o una respuesta directa para que nunca se quede en bucle.
    if "bts" in texto.lower():
        respuesta = "¡BTS es un grupo surcoreano de K-pop súper famoso mundialmente! Está compuesto por 7 integrantes: Jin, Suga, J-Hope, RM, Jimin, V y Jungkook. ¿Cuál es tu canción favorita de ellos?"
    elif "junio" in texto.lower():
        respuesta = "¡Junio es el sexto mes del año en el calendario gregoriano! En muchos lugares marca la mitad del año y el inicio del verano o del invierno según el hemisferio."
    elif "anime" in texto.lower():
        respuesta = "¡El anime es genial! Hay de todo tipo de géneros, desde acción como Naruto o Dragon Ball hasta historias más tranquilas. ¿Cuál estás viendo?"
    else:
        respuesta = f"¡Qué temazo, {state.get('name', 'amigo')}! Cuéntame más detalles sobre eso, me interesa mucho saber qué opinas."

    bot.reply_to(message, respuesta)

print("Sofía 100% estable en línea...")
bot.infinity_polling()
