FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
# RUN mkdir -p /data && chmod 777 /data
RUN python manage.py collectstatic --noinput
ENV MY_ENV=netology_4_11
#EXPOSE 8000
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "warehouse_api.wsgi:application"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
