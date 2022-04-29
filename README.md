# CMPE321 - Project 3 

Furkan Keskin - 2018400150 & Hatice Erk - 2018400090

## Requirements
* MySQL
* Python 

## Deployment 

First, you need to create the database in MySQL. MySQL requires you to connect with the root user and password. After connecting to server, you should run the _createTables.sql_ file in the MySQL Workbench to create the database.
Then, open _settings.py_ file under the _boundb/boundb_ folder. In the _settings.py_ file, you should enter your password.  
```
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SimpleBounDB',
        'USER': 'root',
        'PASSWORD': #yourpassword,
        'HOST': 'localhost',
    }
}
```
* After that, you should run following commands in the _boundb_ folder, which contains _manage.py_.
```
python manage.py makemigrations
python manage.py migrate
```
Finally, run the command:
```
python manage.py runserver
```
and check whether the website is accessible at: [http://127.0.0.1:8000/simpleboun/](http://127.0.0.1:8000/simpleboun/)
