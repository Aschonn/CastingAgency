import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance


###ADD THIS TO ENV
pagination = {
    "page_number" : 5 # Limits returned rows of API
}


ROWS_PER_PAGE = pagination['page_number']

def create_app(test_config=None):
  
  app = Flask(__name__)
  setup_db(app)
  
  #uncomment to create database from scratch

  # db_drop_and_create_all() 

  CORS(app)
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  #-----------------------------------Error message function-----------------------------------------#

  def get_error_message(error, default_text):

      try:
          return error.description['message']
      except:
          return default_text

#-----------------------------Pagination--------------------------------------#
  
  def paginate_results(request, selection):

    # Get page from request. If not given, default to 1
    page = request.args.get('page', 1, type=int)
    
    # Calculate start and end slicing
    start =  (page - 1) * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE

    # Format selection into list of dicts and return sliced
    objects_formatted = [object_name.format() for object_name in selection]
    return objects_formatted[start:end]

  
  
  
#-----------------------------API Endpoints--------------------------------------#


  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):

    selection = Actor.query.all()
    actors_paginated = paginate_results(request, selection)

    if len(actors_paginated) == 0:
      abort(404, {'message': 'no actors found in database.'})

    return jsonify({
      'success': True,
      'actors': actors_paginated
    })

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def insert_actors(payload):

    body = request.get_json()

    if not body:
          abort(400, {'message': 'request does not contain a valid JSON body.'})

    # Extract name, age, gender values from request body
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', 'Other')

    # abort if one of these are missing
    if not name:
      abort(422, {'message': 'no name provided.'})

    if not age:
      abort(422, {'message': 'no age provided.'})

    # Create new instance of Actor & insert it.
    new_actor = Actor(name = name, age = age, gender = gender)
    
    new_actor.insert()

    return jsonify({
      'success': True,
      'created': new_actor.id
    })

  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actors(payload, actor_id):

    body = request.get_json()

    # Find actor with matching id
    actor_to_update = Actor.query.filter(Actor.id == actor_id).one_or_none()

    #error if not valid
    if not actor_id:
      abort(400, {'message': 'please append an actor id to the request url.'})

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})

    if not actor_to_update:
      abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})

    #extract name and age value from request body
    name = body.get('name', actor_to_update.name)
    age = body.get('age', actor_to_update.age)
    gender = body.get('gender', actor_to_update.gender)

    # Set new field values
    actor_to_update.name = name
    actor_to_update.age = age
    actor_to_update.gender = gender

    #update actor with new values
    actor_to_update.update()

    #return json
    return jsonify({
      'success': True,
      'updated': actor_to_update.id,
      'actor' : [actor_to_update.format()]
    })

  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, actor_id):


    #find actor with matching id
    actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()

    #if actor_id or actor_to_delete no valid return error
    if not actor_id:
      abort(400, {'message': 'There is no actor_id in requested URL.'})

    if not actor_to_delete:
        abort(404, {'message': 'Actor not found in database.'})
    
    #delete actor from database
    actor_to_delete.delete()
    
    # Return json
    return jsonify({
      'success': True,
      'deleted': actor_id
    })


#---------------------------Movie Endpoints------------------------------#

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):

    selection = Movie.query.all()
    movies_paginated = paginate_results(request, selection)

    if len(movies_paginated) == 0:
      abort(404, {'message': 'no movies found in database.'})

    return jsonify({
      'success': True,
      'movies': movies_paginated
    })

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def insert_movies(payload):

    # Get request json
    body = request.get_json()

    if not body:
          abort(400, {'message': 'request does not contain a valid JSON body.'})

    # Extract title and release_date value from request body
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    # abort if one of these are missing with appropiate error message
    if not title:
      abort(422, {'message': 'no title provided.'})

    if not release_date:
      abort(422, {'message': 'no "release_date".'})

    # Create new instance of movie & insert it.
    new_movie = (Movie(
          title = title, 
          release_date = release_date
          ))
    new_movie.insert()

    return jsonify({
      'success': True,
      'created': new_movie.id
    })

  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movies(payload, movie_id):

    #get request json
    body = request.get_json()

    #abort if no movie_id or body has been provided
    if not movie_id:
      abort(400, {'message': 'There is no movie_id in requested URL'})

    if not body:
      abort(400, {'message': 'Doesnt have valid JSON body.'})

    #Find movie which should be updated by id
    update_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    #if no movies abort 404
    if not update_movie:
      abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})

    #Extract title and age value from request body
    title = body.get('title', update_movie.title)
    release_date = body.get('release_date', update_movie.release_date)

    # Set new values
    update_movie.title = title
    update_movie.release_date = release_date

    #uodate 
    update_movie.update()

    return jsonify({
      'success': True,
      'edited': update_movie.id,
      'movie' : [update_movie.format()]
    })

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, movie_id):

    # Find movie which should be deleted by id
    movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()
    
    # Abort if not valid
    if not movie_id:
      abort(400, {'message': 'please append an movie id to the request url.'})
  
    if not movie_to_delete:
        abort(404, {'message': 'Movie not found in database.'})
    
    # Delete movie from database
    movie_to_delete.delete()
    
    # Return success and id from deleted movie
    return jsonify({
      'success': True,
      'deleted': movie_id
    })

  #----------------------------------------------------------------------------#
  # Error Handlers
  #----------------------------------------------------------------------------#

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        "success": False, 
        "error": 422,
        "message": get_error_message(error,"unprocessable")
        }
      ), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        "success": False, 
        "error": 400,
        "message": get_error_message(error, "bad request")
        }
      ), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
        "success": False, 
        "error": 404,
        "message": get_error_message(error, "resource not found")
        }
      ), 404

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError): 
      return jsonify(
        {
          "success": False, 
          "error": AuthError.status_code,
          "message": AuthError.error['description']
        }
      ), AuthError.status_code


  # return after going through create_app() function
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)