#!/usr/bin/env python3
import subprocess, webbrowser, time, sys, os

# Inicia Flask SEM thread (blocking)
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

exe_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(exe_dir, "app.py")

# Abre navegador PRIMEIRO  (não bloqueia)
try:
    webbrowser.open("http://localhost:5000", new=1)
except:
    pass

# Aguarda Flask estar pronto
time.sleep(2)

#  Executa Flask (bloqueia aqui)
try:
    subprocess.Popen([sys.executable, app_path], cwd=exe_dir)
    
    # Mantém processo rodando
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(f"Erro: {e}")
    sys.exit(1)
