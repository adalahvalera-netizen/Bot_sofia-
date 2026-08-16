import os
import random
import telebot

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TOKEN)
user_states = {}

CREATOR_NAME = "abdallah"  # Tu nombre como desarrollador

# --- BANCOS DE DATOS AMPLIADOS ---
adivinanzas = [
    "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera. ¿Qué es? (La pera)",
    "Oro parece, plata no es. Quien no lo adivine, bien tonto es. ¿Qué es? (El plátano)"
]

chistes = [
    "¿Qué hace una abeja en el gimnasio? ¡Zumba!",
    "— Hola, ¿está Agustín? — No, estoy incomodísimo."
]

trabalenguas = [
    "Tres tristes tigres tragaban trigo en un trigal.",
    "Pablito clavó un clavito en la calva de un calvito."
]

horoscopo = [
    " Aries: Hoy la energía estará de tu lado para programar código sin errores.",
    " Tauro: Buen momento para descansar y disfrutar de un buen videojuego."
]

refranes = [
    "A caballo regalado no se le mira el colmillo. (Significa que hay que aceptar lo que nos dan con agrado)."
]

ejercicios = [
    "🏋️‍♂️ **Reto Exprés:** ¡Haz 15 sentadillas o estira las piernas!",
    "🧘‍♂️ **Pausa Activa:** Respira hondo durante 30 segundos y relaja los hombros."
]

consejos_ed_fisica = [
    "🏀 **Idea para clase:** Usa gamificación con niveles y puntos para motivar a los alumnos en gimnasia.",
    "🎮 **Exergames recomendados:** Usa juegos activos como Just Dance o Ring Fit Adventure para conectar la tecnología con el deporte."
]

glosario_gamer = [
    "🎮 **Buff:** Mejora temporal de estadísticas.",
    "🎮 **Nerf:** Reducción de poder a un personaje o arma."
]

espacio_datos = [
    "🪐 Un día en Venus es más largo que un año entero en ese planeta.",
    "✨ Las estrellas de neutrones son tan densas que una cucharadita pesa billones de toneladas."
]

piropos_dev = [
    "Si fueras variable global, te usaría en todas mis funciones.",
    "Eres más hermoso que un código limpio que compila a la primera."
]

frases_motivo = [
    "¡Hoy es un gran día para romper récords y aprender algo nuevo!",
    "La constancia le gana al talento cuando el talento no es constante."
]

