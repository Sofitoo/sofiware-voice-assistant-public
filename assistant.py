import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import wikipedia
wikipedia.set_lang("es") # configuracion Wikipedia en español
from dotenv import load_dotenv
load_dotenv()

#IMPLEMENTACION DE IA

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
IA_DISPONIBLE = False #cambiar a True si se quiere usar IA

#INTENCIONES PARA SOFIWARE

INTENCIONES = {
    "hora": {
        "keywords": ["hora", "horario", "hora actual"],
        "accion": "hora"
    },
    "google": {
        "keywords": ["google", "buscador", "buscar", "navegador"],
        "accion": "abrir_google"
    },
    "youtube": {
        "keywords": ["youtube", "YouTube", "videos", "ver videos"],
        "accion": "abrir_youtube"
    },
    "nota": {
    "keywords": ["tomar nota", "anotar", "dictado", "nota", "guardar nota", "anotame","anótame","gurdame", "toma nota"],
    "accion": "guardar_nota"
}
}

#RESPUESTAS DE SOFIWARE SI NO ENTENDIO
RESPUESTAS_DESCONOCIDAS = [
    "No entendí del todo, ¿podés repetir?",
    "Todavía estoy aprendiendo eso 😊",
    "¿Podés decirlo de otra forma?"
]

#VOZ EN ESPAÑOL

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty(
    'voice',
    r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
)

WAKE_WORDS = ["sofi", "sofia"]

def hablar(texto):
    print(f"🤖 SofiWare: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Escuchando...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            texto = recognizer.recognize_google(audio, language="es-ES")
            print(f"🗣️ Dijiste: {texto}")
            return texto.lower()
        except sr.WaitTimeoutError:
            # No se escuchó nada
            return ""
        except sr.UnknownValueError:
            hablar("No te entendí bien")
            return ""
        except sr.RequestError:
            hablar("Error con el servicio de reconocimiento")
            return ""


def ejecutar_comando(texto):
    accion = detectar_intencion(texto)
    respuesta = None

    if accion == "hora":
        hora = datetime.datetime.now().strftime("%H:%M")
        respuesta = f"Son las {hora}"

    elif accion == "abrir_google":
        webbrowser.open("https://www.google.com")
        respuesta = "Abriendo Google"

    elif accion == "abrir_youtube":
        webbrowser.open("https://www.youtube.com")
        respuesta = "Abriendo YouTube"

    elif accion == "guardar_nota":
        guardar_nota(texto)
        respuesta="Listo, ya lo anoté 📝"

    elif "salir" in texto:
        respuesta="Hasta luego"
        hablar(respuesta)
        exit()

    #else:
    #  respuesta = responder_con_ia(texto) <- COMENTADO PARA EVITAR CONFLICTOS (IA NIVEL 2 )

    else:
        respuesta = responder_basico(texto)

    if respuesta:
        hablar(respuesta)
    else:
        hablar(random.choice(RESPUESTAS_DESCONOCIDAS))


def main():
    hablar("SofiWare iniciado. Dime Sofi para activarme.")

    while True:
        texto = escuchar()

        if texto == "": #<- si no escucha no finaliza el ciclo
            continue

        if any(wake in texto for wake in WAKE_WORDS):
            hablar("Sí, te escucho")

            for wake in WAKE_WORDS:
                texto = texto.replace(wake, "")

            comando = texto.strip()

            if comando:
                ejecutar_comando(comando)

if __name__ == "__main__":
    main()

#funcion para el navegador
def procesar_texto(texto):
    accion = detectar_intencion(texto)

    if accion == "hora":
        hora = datetime.datetime.now().strftime("%H:%M")
        return f"Son las {hora}"

    elif accion == "abrir_google":
        webbrowser.open("https://www.google.com")
        return "Abriendo Google"

    elif accion == "abrir_youtube":
        webbrowser.open("https://www.youtube.com")
        return "Abriendo YouTube"
    
    elif accion == "guardar_nota":
        guardar_nota(texto, hablar_python=False)
        return "Listo, ya lo anoté 📝"
    
    #elif accion is None:
    #    respuesta = responder_con_ia(texto)   <-- COMENTADO PARA EVITAR CONFLICTOS (IA NIVEL 2 )
    #    hablar(respuesta)

    elif accion is None:          #<-IA FALSA WIKIPEDIA
        return responder(texto)

    elif "buscar" in texto:
        return "buscar"

    elif "salir" in texto:
        return "Chau"

    else:
        respuesta_ia(texto)

    

        
#FUNCION PARA LAS INTENCIONES
def detectar_intencion(texto):
    for intencion, data in INTENCIONES.items():
        for palabra in data["keywords"]:
            if palabra in texto:
                return data["accion"]
    return None

#FUNCION PARA GUARDAR NOTAS
def guardar_nota(texto, hablar_python=True):
    frases_inicio = [
        "tomar nota", "anotar","anotá","anóta", "dictado", "nota", "guardar nota", "anotame","gurdame", "toma nota"
    ]

    nota = ""

    for frase in frases_inicio:
        if frase in texto:
            nota = texto.split(frase, 1)[1].strip()
            break

    if nota == "":
        if hablar_python:
            hablar("¿Qué querés que anote?")
        return

    with open("notas_sofiware.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"- {nota}\n")

    if hablar_python:
        hablar("Listo, ya lo anoté 📝")
        os.system("notepad notas_sofiware.txt")

#IMPLEMENTACION DE IA NIVEL 1

def respuesta_ia(texto):
    return f"No sé hacer eso todavía, pero entendí que dijiste: '{texto}'"

#FUNCION PARA LA IMPLEMENTACION DE LA IA NIVEL 2

def responder_con_ia(texto):
    try:
       respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sos un asistente virtual llamado Sofi, amable y claro."},
            {"role": "user", "content": texto}
        ]
      )
       return respuesta.choices[0].message.content
    
    except Exception as e:
        print("⚠️ Error IA:", e)
        return "Todavía no puedo responder eso, pero estoy aprendiendo 🤍"

#FUNCION DE BUSCAR EN GOOGLE CON IA

def buscar_en_google(texto):
    query = texto.replace("buscar", "").strip()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    hablar(f"Buscando {query} en Google")

#FUNCION PARA RESPONDER CON IA CUANDO TENGA CARGA
def responder(texto):
    if IA_DISPONIBLE:
        return responder_con_ia(texto)
    else:
        return responder_basico(texto)
    
#FUNCION PARA LIMPAR LAS PREGUNTAS PARA EVITAR CONFLICTOS

def limpiar_pregunta(texto):
    texto = texto.lower()

    disparadores = [
        "sofi",
        "sofía",
        "sophie",
        "quién fue",
        "quien fue",
        "qué es",
        "que es"
    ]

    for d in disparadores:
        texto = texto.replace(d, "")

    return texto.strip()

#FUNCION DE LA IA FALSA CON WIKIPEDIA
def responder_basico(texto):
    
    try:
         consulta = limpiar_pregunta(texto)
         resumen = wikipedia.summary(consulta, sentences=2)
         return resumen
    except wikipedia.DisambiguationError as e:
        return f"Encontré varias opciones sobre eso: {e.options[:3]}"
    except wikipedia.PageError:
        return "No encontré información clara sobre eso 🤍"
    except Exception:
        return "Algo salió mal buscando la información 😕"



