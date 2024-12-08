# docker build -t trading-back:latest .
# docker images
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app/Back/trading_back_v2

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier seulement le requirements.txt d'abord
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier tout le code du dossier Back/trading_back_v2
COPY . .