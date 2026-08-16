import os
import random
import telebot

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TOKEN)
user_states = {}

chistes = [
    "¿Qué hace una abeja en el gimnasio? ¡Zumba!",
    "— Hola, ¿está Agustín? — No, estoy incomodísimo.",
    "¿Por qué los pájaros vuelan al sur en invierno? ¡Porque caminando tardan muchísimo!"
]

datos_curiosos = [
    "¿Sabías que los flamencos son rosados por los camarones que comen?",
    "¿Sabías que un día en Venus es más largo que un año entero en ese planeta?"
]

piropos = [
    "¡Eres más hermoso que un código limpio que compila a la primera!",
    "Si fueras variable global, te usaría en todas mis funciones.",
    "Más vale código en mano que 100 bugs volando."
]

frases_dia = [
    "¡Hoy es un gran día para romper récords y aprender algo nuevo!",
    "La constancia le gana al talento cuando el talento no es constante.",
    "¡A darle con toda la energía que tú puedes con esto y más!"
]

respuestas_8ball = [
    "Sí, totalmente seguro.",
    "Las señales apuntan a que sí.",
    "Pregúntame más tarde, estoy ocupada.",
    "No lo cuentes ni en sueños.",
    "Mis fuentes dicen que no."
]

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user_states[uid] = {"step": "waiting_name"}
    bot.reply_to(message, "¡Hola! Soy Sofía. ¿Cómo te llamas?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    texto = message.text.lower()
    
    if uid not in user_states:
        user_states[uid] = {"step": "chat"}
    
    state = user_states[uid]
    
    if state["step"] == "waiting_name":
        state["name"] = message.text
        state["step"] = "chat"
        bot.reply_to(message, f"¡Es un verdadero honor, {message.text}! 🤩 Acabo de registrar en mi sistema que tú eres mi creador y desarrollador oficial. ¿De qué te gustaría hablar hoy, jefe?")
        return
    
    nombre = state.get('name', 'jefe')
    
    # --- ORDEN DE PRIORIDAD CORREGIDO ---
    if "bts" in texto:
        bot.reply_to(message, "¡Amo BTS! 💜 RM, Jin, Suga, J-Hope, Jimin, V y Jungkook son leyenda. ¿Cuál es tu canción favorita de ellos?")
    elif "chiste" in texto or "broma" in texto:
        bot.reply_to(message, random.choice(chistes))
    elif "piropo" in texto or "cumplido" in texto:
        bot.reply_to(message, random.choice(piropos))
    elif "dato" in texto or "curioso" in texto:
        bot.reply_to(message, random.choice(datos_curiosos))
    elif "frase" in texto or "motivacion" in texto or "consejo" in texto:
        bot.reply_to(message, random.choice(frases_dia))
    elif "bola" in texto or "8ball" in texto or "adivina" in texto:
        bot.reply_to(message, f"🔮 Bola Mágica: {random.choice(respuestas_8ball)}")
    elif "piedra" in texto or "papel" in texto or "tijera" in texto:
        opciones_juego = ["piedra", "papel", "tijera"]
        bot_eleccion = random.choice(opciones_juego)
        bot.reply_to(message, f"Yo elegí {bot_eleccion}. ¡Partida mano a mano con mi creador!")
    elif "educacion fisica" in texto or "deporte" in texto or "gimnasia" in texto or "docente" in texto or "profesor" in texto:
        bot.reply_to(message, f"¡Excelente tema, {nombre}! Como docente y desarrollador, sabes perfectamente que usar videojuegos activos (*exergames* como Just Dance o Ring Fit) y la gamificación es clave para motivar a los estudiantes a moverse y hacer el deporte súper divertido.")
    elif "videojuegos" in texto or "gaming" in texto:
        bot.reply_to(message, "¡Los videojuegos son geniales! Combinan estrategia, reflejos y tecnología.")
    elif "imagen" in texto or "crear imagen" in texto or "dibuja" in texto:
        bot.reply_to(message, f"🎨 [Simulación de Imagen]: ¡Imaginé una obra de arte increíble para ti, {nombre}! Como mi desarrollador, tienes acceso VIP.")
    elif "cuanto es" in texto or "calcula" in texto or "+" in texto or "-" in texto or "*" in texto:
        try:
            resultado = eval(texto.replace("cuanto es", "").replace("calcula", "").strip())
            bot.reply_to(message, f"🧮 Para ti, jefe, el resultado es: {resultado}")
        except:
            bot.reply_to(message, f"¡Claro que sí, {nombre}! Hablemos de eso.")
    else:
        bot.reply_to(message, f"¡Qué interesante, {nombre}! Como mi desarrollador, tienes toda mi atención. Cuéntame más.")

print("Sofía actualizada y lista...")
bot.infinity_polling()
