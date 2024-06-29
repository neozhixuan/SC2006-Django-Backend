# SC2006-Django-Backend
![image](https://github.com/neozhixuan/SC2006-Django-Backend/assets/79783660/dea62639-38f9-44c5-9767-fa7161ab0316)

## Project Scope
This is the backend of our Software Engineering project, which utilises Django's own ORM to model the relations between our different entities and serialise the models, to serve a RESTful API. Data is pulled into the backend using a Data Access Object (DAO) before serving it with business layer logic.

## Initialise Project
1. `pip install -r requirements.txt`
2. `cd backendProject`
3. Get the sqlite file from @neozhixuan
4. Navigate to `apps.py` and comment out every line of `update_model_from_firebase()`
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. Navigate to `apps.py` and uncomment every line of `update_model_from_firebase()`
8. Optional: `python manage.py createsuperuser` to create your own user
9. `python manage.py runserver`

## Navigation
When you have started http://127.0.0.1:8000/, you can navigate around:
1. http://127.0.0.1:8000/admin/ and login to your user
2. http://127.0.0.1:8000/api/orderdata/

