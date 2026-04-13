#!/usr/bin/env python3
import sys
import os
import subprocess
import webbrowser
import time
import threading

def start_flask():
    """Inicia Flask (app.py)"""
    try:
        subprocess.Popen([sys.executable, "app.py"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
    except:
        pass

# 1. Inicia Flask em background
print("Iniciando aplicação...")
start_thread = threading.Thread(target=start_flask, daemon=True)
start_thread.start()

# 2. Aguarda Flask iniciar
time.sleep(3)

# 3. Abre navegador automaticamente
try:
    webbrowser.open("http://localhost:5000")
except:
    pass

# 4. Mantém rodando
print("Sistema aberto no navegador!")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)
