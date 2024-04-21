FROM mcr.microsoft.com/playwright/python:jammy

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY bot.py /app/bot.py

CMD rq worker --with-scheduler --url $REDIS_URL
