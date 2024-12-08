# docker build -t trading-front:latest .
# Utiliser une image Node.js officielle comme base
FROM node:20-alpine AS build

# Définir le répertoire de travail
WORKDIR /app/
# WORKDIR /app/Front/trading_front

# Copier les fichiers de configuration du projet
COPY package*.json ./

# Installer les dépendances
RUN npm ci 
RUN npm install -g @angular/cli

# Copier tous les fichiers du projet
COPY . .

# Construire l'application pour la production
RUN npm run build --configuration=production

# Étape 2 : Utiliser NGINX pour servir les fichiers statiques
FROM nginx:alpine

# Supprimer les fichiers NGINX par défaut
RUN rm -rf /usr/share/nginx/html/*

# Copier les fichiers Angular générés dans NGINX
COPY --from=build /app/dist/trading_front /usr/share/nginx/html

# Copier la configuration personnalisée de NGINX
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Lancer NGINX
CMD ["nginx", "-g", "daemon off;"]
