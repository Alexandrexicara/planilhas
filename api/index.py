import sys
from pathlib import Path

# Garante que o diretorio raiz do projeto esteja no sys.path no ambiente serverless.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app as flask_app

# Ponto de entrada WSGI esperado pela runtime Python da Vercel.
app = flask_app
