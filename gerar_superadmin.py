import argparse
import secrets
import string

from web_access_db import init_db, ensure_superadmin


def gerar_senha(tamanho=16):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(int(tamanho)))


def main():
    parser = argparse.ArgumentParser(description="Cria/atualiza o usuário superadmin (criador) no acesso_web.db.")
    parser.add_argument("--email", required=True, help="Email do criador (superadmin)")
    parser.add_argument("--senha", help="Senha do criador. Se omitida, gera uma senha aleatória.")
    args = parser.parse_args()

    senha = args.senha or gerar_senha()
    init_db()
    ensure_superadmin(args.email, senha)

    print("Superadmin configurado:")
    print(f"Email: {args.email}")
    print(f"Senha: {senha}")


if __name__ == "__main__":
    main()

