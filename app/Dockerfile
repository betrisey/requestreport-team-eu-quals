FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install rust and gcc
RUN apt-get update && apt-get install -y curl gnupg && rm -rf /var/lib/apt/lists/*

# Install yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install yarn requirements
COPY frontend/package.json frontend/yarn.lock /app/frontend/
RUN cd frontend && yarn install --frozen-lockfile

# Install pip requirements
COPY requirements.txt /app/
RUN python -m pip install -r requirements.txt

# Build the frontend
COPY frontend /app/frontend/
RUN cd frontend && yarn parcel build --dist-dir ../static --public-url /app/ src/index.html

COPY server.py /app/

EXPOSE 80

CMD ["python", "server.py"]
