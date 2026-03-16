# 🤖 SofiWare - Voice Assistant

**SofiWare** is a simple experimental voice assistant built with **Python** that listens to user commands and responds using voice and basic actions.
The assistant can recognize Spanish speech, execute simple commands, and retrieve information.

This project was created as an experiment with **voice interfaces, speech recognition, and automation**.

---

## 🧠 Features

* 🎙️ **Voice activation keyword** ("Sofi")
* 🗣️ **Speech recognition in Spanish**
* 🔊 **Voice responses**
* ⚡ Basic command execution:

  * Show current time
  * Open Google
  * Open YouTube
* 📝 Note-taking feature (notes saved to a file)
* 🌐 Optional web interface

---

## 🛠️ Technologies Used

* **Python**
* `speech_recognition`
* `pyttsx3`
* `PyAudio`
* **Flask** (for the web interface)

---

## 📂 Project Structure

```
sofiware-voice-assistant
│
├── assistant.py        # Main voice assistant
├── web_app.py          # Web interface
├── requirements.txt    # Python dependencies
│
├── templates
│   └── index.html
│
├── static
│   └── script.js
│
└── README.md
```

---

## ▶️ How to Run

### 1️⃣ Activate the virtual environment

PowerShell / Bash:

```
.\venv\Scripts\Activate
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Run the assistant

Voice assistant only:

```
python assistant.py
```

Web interface:

```
python web_app.py
```

---

## ⚠️ Project Status

🚧 **Work in Progress**

This project is an experimental prototype created to explore **voice assistants and speech processing in Python**.

Future improvements may include:

* Better natural language understanding
* More commands and integrations
* AI-based responses
* Improved UI for the web interface

---

## 👩‍💻 Author

Developed by **Sofía Olariaga**.
