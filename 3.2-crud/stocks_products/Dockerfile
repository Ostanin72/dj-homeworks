FROM python:3.12
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV MY_ENV=netology_4_11

CMD ["python3", "manage.py", "runserver"]

