import os
from sqlalchemy import Column, String, create_engine, Integer, DateTime, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import json
from array import array
from sqlalchemy.dialects import postgresql



#database_path = os.environ['DATABASE_URL']

#uncomment to run locally
#database_path = 'postgresql://postgres:bowimi321@localhost:5432/agency'
database_path = 'postgres://qkemyejqagfnpt:ca6391feb2aa6ecd86b8cc4dffd4de1f554667ef0d2b3de77211631509cf90ca@ec2-34-202-88-122.compute-1.amazonaws.com:5432/dbulfli3d8a6t3'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

def db_commit():
    #db.session.execute(new_performance) 
    db.session.commit()

'''
Initialise database with test records 
'''

def db_init_records():

    actor1 = (Actor(
        name = 'Dan',
        gender = 'Male',
        age = 26
        ))
    
    actor2 = (Actor(
        name = 'Claudia',
        gender = 'Female',
        age = 23
        ))

    actor3 = (Actor(
        name = 'Dom',
        gender = 'Male',
        age = 25
        ))

    movie1 = (Movie(
        title = 'James Bond',
        release_date = date.today(),
        actor_id = [1]
        ))

    movie2 = (Movie(
        title = 'Toy Story',
        release_date = date.today(),
        actor_id = [1]
        ))

    movie3 = (Movie(
        title = 'Love Actually',
        release_date = date.today(),
        actor_id = [1]
        ))

    performance = Performance.insert().values(
        Movie_id = 1,
        Actor_id = 1,
    )
    

    actor1.insert()
    actor2.insert()
    actor3.insert()
    movie1.insert()
    movie2.insert()
    movie3.insert()
    db.session.execute(performance) 
    db.session.commit()

def associationupdate(movieid, actorid):
    performance = Performance.insert().values(
        Movie_id = movieid,
        Actor_id = actorid,
    )
    
    db.session.execute(performance) 
    db.session.commit()



'''
Association table linking movies and actors in Performances 
'''

Performance = db.Table('performances',
  db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')), 
  db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')), 
  )


'''
Actors
Have name, age and gender
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  gender = Column(String)
  age = Column(Integer)
  performances = db.relationship('Movie', secondary=Performance, backref=db.backref('actors', lazy='joined'))
  

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  #inserts a new model into the database 
  def insert(self):
    db.session.add(self)
    db.session.commit()

  #updates a model in the database, the model must already exist
  def update(self):
    db.session.commit()
  
  #deletes a model in the database, the model must already exist
  def delete(self): 
    db.session.delete(self)
    db.session.commit()

  #define the format for the object returned
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender,
      'age': self.age
      }

'''
Movies
Have title and release date
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)
  actor_id = Column(postgresql.ARRAY(Integer), nullable=True)
  

  def __init__(self, title, release_date, actor_id):
    self.title = title
    self.release_date = release_date
    self.actor_id = actor_id


  #inserts a new model into the database 
  def insert(self):
    db.session.add(self)
    db.session.commit()

  #updates a model in the database, the model must already exist
  def update(self):
    db.session.commit()
  
  #deletes a model in the database, the model must already exist
  def delete(self): 
    db.session.delete(self)
    db.session.commit()

  #define the format for the object returned
  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
      'actor_id': self.actor_id
      }

 