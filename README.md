# SMS19

## ToDo

- Templates Integration
  - Buy/Sell Testing
- Markets
- Leaderboard
- User Portfolio Page
- Stock History Page
- News Section
- Algorithm for Price Fluctuation

## Setting Up Backend

### Setup PostgreSQL

- [Please follow this tutorial and the linked articles to configure PostgreSQL Database](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)
  - Database Name : 'sms19'
  - User: 'sms19admin'
  - Password: 'password'

### Create a python3 virtual environment

```bash
python3 -m venv sms19-env
source env/bin/activate
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py makemigrations main
python manage.py migrate
python manage.py migrate main
```

### Create a superuser for Django

```bash
python manage.py createsuperuser
```

### Run the server

```bash
python manage.py runserver 0.0.0.0:8000
```

### Verify that the Server being used is MySql

```bash
./manage.py shell
>>> from django.db import connection
>>> connection.vendor
```

### Setting Up Social media login

- first create a django superuser using following command

```bash
python manage.py createsuperuser
```

- Go to <http://localhost:8000/admin/socialaccount/socialapp/> and add a new social application
  - Provider : Google
  - Name : google
  - Client id : 637432237961-3r7lhv7o0e11n3mv3atekpk46t8ahib4.apps.googleusercontent.com
  - secret key : xb8yqnj_c8sAjFsITSEt6FR4
  - sites : choose both 127.0.0.1 and example.com

- If you don't get an option for '127.0.0.1' in the sites field
  - Go to <http://localhost:8000/admin/sites/site/add/> and fill following fields and save . Then again proceed to add a social application .
    - Domain name : 127.0.0.1
    - Display name : 127.0.0.1

### Note

- Migrate after every pull from the repository

## Contribution

- Please raise issues if the above procedure does not work for your system.
- Feel free to make necessary changes.
- Please migrate before running the server.

## References for allauth

- Settings : <https://django-allauth.readthedocs.io/en/latest/configuration.html>
- adapters.py <https://stackoverflow.com/questions/27759407/django-allauth-redirect-after-social-signup>
- migration changes <https://stackoverflow.com/questions/29902366/django-migration-is-not-applying-the-migration-changes>
