# Analisis-tweets-CMU-ESPOL
Aplicación web para realizar anotaciones y análisis de tweets en las revueltas ocurridas en Latinoamérica a finales del 2019.


## Set dev environment with Docker

```
# to build the webapp img
sudo docker compose build web_app
 
# set up services locally
sudo docker compose up

# with services running, apply initial migration
sudo docker compose exec web_app python manage.py makemigrations
sudo docker compose exec web_app python manage.py migrate
```

Now we need a dump of db, from the server :
```
python manage.py dumpdata --exclude contenttypes -o <date>_backup.json
```

Then, place the file in the web_app/data folder locally.

Then, with the service running, load the data:
```
sudo docker compose exec web_app python manage.py loaddata ./data/<date>_backup.json
```
Now reload page to see changes.


## Perform backups in server
1. Connect to server
2. Backup :
```
cd CMU_backups
mysqldump -u [DB_USER] -p[DB_PASS] --no-tablespaces [DB_NAME] > [filename].sql
```


## Run tests
```
python manage.py test # All tests

python manage.py test analisis.tests.ProblematicTweetRelation # Specific tests
```
