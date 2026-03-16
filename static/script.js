//estados globales

let voces = [];
let escuchando = false;
let hablando = false;


// Configuración del reconocimiento de voz
const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "es-AR";
recognition.continuous = false;
recognition.interimResults = false;

//carga de voces del navegador

speechSynthesis.onvoiceschanged = () => {
    voces = speechSynthesis.getVoices();
};

//  Voz del navegador se cambia a laura incluye la solucion del bucle
function hablar(texto) {
    if (hablando) {
        window.speechSynthesis.cancel();
        hablando = false;
    }

    const speech = new SpeechSynthesisUtterance(texto);

    const laura = voces.find(
        (v) => v.name.includes("Laura") && v.lang.startsWith("es")
    );

    if (laura) speech.voice = laura;

    speech.lang = "es-ES";
    speech.rate = 1;
    speech.pitch = 1;

    hablando = true;

    speech.onend = () => {
        hablando = false;
    };

    window.speechSynthesis.speak(speech);
}



// 🎤 Escuchar micrófono
function escucharMicrofono() {
    const micBtn = document.getElementById("mic-btn");

    // 🛑 si está hablando, cortar voz
    if (hablando) {
        window.speechSynthesis.cancel();
        hablando = false;
    }

    // 🔁 si ya está escuchando, detener
    if (escuchando) {
        recognition.stop();
        escuchando = false;
        micBtn.classList.remove("animate-pulse");
        document.getElementById("respuesta").innerText = "⏹️ Escucha detenida";
        return;
    }

    // ▶️ empezar a escuchar
    escuchando = true;
    micBtn.classList.add("animate-pulse");
    document.getElementById("respuesta").innerText = "🎧 Escuchando...";
    recognition.start();
}


recognition.onresult = function (event) {
    const texto = event.results[0][0].transcript;
    document.getElementById("texto").value = texto;
    escuchando=false;
    enviarTexto(texto);
};

recognition.onerror = function () {
    document.getElementById("respuesta").innerText = "❌ No pude escucharte";
    document.getElementById("mic-btn").classList.remove("animate-pulse");
};

recognition.onend = function () {
    document.getElementById("mic-btn").classList.remove("animate-pulse");
};

// ✍️ Enviar texto (input o mic)
function enviar() {
    const texto = document.getElementById("texto").value;
    if (texto.trim() !== "") {
        enviarTexto(texto);
    }
}

function enviarTexto(texto) {
    fetch("/comando", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto }),
    })
        .then((res) => res.json())
        .then((data) => {
            document.getElementById("respuesta").innerText =
                "🤖 " + data.respuesta;

            hablar(data.respuesta);
        });
}

