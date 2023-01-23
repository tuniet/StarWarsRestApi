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
from models import db, User, Planet, Character, FavouritePlanets, FavouriteCharacters
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

@app.route("/planets", methods=["GET"])
def getPlanet():
    planets = Planet.query.all()
    response = [planet.serialize() for planet in planets]
    response_body = {"message": "ok",
                     "results": response
    }
    return jsonify(response_body), 200

@app.route("/planets/<int:planetid>", methods=["GET"])
def getPlanetid(planetid):
    planet = db.get_or_404(Planet, planetid)
    response = planet.serialize()
    response_body = {"message": "ok",
                     "results": response
    }
    return jsonify(response_body), 200

@app.route("/characters", methods=["GET"])
def getCharacter():
    characters = Character.query.all()
    response = [character.serialize() for character in characters]
    response_body = {"message": "ok",
                     "results": response
    }
    return jsonify(response_body), 200

@app.route("/characters/<int:characterid>", methods=["GET"])
def getCharacterid(characterid):
    character = db.get_or_404(Character, characterid)
    response = character.serialize()
    response_body = {"message": "ok",
                     "results": response
    }
    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    response = [user.serialize() for user in users]
    response_body = {"message": "ok",
                     "results": response
    }

    return jsonify(response_body), 200

@app.route('/user/<int:userid>/favourites', methods=['GET'])
def getFavourites(userid):
    characters = FavouriteCharacters.query.filter(FavouriteCharacters.userid == userid).all()
    planets = FavouritePlanets.query.filter(FavouritePlanets.userid == userid).all()
    planetResult = [planet.serialize() for planet in planets]
    charResult = [character.serialize() for character in characters]
    response_body = {"message": "ok",
                     "planets": planetResult,
                     "characters": charResult
    }
    return jsonify(response_body), 200

@app.route('/user/<int:userId>/favourites/planet/<int:planetId>', methods=['POST'])
def postFavouritePlanet(userId, planetId):
    favPlanet = FavouritePlanets(userid = userId, planetid = planetId)
    db.session.add(favPlanet)
    db.session.commit()
    return jsonify("Ok"), 200

@app.route('/user/<int:userId>/favourites/character/<int:charId>', methods=['POST'])
def postFavouriteCharacter(userId, charId):
    favChar = FavouriteCharacters(userid = userId, characterid = charId)
    db.session.add(favChar)
    db.session.commit()
    return jsonify("Ok"), 200

#No se como hacer funcionar los DELETE :(
@app.route('/user/<int:userId>/favourites/planet/<int:planetId>', methods=['DELETE'])
def deleteFavouritePlanet(userId, planetId):
    delete = FavouritePlanets.query.filter((FavouritePlanets.userid == userId) and (FavouritePlanets.planetid == planetId))
    db.session.delete(delete)
    db.session.commit()
    return jsonify("Ok"), 200

@app.route('/user/<int:userId>/favourites/character/<int:charId>', methods=['DELETE'])
def deleteFavouriteCharacter(userId, charId):
    delete = FavouriteCharacters.query.filter((FavouriteCharacters.userid == userId) and (FavouriteCharacters.characterid == charId))
    db.session.delete(delete)
    db.session.commit()
    return jsonify("Ok"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
