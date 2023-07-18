from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=True)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=True)
    surname = db.Column(db.String(250), nullable=True)
    phone_number = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=False)
    addresses = db.relationship('Address', backref='user')
    is_active = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
            "email": self.email,
            "is_active" : self.is_active
        }

    def to_dict(self):
        return self.serialize()


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(250))
    street_number = db.Column(db.String(250))
    postal_code = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Address, self).__init__(**kwargs)

    def __repr__(self):
        return '<Address %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "street_name": self.street_name,
            "street_number": self.street_number,
            "postal_code": self.postal_code,
            "user_id": self.user_id
        }

    def to_dict(self):
        return self.serialize()


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(25))
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    

    def __init__(self, **kwargs):
        super(Planet, self).__init__(**kwargs)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
        }

    def to_dict(self):
        return self.serialize()


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    eye_color = db.Column(db.String(20))
    hair_color = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    height = db.Column(db.Integer)
    birth_date = db.Column(db.Integer)
    

    def __init__(self, **kwargs):
        super(Character, self).__init__(**kwargs)

    def __repr__(self):
        return '<Character %r>' % self.name

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


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    passengers = db.Column(db.Integer)
    max_speed = db.Column(db.Integer)
    vehicle_class = db.Column(db.String(250))
    

    def __init__(self, **kwargs):
        super(Vehicle, self).__init__(**kwargs)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "passengers": self.passengers,
            "max_speed": self.max_speed,
            "vehicle_class": self.vehicle_class
        }

    def to_dict(self):
        return self.serialize()


class Character_Favorite_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Character_Favorite_List, self).__init__(**kwargs)

    def __repr__(self):
        return '<Character_Favorite_List %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "user_id": self.user_id
        }

    def to_dict(self):
        return self.serialize()

class Planet_Favorite_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Planet_Favorite_List, self).__init__(**kwargs)

    def __repr__(self):
        return '<Planet_Favorite_List %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "Planet_id": self.planet_id,
            "user_id": self.user_id
        }

    def to_dict(self):
        return self.serialize()

class Vehicle_Favorite_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Vehicle_Favorite_List, self).__init__(**kwargs)

    def __repr__(self):
        return '<Vehicle_Favorite_List %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "user_id": self.user_id
        }

    def to_dict(self):
        return self.serialize()