import base64
import os
import time
import requests


class PagBankClient:
    def __init__(self, client_id, client_secret, ambiente="sandbox"):
        self.client_id = (client_id or "").strip()
        self.client_secret = (client_secret or "").strip()
        self.ambiente = (ambiente or "sandbox").strip().lower()

        self._token = None
        self._token_exp = 0

    def is_configured(self):
        return bool(self.client_id and self.client_secret)

    def _base_url(self):
        return "https://sandbox.api.pagseguro.com" if self.ambiente == "sandbox" else "https://api.pagseguro.com"

    def _get_token(self):
        now = time.time()
        if self._token and now < (self._token_exp - 20):
            return self._token

        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("ascii")

        resp = requests.post(
            f"{self._base_url()}/public/oauth/token",
            headers={
                "Authorization": f"Basic {encoded}",
                "Content-Type": "application/json",
            },
            json={
                "grant_type": "client_credentials",
                "scope": "cob.read cob.write pix.read pix.write",
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        self._token = data.get("access_token")
        self._token_exp = now + int(data.get("expires_in", 3600))
        return self._token

    def create_pix_charge(
        self,
        *,
        amount,
        pix_key,
        payer_name,
        payer_cpf,
        description,
        expiration_seconds=3600,
    ):
        if not self.is_configured():
            raise RuntimeError("PagBank não configurado (client_id/client_secret ausentes)")

        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        payload = {
            "calendario": {"expiracao": int(expiration_seconds)},
            "devedor": {"cpf": str(payer_cpf or "").strip(), "nome": str(payer_name or "").strip()},
            "valor": {"original": f"{float(amount):.2f}"},
            "chave": str(pix_key or "").strip(),
            "infoAdicionais": [{"nome": "Descrição", "valor": str(description or "").strip()[:140]}],
        }

        resp = requests.post(f"{self._base_url()}/v2/cob", headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        cobranca = resp.json()
        txid = cobranca.get("txid")
        loc_id = (cobranca.get("loc") or {}).get("id")

        qr_base64 = None
        if loc_id:
            qr = requests.get(f"{self._base_url()}/v2/loc/{loc_id}/qrcode", headers=headers, timeout=30)
            qr.raise_for_status()
            qr_data = qr.json()
            qr_base64 = qr_data.get("qrcode")

        return {
            "txid": txid,
            "qr_code_base64": qr_base64,
            "pix_key": payload["chave"],
        }

    def get_charge_status(self, txid):
        if not self.is_configured():
            raise RuntimeError("PagBank não configurado (client_id/client_secret ausentes)")

        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = requests.get(f"{self._base_url()}/v2/cob/{txid}", headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return (data.get("status") or "").upper()


def client_from_env():
    return PagBankClient(
        os.environ.get("PAGBANK_CLIENT_ID"),
        os.environ.get("PAGBANK_CLIENT_SECRET"),
        os.environ.get("PAGBANK_ENV", "sandbox"),
    )

