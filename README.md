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


### Project Depenedencies, local developement, Hosting Instruction



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

$ curl -X GET https://artist-capstone-fsnd-matthew.herokuapp.com/actors?page1

    Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
    Request Arguments:
        integer page (optional, 10 actors per page, defaults to 1 if not given)
    Request Headers: None
    Requires permission: read:actors
    Returns:
        List of dict of actors with following fields:
            integer id
            string name
            string gender
            integer age
        boolean success

Example response

{
  "actors": [
    {
      "age": 25,
      "gender": "Andrew",
      "id": 1,
      "name": "Matthew"
      "favorite_color: "blue"
    }
  ],
  "success": true
}


2. POST /actors

Insert new actor into database.

$ curl -X POST https://artist-capstone-fsnd-matthew.herokuapp.com/actors

    Request Arguments: None
    Request Headers: (application/json) 1. string name (required) 2. integer age (required) 3. string gender
    Requires permission: create:actors
    Returns:
        integer id from newly created actor
        boolean success

Example response

{
    "created": 5,
    "success": true
}

Errors

If you try to create a new actor without a requiered field like name, it will throw a 422 error:

$ curl -X GET https://artist-capstone-fsnd-matthew.herokuapp.com/actors?page123124

will return

{
  "error": 422,
  "message": "no name provided.",
  "success": false
}

3. PATCH /actors

Edit an existing Actor

$ curl -X PATCH https://artist-capstone-fsnd-matthew.herokuapp.com/actors/1

    Request Arguments: integer id from actor you want to update
    Request Headers: (application/json) 1. string name 2. integer age 3. string gender
    Requires permission: edit:actors
    Returns:
        integer id from updated actor
        boolean success
        List of dict of actors with following fields:
            integer id
            string name
            string gender
            integer age

Example response

{
    "actor": [
        {
            "age": 30,
            "gender": "Other",
            "id": 1,
            "name": "Test Actor"
        }
    ],
    "success": true,
    "updated": 1
}

Errors

If you try to update an actor with an invalid id it will throw an 404error:

$ curl -X PATCH https://artist-capstone-fsnd-matthew.herokuapp.com/actors/125

will return

{
  "error": 404,
  "message": "Actor with id 125 not found in database.",
  "success": false
}

Additionally, trying to update an Actor with already existing field values will result in an 422 error:

{
  "error": 422,
  "message": "provided field values are already set. No update needed.",
  "success": false
}

4. DELETE /actors

Delete an existing Actor

$ curl -X DELETE https://artist-capstone-fsnd-matthew.herokuapp.com/actors/1

    Request Arguments: integer id from actor you want to delete
    Request Headers: None
    Requires permission: delete:actors
    Returns:
        integer id from deleted actor
        boolean success

Example response

{
    "deleted": 5,
    "success": true
}

Errors

If you try to delete actor with an invalid id, it will throw an 404error:

$ curl -X DELETE https://artist-capstone-fsnd-matthew.herokuapp.com/actors/125

will return

{
  "error": 404,
  "message": "Actor with id 125 not found in database.",
  "success": false
}

5. GET /movies

Query paginated movies.

$ curl -X GET https://artist-capstone-fsnd-matthew.herokuapp.com/movies?page1

    Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
    Request Arguments:
        integer page (optional, 10 movies per page, defaults to 1 if not given)
    Request Headers: None
    Requires permission: read:movies
    Returns:
        List of dict of movies with following fields:
            integer id
            string name
            date release_date
        boolean success

Example response

{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Matthew first Movie"
    }
  ],
  "success": true
}

Errors

If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

$ curl -X GET https://artist-capstone-fsnd-matthew.herokuapp.com/movies?page123124

will return

{
  "error": 404,
  "message": "no movies found in database.",
  "success": false
}

6. POST /movies

Insert new Movie into database.

$ curl -X POST https://artist-capstone-fsnd-matthew.herokuapp.com/movies

    Request Arguments: None
    Request Headers: (application/json) 1. string title (required) 2. date release_date (required)
    Requires permission: create:movies
    Returns:
        integer id from newly created movie
        boolean success

Example response

{
    "created": 5,
    "success": true
}

Errors

If you try to create a new movie without a requiered field like name, it will throw a 422 error:

$ curl -X GET https://artist-capstone-fsnd-matthew.herokuapp.com/movies?page123124

will return

{
  "error": 422,
  "message": "no name provided.",
  "success": false
}

7. PATCH /movies

Edit an existing Movie

$ curl -X PATCH https://artist-capstone-fsnd-matthew.herokuapp.com/movies/1

    Request Arguments: integer id from movie you want to update
    Request Headers: (application/json) 1. string title 2. date release_date
    Requires permission: edit:movies
    Returns:
        integer id from updated movie
        boolean success
        List of dict of movies with following fields:
            integer id
            string title
            date release_date

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

Errors

If you try to update an movie with an invalid id it will throw an 404error:

$ curl -X PATCH https://artist-capstone-fsnd-matthew.herokuapp.com/movies/125

will return

{
  "error": 404,
  "message": "Movie with id 125 not found in database.",
  "success": false
}

Additionally, trying to update an Movie with already existing field values will result in an 422 error:

{
  "error": 422,
  "message": "provided field values are already set. No update needed.",
  "success": false
}

8. DELETE /movies

Delete an existing movie

$ curl -X DELETE https://artist-capstone-fsnd-matthew.herokuapp.com/movies/1

    Request Arguments: integer id from movie you want to delete
    Request Headers: None
    Requires permission: delete:movies
    Returns:
        integer id from deleted movie
        boolean success

Example response

{
    "deleted": 5,
    "success": true
}

Errors

If you try to delete movie with an invalid id, it will throw an 404error:

$ curl -X DELETE https://artist-capstone-fsnd-matthew.herokuapp.com/movies/125

will return

{
  "error": 404,
  "message": "Movie with id 125 not found in database.",
  "success": false
}













.env
pip install python-dotenv