"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, FavoritePlanet, FavoritePeople
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    serialize_persons = [person.serialize() for person in people] 
    return jsonify({"people": serialize_persons}), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    
    if person is None:
        return jsonify({"error": "People not found"}), 404
    
    return jsonify(person.serialize()), 200

    
@app.route('/people', methods=['POST'])
def create_people():
    body = request.json
    name = body.get("name", None)
    height = body.get("height", None)
    mass = body.get("mass", None)
    hair_color = body.get("hair_color", None)
    skin_color= body.get("skin_color", None)
    eye_color = body.get("eye_color", None)
    birth_year = body.get("birth_year", None)
    gender = body.get("gender", None)


    if name is None or height is None or mass is None or hair_color is None or skin_color is None or eye_color is None or birth_year is None or gender is None:
     return jsonify({"error": "missing fields"}), 400
    
     
    person = People(
        name=name,
        height=height,
        mass=mass,
        hair_color=hair_color,
        skin_color=skin_color,
        eye_color=eye_color,
        birth_year=birth_year,
        gender=gender
    )
    try:

        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)
        return jsonify(person.serialize()), 201
        
    except Exception as error:
        db.session.rollback()
        return jsonify({"error":f"{error}"}), 500 
    
      
@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    serialize_planets = [planet.serialize() for planet in planets] 
    return jsonify({"planets": serialize_planets}), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    return jsonify(planet.serialize()), 200
    
@app.route('/planet', methods=['POST'])
def create_one_planets():
    body = request.json
    name = body.get("name", None)
    rotation_period = body.get("rotation_period", None)
    orbital_period= body.get("orbital_period", None)
    diameter = body.get("diameter", None)
    climate= body.get("climate", None)
    gravity = body.get("gravity", None)
    terrain = body.get("terrain", None)
    surface_water= body.get("surface_water", None)
    population = body.get("population", None)


    if name is None or rotation_period is None or orbital_period is None or diameter is None or climate is None or gravity is None or terrain is None or surface_water is None or population is None:
     return jsonify({"error": "missing fields"}), 400
    
     
    planet = Planet(
        name=name,
        rotation_period = rotation_period,
        orbital_period = orbital_period,
        diameter = diameter,
        climate = climate,
        gravity = gravity,
        terrain = terrain,
        surface_water = surface_water,
        population = population
    )
    try:

        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)
        return jsonify(planet.serialize()), 201
        
    except Exception as error:
        db.session.rollback()
        return jsonify({"error":f"{error}"}), 500 
    
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialize_users = [user.serialize() for user in users] 
    return jsonify({"users": serialize_users}), 200

@app.route('/people/favorite/', methods=['GET'])
def get_favorite_people():
    favorites_people = FavoritePeople.query.all()
    serialize_favorites_people = [favorite_people.serialize() for favorite_people in favorites_people]
    return jsonify({"favorites_people": serialize_favorites_people}), 200


@app.route('/planet/favorite/', methods=['GET'])
def get_favorite_planet():
    favorites_planets = FavoritePlanet.query.all()
    serialize_favorites_planets = [favorite_planet.serialize() for favorite_planet in favorites_planets]
    return jsonify({"favorites_planet": serialize_favorites_planets}), 200

@app.route('/users', methods=['POST'])
def register_user():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)
    is_active = body.get("is_active", None)
    is_banned = body.get("is_banned", None)

    
    if email is None or password is None or is_active is None or is_banned is None:
     return jsonify({"error": "missing fields"}), 400
    
    new_user = User(email=email, password=password, is_active=is_active, is_banned=is_banned)

    try:

        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
        
    except Exception as error:
      return jsonify({"error":f"{error}"}), 500 
    
@app.route('/people/favorite/', methods=['POST'])
def create_the_favorite_people():
     
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    body = request.json
    user_id = body.get("user_id", None)
    people_id = body.get("people_id", None)

    if user_id is None or people_id is None:
     return jsonify({"error": "missing fields"}), 400

    new_favorite_character = FavoritePeople(user_id=user_id, people_id=people_id)

    try:
        
        db.session.add(new_favorite_character)
        db.session.commit()
        return jsonify((new_favorite_character.serialize())), 201

    except Exception as error:
        return jsonify({"error":str(error)}), 500


@app.route('/planet/favorite/', methods=['POST'])
def create_the_favorite_planet():
     
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    body = request.json
    user_id = body.get("user_id", None)
    planet_id = body.get("planet_id", None)

    if user_id is None or planet_id is None:
     return jsonify({"error": "missing fields"}), 400

    new_favorite_planet = FavoritePlanet(user_id=user_id, planet_id=planet_id)

    try:
        
        db.session.add(new_favorite_planet)
        db.session.commit()
        return jsonify((new_favorite_planet.serialize())), 201

    except Exception as error:
        return jsonify({"error":str(error)}), 500


@app.route('/people/favorite/', methods=['POST'])
def create_favorite_people():
        favorites_people = FavoritePeople.query.all()
        serialize_favorites_people = [favorite_people.serialize() for favorite_people in favorites_people]
        return jsonify({"favorites_people": serialize_favorites_people}), 200


@app.route('/planet/favorite/', methods=['POST'])
def create_favorite_planet():
        favorites_planets = FavoritePlanet.query.all()
        serialize_favorites_planets = [favorite_planet.serialize() for favorite_planet in favorites_planets]
        return jsonify({"favorites_planet": serialize_favorites_planets}), 200



@app.route('/users/favorites/<int:id>', methods=['GET'])
def get_user_favorites(id):
    planets = FavoritePlanet.query.filter_by(user_id=id).all()
    people = FavoritePeople.query.filter_by(user_id=id).all()
    serialize_planets = [planet.serialize() for planet in planets] 
    serialize_people =  [person.serialize() for person in people]
    return jsonify({"favorite_planets": serialize_planets, "favorite_people": serialize_people}), 200
    

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet = FavoritePlanet.query.filter_by(planet_id=planet_id).first()
    if favorite_planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404

    try:
        db.session.delete(favorite_planet)
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted successfully"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite_people = FavoritePeople.query.filter_by(people_id=people_id).first()
    if favorite_people is None:
        return jsonify({"error": "Favorite people not found"}), 404

    try:
        db.session.delete(favorite_people)
        db.session.commit()
        return jsonify({"message": "Favorite people deleted successfully"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
