
import os
from flask import Flask, request, abort, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, db_init_records, db_drop_and_create_all, Actor, Movie, Performance, db_commit, associationupdate
import json
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    
    #uncomment to start a new database on app refresh
    #db_drop_and_create_all()

    #uncomment to insert test data
    db_init_records()
    
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response



    '''
    API Endpoints
    '''
    #GET ENDPOINTS

    @app.route('/')
    def main():
        greeting = 'Hello and welcome to Dan\'s project!'

        return greeting

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actor.query.all()

        actors = []

        for actor in selection: 
            actors.append(actor.format())

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'status': True, 
            'actors': actors
        })

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movie.query.all()

        movies = []

        for movie in selection:
            movies.append(movie.format())

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'status': True, 
            'movies': movies
        })

    #DELETE ENPOINTS
    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        selection = Actor.query.get(id)

        if not selection:
            abort(404)
        
        try:
            selection.delete()
        
        except:
            abort(422)
            print('it could not be deleted')

        return jsonify({
            'status': True, 
            'actor': id
        })

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        selection = Movie.query.get(id)

        if not selection:
            abort(404)
        
        try:
            selection.delete()
        
        except:
            abort(422)
            print('it could not be deleted')

        return jsonify({
            'status': True, 
            'movie': id
        })

    #POST ENPOINTS
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        res = request.get_json()

        if not res:
            abort(400)

        try:
            actor = Actor(
                name=res['name'],
                age=res['age'],
                gender=res['gender']
            )
            actor.insert()
        
        except:
            abort(422)
            print('it could not be added') 
            
        return jsonify({
            'status': True, 
            'actor': [actor.format()]
        })


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        res = request.get_json()

        if not res:
            abort(400)

        try:
            movie = Movie(
                title=res['title'],
                release_date=res['release_date'],
                actor_id=res['actor_id']
            )
            
            movie.insert()

        except:
            print('movie could not be added') 
            abort(422)
            
        #fill association table
        try:
            index = 0
            for x in res['actor_id']:
                #if user inputted an incorrect ID it will skip it and input the rest
                try:
                    actor = Actor.query.get(res['actor_id'][index])
                    associationupdate(movie.id, actor.id)
                    index += 1
                except:
                    index += 1
                    

        except:
            print('performance could not be added') 
            abort(422)
            

        return jsonify({
            'status': True, 
            'movie': [movie.format()]
        })


    #PATCH ENPOINTS 
    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload, id):
        res = request.get_json()

        if not res: 
            abort(404)
        
        actor = Actor.query.get(id)

        try: 
            if 'name' in res: 
                actor.name = res['name']
            if 'age' in res: 
                actor.age = res['age']
            if 'gender' in res: 
                actor.gender = res['gender']
            
            actor.update()
        
        except: 
            print('could not create object')
            abort(422)

        return jsonify({
            'status': True, 
            'actor': [actor.format()]
        })

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload, id):
        res = request.get_json()

        if not res: 
            abort(404)
        
        movie = Movie.query.get(id)

        try: 
            if 'title' in res: 
                movie.title = res['title']
            if 'release_date' in res: 
                movie.release_date = res['release_date']
            if 'actor_id' in res: 
                movie.actor_id = res['actor_id']
            
            movie.update()
        
        except: 
            print('could not create object')
            abort(422)

        return jsonify({
            'status': True, 
            'movie': [movie.format()]
        })

    '''
    Error Handlers
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The server can not find the requested resource."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
            }), 405   


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable."
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "not authorized"
        }), 401


    return app


app = create_app()

if __name__ == '__main__':
    app.run()