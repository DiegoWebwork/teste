from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from pyngrok import ngrok
import pywhatkit as kit
import qrcode
import asyncio
import os

os.environ['DISPLAY'] = ':0'

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

def delay(t, v):
    return asyncio.sleep(t, result=v)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('connection')
def handle_connection():
    emit('message', '© BOT-ZDG - Iniciado')
    emit('qr', './icon.svg')

@app.route('/zdg-message', methods=['POST'])
def send_message():
    number = request.form.get("number")
    message = request.form.get("message")

    if not number or not message:
        return jsonify({
            "status": False,
            "message": "Número e mensagem são necessários."
        }), 422

    numberDDI = number[:2]
    numberDDD = number[2:4]
    numberUser = number[-8:]

    if numberDDI != "55":
        numberZDG = f"{number}@c.us"
        
        try:
            kit.sendwhatmsg_instantly(numberZDG, message)
            return jsonify({
                "status": True,
                "message": "BOT-ZDG Mensagem enviada"
            }), 200
        except Exception as e:
            return jsonify({
                "status": False,
                "message": "BOT-ZDG Mensagem não enviada",
                "response": str(e)
            }), 500

    elif numberDDI == "55" and int(numberDDD) <= 30:
        numberZDG = f"55{numberDDD}9{numberUser}@c.us"
        
        try:
            kit.sendwhatmsg_instantly(numberZDG, message)
            return jsonify({
                "status": True,
                "message": "BOT-ZDG Mensagem enviada"
            }), 200
        except Exception as e:
            return jsonify({
                "status": False,
                "message": "BOT-ZDG Mensagem não enviada",
                "response": str(e)
            }), 500

if __name__ == '__main__':
    socketio.run(app)
