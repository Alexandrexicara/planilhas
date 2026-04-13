#!/usr/bin/env python3
import subprocess, webbrowser, time, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.Popen([sys.executable, "app.py"])
time.sleep(3)
webbrowser.open("http://localhost:5000")
while True:
    time.sleep(1)
