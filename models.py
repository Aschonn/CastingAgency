import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from config import database_setup

#--------------------------------Database Setup --------------------------------------------#


db = SQLAlchemy()

def setup_db(app, database_path=database_path):

    # ENV = 'prod'

    # if ENV == 'dev':
    #   database_path = "postgres://postgres:091297@localhost:5432/casting'
    # else: 
    #   database_path = 'postgres://vdqikcbmqqwskr:0e2f2948a8f9941ecaf35f1d6cc1e38e68dcd22c124a22b118e17af82cc4af84@ec2-52-207-124-89.compute-1.amazonaws.com:5432/d2osbifms59anj'

    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://vdqikcbmqqwskr:0e2f2948a8f9941ecaf35f1d6cc1e38e68dcd22c124a22b118e17af82cc4af84@ec2-52-207-124-89.compute-1.amazonaws.com:5432/d2osbifms59anj'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    new_actor = (Actor(
        name = 'Andrew',
        gender = 'Male',
        age = 23,
        ))
    new_movie = (Movie(
        title = 'Raiders of the lost Arc',
        release_date = date.today()
        ))
    new_performance = Performance.insert().values(
        Movie_id = new_movie.id,
        Actor_id = new_actor.id,
        actor_fee = 700.00
    )

    new_actor.insert()
    new_movie.insert()
    db.session.execute(new_performance) 
    db.session.commit()


#--------------------------------# Performance Association Table --------------------------------------------#
#-------------------More Info: https://www.pythoncentral.io/sqlalchemy-association-tables/ ------------------#


Performance = db.Table('Performance', db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('actor_fee', db.Float)
)

#----------------------------------Actors Model ------------------------------------------#

class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  gender = Column(String)
  age = Column(Integer)
  favorite_color = Column(String)

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age
    self.favorite_color

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'gender': self.gender,
      'age': self.age,
      'favorite_color' : self.favorite_color
    }

 
#------------------------------------Movies Model ----------------------------------------#

class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)
  actors = db.relationship('Actor', secondary=Performance, backref=db.backref('performances', lazy='joined'))

  def __init__(self, title, release_date) :
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'release_date': self.release_date
    }