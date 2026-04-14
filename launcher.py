#!/usr/bin/env python3
import subprocess, webbrowser, time, sys, os, threading
import atexit

exe_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
app_script = os.path.join(exe_dir, "app.py")

proc = None

def start_flask():
    global proc
    try:
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        env['FLASK_DEBUG'] = '0'
        env['WERKZEUG_RUN_MAIN'] = 'true'
        
        proc = subprocess.Popen([sys.executable, app_script], 
                               cwd=exe_dir,
                               env=env,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL,
                               creationflags=0x08000000)
    except Exception as e:
        print(f"Erro ao iniciar app: {e}")

def on_exit():
    if proc:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except:
            pass

atexit.register(on_exit)

start_flask()
time.sleep(4)

try:
    webbrowser.open("http://localhost:5000")
except:
    pass

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
