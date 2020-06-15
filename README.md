1. `git clone https://github.com/petrshirin/DatingBot.git`
2. Create file `.env` near manage.py (example in `.env.example`)
3. fill .env file some params:

```
TOKEN=TOKEN

SECRET_KEY=Add_some_key 
DEBUG=True

DB_HOST=localhost
DB_USER=postgres
DB_PASS=root
DB_NAME=lovebot
DB_PORT=5432


ENCRYPTED_COOKIE_STORAGE_KEY=Thirty  two  length  bytes  key.
```

4. change db conf in `settings.py`, if you do not have postgres server.
    `DATABASES` dict in `settings.py` change on:
    ```
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
   }
5. create venv (linux/windows: `python3 -m venv venv`) in folder with project
6. activate venv  
```
cd venv/Scripts/
activate.bat 
```

6. install req `pip install -r req.txt` \
Maybe will be a some errors fixed it or if error in lib asyncpg or psycopg2, just remove this name in `req.txt`

7. create migrations for bd `python manage.py makemigrations`
8. migrate db `python manage.py migrate`
9. create superuser(for access to admin panel) `python manage.py createsuperuser`
10. create 3 restaurants in admin panel, table `UserRestaurants`
11. start `python manage.py runserver`

datingbot \
    --aiohttp_chat - websocket chat \
    --api - app for ajax requests \
    --datingbot - project settings \
    --media - media files(user photos) \
    --static - site static(js, css, svg) \
    --userprofile - app in user logic \
    -- --management - help command \
    -- --migrations - app migrations for db \
    -- -- templates - html files \
    -- -- *.py  - server logic