# Paragraph-Search Using Django

- Tech Used: Django, Djangorestframework, PostgreSQL
- Formatter User: black 24.3.0

## How to run locally
### Using Virtualenv
1. Clone this repo: `git clone https://github.com/adhi85/paragraph-search-django.git`
2. `cd paragraph-search-django`
3. `virtualenv myenv`
4. `myenv\Scripts\activate`
5. Create a .env file and refer the `.env.example` to fill the database details.
6. `python -m pip install requirements.txt`
7. `python manage.py runserver`
8. The APIs are available [here](http://localhost:8000/api)
9. The swagger docs can be accessed [here](http://localhost:8000/api/swagger/)

### Using Docker
1. Clone this repo: `git clone https://github.com/adhi85/paragraph-search-django.git`
2. `cd paragraph-search-django`
3. Create a .env file and refer the `.env.example` to fill the database details.
4. `docker build -t paragraph .`
5. `docker run -p 8000:8000 paragraph:latest`
6. The APIs are available [here](http://localhost:8000/api)
7. The swagger docs can be accessed [here](http://localhost:8000/api/swagger/)

## API Endpoints
### PREFIX: /api
### Token Generate
*POST*: "token/" 
BODY: 
```
{  
  "email": "user@email.com",  
  "password": "user"  
}  
```
RESPONSE:
```
{
  "refresh": "<Refresh-token>",
  "access": "<Access-Token>"
}
```
### Create User
*POST*: "create-user/"
BODY:
```
{
  "name": "user",
  "email": "user@email.com",
  "password": "user",
  "dob": "1990-2-2"
}
```
RESPONSE: 
```
{
  "id": 1,
  "email": "user@email.com",
  "name": "user",
  "dob": "1990-02-02",
  "created_at": "2024-03-30T16:36:12.335566Z",
  "modified_at": "2024-03-30T16:36:12.335566Z",
  "is_active": true,
  "is_staff": false
}
```

### Create Paragraph
*POST*: "paras/"
BODY:
```
{
  "para": "Sample paragraph \n\n This is another paragraph \n\n This contains word MARKABLE."
}
```
RESPONSE:`None`  
STATUS CODE: HTTP_201_CREATED)

### Search Word
*GET*: "search/\<str:word>\/"
BODY: `NONE`  
RESPONSE: 
```
{
  "paras": {
    "Paragraph-1": "<1st Paragraph>",
    "Paragraph-2": "<2nd Paragraph>",
    "Paragraph-3": "3rd Paragraph"
  }
}
```



