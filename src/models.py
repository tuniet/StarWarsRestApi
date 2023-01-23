from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    desc = db.Column(db.String(120), nullable = False)
    hair_color = db.Column(db.String(120), nullable=False)
    eye_color = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "desc": self.desc,
                "hair_color": self.hair_color,
                "eye_color": self.eye_color
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    desc = db.Column(db.String(120), nullable = False)
    climate = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "desc": self.desc,
                "climate": self.climate,
                "population": self.population
        }

class FavouritePlanets(db.Model):
    __tablename__ = 'favouritePlanets'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    planetid = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable = False)

    def __repr__(self):
        return '<FavouritePlanets %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "userid": self.userid,
                "planetid": self.planetid
        }

class FavouriteCharacters(db.Model):
    __tablename__ = 'favouriteCharacters'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    characterid = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)

    def __repr__(self):
        return '<FavouriteCharacters %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "userid": self.userid,
                "characterid": self.characterid
        }