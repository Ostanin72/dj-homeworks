FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
# RUN mkdir -p /data && chmod 777 /data
RUN python manage.py collectstatic --noinput

# Создаем пользователя для запуска приложения (не root)
RUN adduser --uid 1000 --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

#EXPOSE 8000
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "warehouse_api.wsgi:application"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
