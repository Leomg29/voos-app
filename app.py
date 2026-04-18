from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Sistema pronto! Rode o app web depois."
