FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python manage.py collectstatic --noinput; \ 
    python manage.py runserver 0.0.0.0:8000
