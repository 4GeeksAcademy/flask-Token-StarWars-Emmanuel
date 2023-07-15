from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
            
class User(db.Model):
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250),unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.db.String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }

    def to_dict(self):
        return self.serialize()
    

class Characters(db.Model):
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birth_date = db.Column(db.String(250))
    height = db.Column(db.Integer, primary_key=False)
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    gender = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "gender": self.gender,
            "height": self.height,
            "birth_date": self.birth_date
        }

    def to_dict(self):
        return self.serialize()

class Planets(db.Model):
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.Integer, primary_key=False)
    diameter = db.Column(db.Integer, primary_key=False)
    climate = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    terrain = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "climate": self.climate,

        }

    def to_dict(self):
        return self.serialize()


class Ships(db.Model):
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    model = db.Column(db.String(250))
    max_speed = db.Column(db.Integer, primary_key=False)
    passengers = db.Column(db.Integer, primary_key=False)
    starship_class = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "passengers": self.passengers,
            "max_speed": self.max_speed,
            "starship_class": self.starship_class
        }

    def to_dict(self):
        return self.serialize()

    

class CharacterFavorites(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def serialize(self):
        return {
            "id": self.id,
            "char_id": self.character_id,
            "user": self.user_id
        }

    def to_dict(self):
        return self.serialize()

class PlanetsFavorites(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user": self.user_id
        }

    def to_dict(self):
        return self.serialize()

class ShipsFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        return {
            "id": self.id,
            "ship_id": self.vehicle_id,
            "user": self.user_id
        }

    def to_dict(self):
        return self.serialize()
    


# ## Draw from SQLAlchemy db.Model
# render_er(db.Model, 'diagram.png')


        


import os