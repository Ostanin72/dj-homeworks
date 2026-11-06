# stocks_products (Склады и запасы)

REST API для управления складами и номенклатурой. Проект упакован в Docker-контейнер и использует SQLite3.

## Технологии
- Python 3.12
- Django 6.1.3
- Django REST Framework
- SQLite3
- Docker

## Быстрый запуск

Убедитесь, что у вас установлены [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

### 1. Сборка образа
```bash
docker build -t stocks_products .

### 2. Подготовка базы данных (миграции)
docker run --rm -v "$(pwd)/data":/data stocks_products python manage.py migrate

### 3. Запуск  сервера
```bash
docker run -d -p 8000:8000 -v "$(pwd)/data":/data --name stocks_products stocks_productsocker build -t stocks_products .

### 4. Проверка доступности сервера
'''bash
curl localhost:8000