# Analisis-tweets-CMU-ESPOL
Análisis de tweets en las revueltas ocurridas en Latinoamérica a finales del 2019.

## Requisitos
* Python: 3.7.3
* Django: 2.2.4
* Environ: pip install django-environ
* Agregar el .env en /analisistweets

## Perform backups
1. Connect to server
2. Backup :
```
cd CMU_backups
mysqldump -u [DB_USER] -p[DB_PASS] --no-tablespaces [DB_NAME] > [filename].sql
```

## Development workflow
1. Start python virtual environment.
2. Set environment variables :
```
SECRET_KEY=<secret>
DJANGO_SETTINGS_MODULE=analisistweets.settings_dev
```
3. Change directory and start app :
```
cd web_app
python manage.py runserver
```

## Seed DB
```
python manage.py loaddata fixtures/annotators.yaml
python manage.py loaddata fixtures/tweets.yaml
python manage.py loaddata fixtures/questions.yaml
python manage.py loaddata fixtures/annotations.yaml
```

## Run tests
```
python manage.py test # All tests

python manage.py test analisis.tests.ProblematicTweetRelation # Specific tests
```

## Run app
```
# Start app
sudo docker-compose up

# To run bash in web_app
sudo docker-compose run web_app bash

sudo docker-compose run web_app python manage.py makemigrations
sudo docker-compose run web_app python manage.py migrate

# To re-build web app after modify /web_app
sudo docker-compose build web_app
```
