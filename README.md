# Event Management System Back-end 
A simple event management system.

## Project support features
- Users can sign up and login into their accounts
- Users can change their account passwords
- Authenticated users can access all events and mark as an attendee to a specific event.
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
   
## API endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | event-management-system/api/auth/account/login | To login to an existing account |
| POST | event-management-system/api/auth/account/register | To create a new user account |
| POST | event-management-system/api/auth/account/logout | To logout of a logged in account |
| POST | event-management-system/api/auth/account/password_change | To change password of a specific account |
| POST | event-management-system/api/category | To add new event categories |
| POST | event-management-system/api/speaker | To create a speaker for an event |
| POST | event-management-system/api/events | To create a new event |
| POST | event-management-system/api/event/attendee | while logged in sign up as an attendee to an event |

### Technologies Used
* [Django](https://www.djangoproject.com/) A pyhton web framework that enables rapid development Aand clean, pragmatic design
* [Django Rest Framework](https://www.django-rest-framework.org/) A powerful and flexible toolkit for building web APIs
* [SQLiteDB](https://www.sqlitedb.com/) A lightweight SQL based database.

### Authors
* [Michael Wekesa](https://github.com/wekesa360)
