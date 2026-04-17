#!/usr/bin/env python3
"""
Teste simples para isolar o problema do gunicorn
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "App funcionando!"

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