respuestas_8ball = [
    "Sí, totalmente seguro.",
    "Las señales apuntan a que sí.",
    "Pregúntame más tarde, estoy ocupada.",
    "No lo cuentes ni en sueños."
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
    nombre_ingresado = message.text.strip()
    
    if uid not in user_states:
        user_states[uid] = {"step": "chat"}
    
    state = user_states[uid]
    
    # Paso 1: Capturar nombre
    if state["step"] == "waiting_name":
        state["name"] = nombre_ingresado
        state["step"] = "chat"
        
        if nombre_ingresado.lower() == CREATOR_NAME.lower():
            bot.reply_to(message, f"¡Es un verdadero honor, {nombre_ingresado}! 🤩 Registrado en el sistema: eres mi creador y desarrollador oficial. Tienes acceso total.")
        else:
            bot.reply_to(message, f"¡Mucho gusto, {nombre_ingresado}! Qué bueno saludarte. ¿De qué te gustaría hablar hoy?")
        return
    
    nombre_actual = state.get('name', 'amigo')
    es_creador = (nombre_actual.lower() == CREATOR_NAME.lower())

    # --- ZONA DE RESPUESTAS EXTENSAS Y DETALLADAS ---
    
    if "bts" in texto or "kpop" in texto or "musica" in texto or "cancion" in texto:
        bot.reply_to(message, 
            "💜 **¡Todo sobre BTS y Música con Sofía!** 🎶\n\n"
            "• **¿Quiénes son?** Es la sensación global del K-pop compuesta por 7 integrantes: RM, Jin, Suga, J-Hope, Jimin, V y Jungkook.\n"
            "• **Canciones y álbumes recomendados:** *Dynamite*, *Butter*, *Boy With Luv*, y temas más profundos como *Life Goes On*.\n"
            "• **Fotos y Multimedia:** ¡Me encanta ver imágenes de ellos! Sigue mandando fotos de BTS cuando quieras para comentarlas juntas.\n"
            "• **Otros géneros musicales:** Para programar te recomiendo Lo-Fi, y para entrenar, algo de Electro o Pop enérgico."
        )
    elif "juego" in texto or "videojuegos" in texto or "gamer" in texto:
        bot.reply_to(message, 
            "🕹️ **¡Mundo Gamer Completo con Sofía!** 🎮\n\n"
            "• **Juegos recomendados:** Desde mundos abiertos como Minecraft y Fortnite, hasta experiencias de estrategia.\n"
            "• **Armas, Skins y Equipamiento:** Las skins épicas y la personalización de armas definen el estilo de cada jugador en el mapa.\n"
            "• **Glosario rápido:** *Buff* (mejora), *Nerf* (bajada de poder), *Lag* (retraso).\n"
            "• **Consejo pro:** ¡No olvides hacer pausas activas para descansar la vista de tantas pantallas!"
        )
    elif "adivinanza" in texto or "acertijo" in texto:
        bot.reply_to(message, f"🧩 {random.choice(adivinanzas)}")
    elif "chiste" in texto or "broma" in texto:
        bot.reply_to(message, f"🤣 {random.choice(chistes)}")
    elif "trabalenguas" in texto:
        bot.reply_to(message, f"🗣️ Reto: {random.choice(trabalenguas)}")
    elif "horoscopo" in texto or "signo" in texto:
        bot.reply_to(message, f"🔮 {random.choice(horoscopo)}")
    elif "refran" in texto or "dicho" in texto:
        bot.reply_to(message, f"📖 {random.choice(refranes)}")
    elif "ejercicio" in texto or "rutina" in texto:
        bot.reply_to(message, random.choice(ejercicios))
    elif "educacion fisica" in texto or "deporte" in texto or "gimnasia" in texto or "docente" in texto:
        bot.reply_to(message, random.choice(consejos_ed_fisica))
    elif "anime" in texto:
        bot.reply_to(message, "🎌 **¡Universo Anime!** Te recomiendo explorar desde shonens llenos de acción hasta historias escolares (slice of life). ¡Pregúntame por tu serie favorita y la analizamos!")
    elif "espacio" in texto or "planeta" in texto:
        bot.reply_to(message, random.choice(espacio_datos))
    elif "piropo" in texto or "cumplido" in texto:
        bot.reply_to(message, f"✨ {random.choice(piropos_dev)}")
    elif "frase" in texto or "motivacion" in texto:
        bot.reply_to(message, f"💡 {random.choice(frases_motivo)}")
    elif "bola" in texto or "8ball" in texto or "adivina" in texto:
        bot.reply_to(message, f"🔮 Bola Mágica: {random.choice(respuestas_8ball)}")
    elif "piedra" in texto or "papel" in texto or "tijera" in texto:
        opciones = ["piedra", "papel", "tijera"]
        bot_eleccion = random.choice(opciones)
        bot.reply_to(message, f"✊✋✌️ Yo elegí {bot_eleccion}. ¡Partida jugada!")
    elif "imc" in texto:
        bot.reply_to(message, "🧮 Cálculo de IMC: Divide tu peso en kilos entre tu altura al cuadrado (m²).")
    elif "contraseña" in texto or "password" in texto:
        pwd = ''.join(random.choice("ABCDEFGH123456789!@#") for _ in range(10))
        bot.reply_to(message, f"🔒 Contraseña segura generada: `{pwd}`", parse_mode="Markdown")
    elif "cuanto es" in texto or "calcula" in texto or "+" in texto or "-" in texto or "*" in texto:
        try:
            resultado = eval(texto.replace("cuanto es", "").replace("calcula", "").strip())
            bot.reply_to(message, f"🧮 Resultado: {resultado}")
        except:
            bot.reply_to(message, f"¡Claro que sí, {nombre_actual}! Hablemos de ese cálculo.")
    else:
        if es_creador:
            bot.reply_to(message, f"👑 [Modo Jefe Activo]: Entendido, {nombre_actual}. Como mi desarrollador, anoto esto en el sistema principal. ¡Pregúntame de música, BTS, juegos, anime o educación!")
        else:
            bot.reply_to(message, f"¡Qué interesante, {nombre_actual}! Cuéntame más, mándame fotos o pídeme información detallada sobre música, BTS, videojuegos y educación física.")

print("Sofía con respuestas ampliadas y modo desarrollador en línea...")
bot.infinity_polling()
        
