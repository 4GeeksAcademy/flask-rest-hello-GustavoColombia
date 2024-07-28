from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    is_banned = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "is_banned": self.is_banned

            # do not serialize the password, its a security breach
        }
  
  
    
    favorite_people = db.relationship("FavoritePeople", backref="user_favorite_people") 
    favorite_planets = db.relationship("FavoritePlanet", backref="user_favorite_planets") 
   
    
class People (db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    height = db.Column(db.String(30), nullable=False)
    mass = db.Column(db.String(60),  nullable=False)
    hair_color = db.Column(db.String(60), nullable=False)    
    skin_color = db.Column(db.String(60), nullable=False)
    eye_color = db.Column(db.String(60), nullable=False)
    birth_year = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender

            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rotation_period = db.Column(db.String(50),  nullable=False)
    orbital_period = db.Column(db.String(100),  nullable=False)
    diameter = db.Column(db.String(100),  nullable=False)
    climate = db.Column(db.String(100),  nullable=False)
    gravity = db.Column(db.String(100),  nullable=False)
    terrain = db.Column(db.String(100),  nullable=False)
    surface_water = db.Column(db.String(100), nullable=False)
    population = db.Column(db.String(100),  nullable=False)
    


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population

            # do not serialize the password, its a security breach
        }



            # do not serialize the password, its a security breach
        
class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
            

            # do not serialize the password, its a security breach
        }
class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
                    
           

            # do not serialize the password, its a security breach
        }




            # do not serialize the password, its a security breach
     
    
