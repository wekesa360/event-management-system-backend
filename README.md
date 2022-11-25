# Event Management System (in Django)

## Installation

1) Create a ```virtual environment``` 
2) Install all requirements in the ```requirements.txt``` file
   
   ```python
   pip install -r requirements.txt
   ```
3) Set up all the environmnet variables ina ```.ENV``` file in the base directory
   ##### The Environment Variables

   ```
    SECRET_KEY = 'some random string'
    EMAIL_PORT=587
    EMAIL_USE_TLS = True
    EMAIL_HOST='Smtp-mail.outlook.com'
    EMAIL_HOST_USER='your-email@outlook.com'
    EMAIL_HOST_PASSWORD='your email password'
    ```

4) Run ```python python manage.py makemigrations```, followed by ```python python manage.py migrate```
5) Create a superuser, for logging into the admin panel with: ```python python manage.py createsuperuser```
6) Finally; run ```python python manage.py runserver```