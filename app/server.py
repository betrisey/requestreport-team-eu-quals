import os
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Response
from fastapi.staticfiles import StaticFiles
from redis import Redis
from rq import Queue
from Secweb import SecWeb

REDIS_URL = os.getenv("REDIS_URL")

bot_queue = Queue(connection=Redis.from_url(REDIS_URL))
redis: Redis = None

app = FastAPI()

SecWeb(app=app)


# TODO remove, only for testing
@app.get("/alt-svc")
async def alt_svc(host: str, response: Response):
    response.headers["Alt-Svc"] = f'h2="{host}"; ma=15'
    return {"success": True}


@app.post("/visit")
async def visit(url: Annotated[str, Form()]):
    bot_queue.enqueue("bot.visit", url)
    return {"success": True}


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=80, proxy_headers=True, forwarded_allow_ips="*"
    )
