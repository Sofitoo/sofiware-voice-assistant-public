from flask import Flask, render_template, request, jsonify
from assistant import procesar_texto

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/comando", methods=["POST"])
def comando():
    texto = request.json.get("texto")
    respuesta = procesar_texto(texto)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True)
