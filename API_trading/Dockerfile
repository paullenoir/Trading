# docker build -t trading-api:latest .
# docker images
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app/API_trading

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier seulement le requirements.txt d'abord
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier tout le code du dossier /app/API_trading
COPY . .

# Commande d'entrée par défaut
CMD ["sh", "-c", " python manage.py runserver 0.0.0.0:8001"]