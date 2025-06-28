# Многоэтапная сборка для оптимизации размера образа

# Этап 1: Сборка приложения
FROM node:18-alpine as build

# Рабочая директория в контейнере
WORKDIR /app

# Копируем файлы конфигурации для установки зависимостей
COPY package*.json ./
COPY tsconfig.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Устанавливаем зависимости
RUN npm ci --only=production

# Копируем исходный код
COPY public/ ./public/
COPY src/ ./src/

# Собираем продакшен версию
RUN npm run build

# Этап 2: Nginx для раздачи статики
FROM nginx:alpine

# Копируем собранное приложение
COPY --from=build /app/build /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Экспонируем порт
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"] 