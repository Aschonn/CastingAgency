### Heroku Link
https://casting4561.herokuapp.com

### Motivation

This is the last project of the Udacity-Full-Stack-Nanodegree Course. It covers following technical topics in 1 app:

- Database modeling with postgres & sqlalchemy (see models.py)
- API to performance CRUD Operations on database with Flask (see app.py)
- Automated testing with Unittest (see test_app)
- Authorization & Role based Authentification with Auth0 (see auth.py)
- Deployment on Heroku


### Setup Auth0
Setup Auth0

1) Create a new Auth0 Account
    Select a unique tenant domain
    Create a new, single page web application
2) Create a new API
    in API Settings:
        Enable RBAC
        Enable Add Permissions in the Access Token
3) Create new API permissions:
    -get:actors
    -get:movies
    -post:actors
    -post:movies
    -patch:actors
    -patch:movies
    -delete:actors
    -delete:movies
4) Create new roles for:
    casting-director
        permissions:
            -delete:actors
            -patch:actors
            -patch:movies
            -post:actors
    casting-assistant:
        permissions:
            -get:actors
            -get:movies
    executive-producer:
        permissions:
            -delete:movies
            -patch:movies
            -post:movies

5) To optain JWT Tokens: https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}

6) Insert JWT Tokens into 'bearer_tokens' section in settings.py.


### Project Depenedencies, local developement, Hosting Instruction, Enviromental Variables


### Enviromental Variables:

1) Install python-dotenv:

    $ pip install dotenv

2) Create a '.env' file:

    $ touch .env

3) Add DATABASE_URL

    DATABASE_URL = "postgres://{username}:{password}@localhost:{port}/{database_name}"

4) Add SECRET_KEY (OPTIONAL)

    SECRET_KEY = "{SECRET_KEY}"


# dependencies:
- I used python 3.8.2 but anything over 3.7 will work. 
- All the related dependencies are in the requirements.txt

# Create a virtualenv and install dependencies

1) Install Virtualenv  

    python -m pip install --user virtualenv

2) Create Virtualenv in local project

    virtualenv -p /usr/bin/python3 isoEnv

3) Install needed dependencies:

    pip install -r requirements.txt



### Detailed instructions for scripts to install any project dependencies, and to run the development server.
    
# How To Run:

To run appliation developement server:

    ```python app.py```

To run tests:

    ```python test_app.py```


Testing Results Examples:


'''
    ......................
----------------------------------------------------------------------
Ran 22 tests in 6.834s

OK
(env) _____@______:~/Desktop/castingagency$ 
'''
    
### Documentation of API behavior and RBAC controls


## GET /actors

Query paginated actors.

$ curl -X GET 

Example response:




2. POST /actors

Insert new actor into database.

$ curl -X POST http://127.0.0.1:8080/actors

Example response:

If you try to create a new actor without a requiered field like name, it will throw a 422 error:




3. PATCH /actors

Edit an existing Actor

$ curl -X PATCH 


Example response:





4. DELETE /actors

Delete an existing Actor

$ curl -X DELETE


Example response




5. GET /movies

Query paginated movies.

$ curl -X GET 


Example response




6. POST /movies

Insert new Movie into database.

$ curl -X POST http://127.0.0.1:8080/movies





7. PATCH /movies

Edit an existing Movie

$ curl -X PATCH http://127.0.0.1:8080/movies
Example response

{
    "created": 1,
    "movie": [
        {
            "id": 1,
            "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
            "title": "Test Movie 123"
        }
    ],
    "success": true
}




8. DELETE /movies

Delete an existing movie

$ curl -X DELETE https://artist-capstone-fsnd-matthew.herokuapp.com/movies/1

Example response

{
    "deleted": 5,
    "success": true
}



