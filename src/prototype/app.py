from flask import Flask, request
import requests

TOKEN_API = '639642745:AAHd9aIHomuZZH7-pxJPRpWAAdMjF4vHRWc'

app = Flask(__name__)

# chat_id = request.json["message"]["chat"]["id"]

def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TOKEN_API}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
        chat_id = request.json["message"]["chat"]["id"]
        send_message(chat_id, "pong")
    return {"ok": True}

# @app.route('/', methods=["POST"])
# def process():  # put application's code here
#     print(request.json)
#     return {"ok": True}

# if __name__ == '__main__':
#     app.run()
