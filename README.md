# Analisis-tweets-CMU-ESPOL
Aplicación web para realizar anotaciones y análisis de tweets en las revueltas ocurridas en Latinoamérica a finales del 2019.


## Set dev environment with Docker

```
# to build the webapp img
docker compose build web_app
 
# set up services locally
docker compose up

# with services running, apply initial migration
docker compose exec web_app python manage.py makemigrations
docker compose exec web_app python manage.py migrate

# create superuser to work with app locally
docker-compose exec web_app python manage.py createsuperuser

# seed db
docker-compose exec web_app python script_populate.py
```

## Run tests
```
python manage.py test # All tests

python manage.py test analisis.tests.ProblematicTweetRelation # Specific tests
```
