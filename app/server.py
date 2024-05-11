import os
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Request, Response
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from redis import Redis
from rq import Queue
from Secweb import SecWeb

REDIS_URL = os.getenv("REDIS_URL")

bot_queue = Queue(connection=Redis.from_url(REDIS_URL))
redis: Redis = None

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

SecWeb(app=app)


@app.post("/visit")
@limiter.limit("6/minute")
async def visit(url: Annotated[str, Form()], request: Request):
    bot_queue.enqueue("bot.visit", url)
    return {"success": True}


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=80, proxy_headers=True, forwarded_allow_ips="*"
    )
