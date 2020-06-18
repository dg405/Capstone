# Capstone Project

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virtual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create new databases for the main application and test script:
```bash
createdb agency
createdb agencytest
```

## Running the Server Locally

From within the directory first ensure you are using your created virtual environment and have changed the `database_path` in `models.py` to reflect your local database path.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Testing
To run the tests, run:
```
python test_app.py
```

## API Reference

### Getting Started
- Base URL: **_https://capstone-dan.herokuapp.com/_**
- Authentication: Auth0 is used for authenication. Bearer tokens for all three roles are available in the `test_app.py` file and expire after 24 hours (limit set by Auth0).

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 400,
    "message": "bad request",
    "success": False
    
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 401: Not Authorized
- 404: Not Found
- 405: Method Not Allowed
- 422: Not Processable

### Endpoints 
#### GET /actors
- General:
    - Returns a list of actor objects and a success value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/actors -H"Authorization: Bearer <Token>"`
- Requires Permission: `get:actors`
- Sample Response:
``` 
{
    "actors": [
        {
            "age": 25,
            "gender": "Male",
            "id": 3,
            "name": "Dom"
        }
    ],
    "status": true
}

```

#### GET /movies
- General:
    - Returns a list of movie objects and a success value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/movies -H"Authorization: Bearer <Token>"`
- Requires Permission: `get:movies`
- Sample Response:
```
{
    "movies": [
        {
            "actor_id": [
                1,
                3,
                2
            ],
            "id": 7,
            "release_date": "Fri, 12 Jun 2020 00:00:00 GMT",
            "title": "Batman"
        }
    ], 
    "status": true
}
```

#### POST /actors
- General:
    - Posts a new actor to the database.
    - Returns the actor posted and a status value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/actors -X POST -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"name": "Dan", "age": "32","gender": "Male"}'`
- Requires Permission: `post:actors`
- Sample Response:
```
{
    "actor": [
        {
            "age": 32,
            "gender": "Male",
            "id": 21,
            "name": "Dan"
        }
    ],
    "status": true
}
```

#### POST /movies
- General:
    - Posts a new movie to the database.
    - Returns the movie posted and a status value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/movies -X POST -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"title": "Batman", "release_date": "2020-06-12", "actor_id": [1, 3, 2]}'`
- Requires Permission: `post:movies`
- Sample Response:
```
{
    "movie": [
        {
            "actor_id": [
                1,
                3,
                2
            ],
            "id": 20,
            "release_date": "Fri, 12 Jun 2020 00:00:00 GMT",
            "title": "Batman"
        }
    ],
    "status": true
}
```

#### PATCH /actors
- General:
    - Modifies an actor on the database.
    - Returns the modified actor and a status value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/actors/1 -X PATCH -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"age": "52", "gender": "Female"}'`
- Requires Permission: `patch:actors`
- Sample Response:
```
{
    "actor": [
        {
            "age": 52,
            "gender": "Female",
            "id": 1,
            "name": "Dan"
        }
    ],
    "status": true
}
```

#### PATCH /movies
- General:
    - Modifies a  movie on the database.
    - Returns the modified movie and a status value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/movies -X PATCH -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"title": "Wonder Woman}'`
- Requires Permission: `patch:movies`
- Sample Response:
```
{
    "movie": [
        {
            "actor_id": [
                1
            ],
            "id": 1,
            "release_date": "Thu, 18 Jun 2020 00:00:00 GMT",
            "title": "Wonder Woman"
        }
    ],
    "status": true
}
```

#### DELETE /actors
- General:
    - Deletes an actor on the database.
    - Returns the id of the deleted actor and a status value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/actors/22 -X DELETE -H"Authorization: Bearer <Token>" `
- Requires Permission: `delete:actors`
- Sample Response:
```
{
    "actor": "22",
    "status": true
}
```

#### DELETE /movies
- General:
    - Deletes a  movie on the database.
    - Returns the deleted movie and a status value.
- Sample Request: `curl https://capstone-dan.herokuapp.com/movies/7 -X DELETE -H"Authorization: Bearer <Token>"`
- Requires Permission: `delete:movies`
- Sample Response:
```
{
    "movie": "7",
    "status": true
}
```
### Permissions
The following permissions were created in and are managed by Auth0: 
- get:movies (can see all movies)
- get:actors (can see all actors)
- post:actors (can create new actors)
- post:movies (can create new movies)
- patch:actors (can modify actors)
- patch:movies (can modify movies)
- delete:actors (can delete actors)
- delete:movies (can delete movies)

### Roles 
The following roles have been assigned the permissions listed below:

#### Casting Assistant
- get:actors
- get:movies

#### Casting Director
- get:actors
- get:movies
- post:actors
- patch:actors
- delete:actors 
- patch:movies 

#### Executive Director
- get:actors
- get:movies
- post:actors
- patch:actors
- delete:actors 
- patch:movies 
- post:movies
- delete:movies

Bearer tokens for all three roles are available in the `test_app.py` file and expire after 24 hours (limit set by Auth0).

## Authors
Dan Ghadimi

## Acknowledgements 
The awesome team at Udacity!
 
