import os
import random
import telebot

TOKEN = "8993633836:AAGJJHm9_3bSksfglYXs_T_vveLU8ny1h9I"
bot = telebot.TeleBot(TOKEN)
user_states = {}

CREATOR_NAME = "abdallah"  # Tu nombre como desarrollador

# --- BANCOS DE DATOS ---
adivinanzas = [
    "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera. ¿Qué es? (La pera)",
    "Oro parece, plata no es. Quien no lo adivine, bien tonto es. ¿Qué es? (El plátano)"
]

chistes = [
    "¿Qué hace una abeja en el gimnasio? ¡Zumba!",
    "— Hola, ¿está Agustín? — No, estoy incomodísimo."
]

ejercicios = [
    "🏋️‍♂️ **Reto Exprés:** ¡Haz 15 sentadillas o estira las piernas!",
    "🧘‍♂️ **Pausa Activa:** Respira hondo durante 30 segundos y relaja los hombros."
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
    
    # Paso 1: Capturar nombre y verificar si eres el desarrollador
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

    # --- RESPUESTAS NATURALES Y COMPLETAS ---
    if "chiste" in texto or "broma" in texto:
        bot.reply_to(message, f"🤣 ¡Claro que sí! Aquí te va uno:\n\n{random.choice(chistes)}")
        
    elif "anime" in texto or "dragon ball" in texto or "naruto" in texto:
        bot.reply_to(message, 
            "🎌 **¡Hablemos de anime!** Es un mundo increíble. Desde clásicos legendarios como Dragon Ball hasta historias modernas llenas de acción y emoción.\n\n"
            "¿Cuál es tu serie favorita? Dime cuál te gusta y comentamos sobre sus personajes y peleas épicas."
        )
        
    elif "bts" in texto or "kpop" in texto or "musica" in texto or "cancion" in texto:
        bot.reply_to(message, 
            "💜 **¡La música y BTS son geniales!**\n\n"
            "• **BTS:** Está compuesto por RM, Jin, Suga, J-Hope, Jimin, V y Jungkook, y tienen canciones increíbles.\n"
            "• **Fotos:** Me encanta cuando me mandas fotos de ellos por aquí para verlas.\n"
            "• **Estilos:** Ya sea que busques algo para relajarte programando o energía para entrenar, ¡siempre hay un buen tema para cada momento!"
        )
        
    elif "ejercicio" in texto or "rutina" in texto or "deporte" in texto:
        bot.reply_to(message, 
            "💪 **¡Actívate con Sofía!**\n\n"
            f"{random.choice(ejercicios)}\n\n"
            "Mantenerse activo ayuda a despejar la mente, especialmente cuando pasamos mucho rato programando frente a la pantalla."
        )
        
    elif "adivinanza" in texto or "acertijo" in texto:
        bot.reply_to(message, f"🧩 A ver si adivinas esta:\n\n{random.choice(adivinanzas)}")
        
    else:
        if es_creador:
            bot.reply_to(message, f"👑 [Modo Jefe Activo]: Entendido perfectamente, {nombre_actual}. Como mi desarrollador, anoto cada detalle en el sistema principal para seguir mejorando la conversación.")
        else:
            bot.reply_to(message, f"¡Qué interesante lo que me cuentas, {nombre_actual}! Me encanta conversar contigo sobre esto. Cuéntame más detalles o pídeme un chiste, un dato de anime o música.")

print("Sofía con respuestas naturales y modo creador lista en la nube...")
bot.infinity_polling()
