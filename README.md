# SMS19

## Setting Up Backend

### Setup MySql

- [Please follow this tutorial and the linked articles to configure MySql Database](https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database)
  - Database Name : 'SMS19'
  - Use 'root' user

### Create a python3 virtual environment

```bash
python3 -m venv sms19-env
source env/bin/activate
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
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

### Tree Structure

.
├── manage.py
├── README.md
├── requirements.txt
├── SMS19
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── sms19-env
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    ├── pip-selfcheck.json
    └── pyvenv.cfg

### Note

- Use the root user in mysql
- Migrate after every pull from the repository
- To maintain the tree structure:

  ```bash
  sudo apt-get install tree
  tree -L 2
  ```

## Contribution

- Please raise issues if the above procedure does not work for your system.
- Feel free to make necessary changes.
- Please migrate before running the server.
