FROM nginx:latest

RUN mkdir -p /app/staticfiles

# Копируем конфиг Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# Открываем HTTP-порт
EXPOSE 80
