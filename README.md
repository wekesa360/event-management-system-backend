# Event Management System (in Django)

## Installation

1) Create a ```virtual environment``` 
2) Install all requirements in the ```requirements.txt``` file
   
   ```python
   pip install -r requirements.txt
   ```
3) Set up all the environmnet variables in a ```.ENV``` file in the base directory
   ##### The Environment Variables

   ```
    SECRET_KEY = 'some random string'
    
    ```

4) Run 
    ```python 
    python manage.py makemigrations
    ```
    followed by 
    ```python 
    python manage.py migrate
    ```
5) Create a superuser, for logging into the admin panel with: 
   ```python
   python manage.py createsuperuser
   ```
6) Finally run; 
   ```python
    python manage.py runserver
    ```