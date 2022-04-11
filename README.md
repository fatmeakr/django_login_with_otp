# Requirement

* linux based os
* python >= 3.7 and pip
* postgres database

# HOW TO RUN
* clone project and cd to project directory
* create and edit `.env` file based on `sample.env`
* install requirement packages via `pip install -r requirement.txt`
* migrate database via `python manage.py migrate`
* create superuser via `python manage.py createsuperuser` to test the login.
* run server via `python manage.py runserver`
* run the celery task via `celery -A login worker -l info`
* make messages via `django-admin makemessages --all`
* comile messages via `django-admin compilemesssages`
 
