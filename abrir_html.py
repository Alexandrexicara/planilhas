#!/usr/bin/env python3
"""
Script para abrir o arquivo HTML no navegador
"""
import webbrowser
import os

def main():
    html_file = "SISTEMA_PLUS.html"
    
    if os.path.exists(html_file):
        print(f"🚀 Abrindo {html_file} no navegador...")
        webbrowser.open(f'file://{os.path.abspath(html_file)}')
        print("✅ Sistema aberto no navegador!")
    else:
        print(f"❌ Arquivo {html_file} não encontrado!")

if __name__ == "__main__":
    main()
