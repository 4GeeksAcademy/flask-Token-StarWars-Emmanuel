"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, redirect, session, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap, generate_token
from admin import setup_admin
from models import db, User, Address, Planet, Character, Vehicle, Character_Favorite_List, Planet_Favorite_List, Vehicle_Favorite_List

from flask_bcrypt import Bcrypt  # para encriptar y comparar
from flask_sqlalchemy import SQLAlchemy  # Para rutas
from flask_jwt_extended import  JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

# app.config["JWT_SECRET_KEY"] = "valor-variable"  # clave secreta para firmar los tokens, cuanto mas largo mejor.


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.url_map.strict_slashes = False
jwt = JWTManager(app)  # isntanciamos jwt de JWTManager utilizando app para tener las herramientas de encriptacion.

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

# ... (definiciones de las rutas para User)

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        serialized_users = [user.serialize() for user in users]
        return jsonify(users=serialized_users), 200

    except Exception as e:
        return jsonify({'error': 'Error retrieving users: ' + str(e)}), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404
    return jsonify(user.serialize())

# ... (create user that works like a signup)

@app.route('/signup', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        

        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user is not None:
            return jsonify({'error': 'Email already exists.'}), 409

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # username = data.get('username')
        # name = data.get('name')
        # surname = data.get('surname')
        # phone_number = data.get('phone_number')

        # if not username or not name or not surname or not phone_number:
        #     return jsonify(message='Missing required fields'), 400

        # address_data = data.get('address')
        # if not address_data:
        #     return jsonify(message='Address is required'), 400

        # street_name = address_data.get('street_name')
        # street_number = address_data.get('street_number')
        # postal_code = address_data.get('postal_code')

        # if not street_name or not street_number or not postal_code:
        #     return jsonify(message='Missing required fields for address'), 400

        new_user = User(email=email, password=password_hash, is_active = False)
        
        # (username=username, password=password_hash, name=name, surname=surname,
        #                 phone_number=phone_number, email=email)
        # new_address = Address(street_name=street_name, street_number=street_number, postal_code=postal_code)
        # new_user.address = new_address

        db.session.add(new_user)
        db.session.commit()

        return jsonify(message='User created successfully', user=new_user.serialize()), 201

    except Exception as e:
        return jsonify({'error': 'Error in user creation: ' + str(e)}), 500

# ... (login route)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        is_active = data.get('is_active')

        # # Query the User model using the provided email
    
        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400
        
        login_user = User.query.filter_by(email=request.json['email']).one()
        password_db = login_user.password
        true_o_false = bcrypt.check_password_hash(password_db, password)
        
        if true_o_false:
            # Lógica para crear y enviar el token
            user_id = login_user.id
            access_token = create_access_token(identity=user_id)
            form_status = login_user.is_active 
            return jsonify({ 'access_token':access_token, 'form_status':form_status}), 200
        else:
            return {"Error":"Contraseña  incorrecta"}

        # and user.password == password:
        # and is_active:
            # Generate the token object (e.g., using JWT library)
            token = generate_token(user.id)

        #     # Save the token in the session
        #     session['token'] = token

          
        #     return redirect(url_for('/private'))
        # else:
            # return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': 'Error in login: ' + str(e)}), 500

# ... (logout route)

@app.route('/logout', methods=['POST'])
@jwt_required()  # Requires authentication with a valid JWT token
def logout():
    unset_jwt_cookies()  # Remove JWT token from the client

    return redirect(url_for('/signup'))  # Redirect to the home page (public)

# ... (Private route)

@app.route('/private')
def private():
    token = session.get('token')
    if token:
        # User is authenticated, perform private actions
        return jsonify({'message': 'Welcome to the private area!'})
    else:
        return jsonify({'error': 'Unauthorized'}), 401

# ... (token route)

@app.route('/token', methods=['POST'])
def get_token():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400
        
        login_user = User.query.filter_by(email=request.json['email']).one()
        password_db = login_user.password
        true_o_false = bcrypt.check_password_hash(password_db, password)
        
        if true_o_false:
            # Lógica para crear y enviar el token
            user_id = login_user.id
            access_token = create_access_token(identity=user_id)
            return { 'access_token':access_token}, 200

        else:
            return {"Error":"Incorrect Password"}
    
    except Exception as e:
        return {"Error":"Written email is not in the database:" + str(e)}, 500

# ... (otros métodos para users)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')
    phone_number = data.get('phone_number')
    email = data.get('email')

    if not username or not password or not name or not surname or not phone_number or not email:
        return jsonify(message='Missing required fields'), 400

    user.username = username
    user.password = password
    user.name = name
    user.surname = surname
    user.phone_number = phone_number
    user.email = email

    address_data = data.get('address')
    if address_data:
        address = Address.query.filter_by(user_id=user_id).first()
        if not address:
            return jsonify(message='Address not found for the user'), 404

        street_name = address_data.get('street_name')
        street_number = address_data.get('street_number')
        postal_code = address_data.get('postal_code')

        if not street_name or not street_number or not postal_code:
            return jsonify(message='Missing required fields for address'), 400

        address.street_name = street_name
        address.street_number = street_number
        address.postal_code = postal_code

    db.session.commit()

    return jsonify(message='User and address updated successfully', user=user.serialize(), address=address.serialize())


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    # Delete associated address
    address = Address.query.filter_by(user_id=user_id).first()
    if address:
        db.session.delete(address)

    # Delete associated favorite lists
    character_favorite_list = Character_Favorite_List.query.filter_by(user_id=user_id).first()
    if character_favorite_list:
        db.session.delete(character_favorite_list)

    planet_favorite_list = Planet_Favorite_List.query.filter_by(user_id=user_id).first()
    if planet_favorite_list:
        db.session.delete(planet_favorite_list)

    vehicle_favorite_list = Vehicle_Favorite_List.query.filter_by(user_id=user_id).first()
    if vehicle_favorite_list:
        db.session.delete(vehicle_favorite_list)

    db.session.delete(user)
    db.session.commit()

    return jsonify(message='User deleted successfully')

# ... (definiciones de la clase Adress)

@app.route('/addresses', methods=['GET'])
def get_addresses():
    addresses = Address.query.all()
    return jsonify(addresses=[address.serialize() for address in addresses])

@app.route('/addresses/<int:address_id>', methods=['GET'])
def get_address(address_id):
    address = Address.query.get(address_id)
    if address:
        return jsonify(address.serialize())
    else:
        return jsonify(message='Address not found'), 404

@app.route('/addresses', methods=['POST'])
def create_address():
    data = request.get_json()
    street_name = data.get('street_name')
    street_number = data.get('street_number')
    postal_code = data.get('postal_code')
    user_id = data.get('user_id')

    new_address = Address(street_name=street_name, street_number=street_number, postal_code=postal_code, user_id=user_id)
    db.session.add(new_address)
    db.session.commit()

    return jsonify(message='Address created successfully', address=new_address.serialize()), 201

@app.route('/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        return jsonify(message='Address not found'), 404

    data = request.get_json()
    address.street_name = data.get('street_name', address.street_name)
    address.street_number = data.get('street_number', address.street_number)
    address.postal_code = data.get('postal_code', address.postal_code)
    address.user_id = data.get('user_id', address.user_id)

    db.session.commit()

    return jsonify(message='Address updated successfully', address=address.serialize())

@app.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    address = Address.query.get(address_id)
    if address:
        db.session.delete(address)
        db.session.commit()
        return jsonify(message='Address deleted successfully')
    else:
        return jsonify(message='Address not found'), 404


# ... (definiciones de las clases Planet, Character, Vehicle)

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify(planets=[planet.serialize() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    else:
        return jsonify(message='Planet not found'), 404

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    population = data.get('population')
    terrain = data.get('terrain')
    diameter = data.get('diameter')
    orbital_period = data.get('orbital_period')

    new_planet = Planet(name=name, description=description, population=population, terrain=terrain,
                        diameter=diameter, orbital_period=orbital_period)
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(message='Planet created successfully', planet=new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify(message='Planet not found'), 404

    data = request.get_json()
    planet.name = data.get('name', planet.name)
    planet.description = data.get('description', planet.description)
    planet.population = data.get('population', planet.population)
    planet.terrain = data.get('terrain', planet.terrain)
    planet.diameter = data.get('diameter', planet.diameter)
    planet.orbital_period = data.get('orbital_period', planet.orbital_period)

    db.session.commit()

    return jsonify(message='Planet updated successfully', planet=planet.serialize())

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message='Planet deleted successfully')
    else:
        return jsonify(message='Planet not found'), 404


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify(characters=[character.serialize() for character in characters])

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character:
        return jsonify(character.serialize())
    else:
        return jsonify(message='Character not found'), 404

@app.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    eye_color = data.get('eye_color')
    hair_color = data.get('hair_color')
    gender = data.get('gender')
    height = data.get('height')
    birth_date = data.get('birth_date')

    new_character = Character(name=name, description=description, eye_color=eye_color, hair_color=hair_color,
                              gender=gender, height=height, birth_date=birth_date)
    db.session.add(new_character)
    db.session.commit()

    return jsonify(message='Character created successfully', character=new_character.serialize()), 201

@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify(message='Character not found'), 404

    data = request.get_json()
    character.name = data.get('name', character.name)
    character.description = data.get('description', character.description)
    character.eye_color = data.get('eye_color', character.eye_color)
    character.hair_color = data.get('hair_color', character.hair_color)
    character.gender = data.get('gender', character.gender)
    character.height = data.get('height', character.height)
    character.birth_date = data.get('birth_date', character.birth_date)

    db.session.commit()

    return jsonify(message='Character updated successfully', character=character.serialize())

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify(message='Character deleted successfully')
    else:
        return jsonify(message='Character not found'), 404


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify(vehicles=[vehicle.serialize() for vehicle in vehicles])

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        return jsonify(vehicle.serialize())
    else:
        return jsonify(message='Vehicle not found'), 404

@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    model = data.get('model')
    manufacturer = data.get('manufacturer')
    passengers = data.get('passengers')
    max_speed = data.get('max_speed')
    vehicle_class = data.get('vehicle_class')

    new_vehicle = Vehicle(name=name, description=description, model=model, manufacturer=manufacturer,
                          passengers=passengers, max_speed=max_speed, vehicle_class=vehicle_class)
    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(message='Vehicle created successfully', vehicle=new_vehicle.serialize()), 201

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify(message='Vehicle not found'), 404

    data = request.get_json()
    vehicle.name = data.get('name', vehicle.name)
    vehicle.description = data.get('description', vehicle.description)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.manufacturer = data.get('manufacturer', vehicle.manufacturer)
    vehicle.passengers = data.get('passengers', vehicle.passengers)
    vehicle.max_speed = data.get('max_speed', vehicle.max_speed)
    vehicle.vehicle_class = data.get('vehicle_class', vehicle.vehicle_class)

    db.session.commit()

    return jsonify(message='Vehicle updated successfully', vehicle=vehicle.serialize())

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify(message='Vehicle deleted successfully')
    else:
        return jsonify(message='Vehicle not found'), 404

# ... (definición de la clase Character_Favorite_List)

@app.route('/character-favorite-lists', methods=['GET'])
def get_character_favorite_lists():
    favorite_lists = Character_Favorite_List.query.all()
    return jsonify(favorite_lists=[favorite_list.serialize() for favorite_list in favorite_lists])

@app.route('/character-favorite-lists', methods=['POST'])
def create_character_favorite_list():
    data = request.get_json()
    character_id = data.get('character_id')
    user_id = data.get('user_id')

    new_character_favorite_list = Character_Favorite_List(character_id=character_id, user_id=user_id)
    db.session.add(new_character_favorite_list)
    db.session.commit()

    return jsonify(message='Character favorite list created successfully', favorite_list=new_character_favorite_list.serialize()), 201

@app.route('/character-favorite-lists/<int:favorite_list_id>', methods=['GET'])
def get_character_favorite_list(favorite_list_id):
    favorite_list = Character_Favorite_List.query.get(favorite_list_id)
    if favorite_list:
        return jsonify(favorite_list.serialize())
    else:
        return jsonify(message='Character favorite list not found'), 404

@app.route('/character-favorite-lists/<int:favorite_list_id>', methods=['PUT'])
def update_character_favorite_list(favorite_list_id):
    favorite_list = Character_Favorite_List.query.get(favorite_list_id)
    if not favorite_list:
        return jsonify(message='Character favorite list not found'), 404

    data = request.get_json()
    favorite_list.character_id = data.get('character_id', favorite_list.character_id)
    favorite_list.user_id = data.get('user_id', favorite_list.user_id)

    db.session.commit()

    return jsonify(message='Character favorite list updated successfully', favorite_list=favorite_list.serialize())

@app.route('/character-favorite-lists/<int:favorite_list_id>', methods=['DELETE'])
def delete_character_favorite_list(favorite_list_id):
    favorite_list = Character_Favorite_List.query.get(favorite_list_id)
    if favorite_list:
        db.session.delete(favorite_list)
        db.session.commit()
        return jsonify(message='Character favorite list deleted successfully')
    else:
        return jsonify(message='Character favorite list not found'), 404



# ... (definición de la clase Planet_Favorite_List)

@app.route('/planet-favorite-lists', methods=['GET'])
def get_planet_favorite_lists():
    favorite_lists = Planet_Favorite_List.query.all()
    return jsonify(favorite_lists=[favorite_list.serialize() for favorite_list in favorite_lists])

@app.route('/planet-favorite-lists', methods=['POST'])
def create_planet_favorite_list():
    data = request.get_json()
    planet_id = data.get('planet_id')
    user_id = data.get('user_id')

    new_planet_favorite_list = Planet_Favorite_List(planet_id=planet_id, user_id=user_id)
    db.session.add(new_planet_favorite_list)
    db.session.commit()

    return jsonify(message='Planet favorite list created successfully', favorite_list=new_planet_favorite_list.serialize()), 201

@app.route('/planet-favorite-lists/<int:favorite_list_id>', methods=['GET'])
def get_planet_favorite_list(favorite_list_id):
    favorite_list = Planet_Favorite_List.query.get(favorite_list_id)
    if favorite_list:
        return jsonify(favorite_list.serialize())
    else:
        return jsonify(message='Planet favorite list not found'), 404

@app.route('/planet-favorite-lists/<int:favorite_list_id>', methods=['PUT'])
def update_planet_favorite_list(favorite_list_id):
    favorite_list = Planet_Favorite_List.query.get(favorite_list_id)
    if not favorite_list:
        return jsonify(message='Planet favorite list not found'), 404

    data = request.get_json()
    favorite_list.planet_id = data.get('planet_id', favorite_list.planet_id)
    favorite_list.user_id = data.get('user_id', favorite_list.user_id)

    db.session.commit()

    return jsonify(message='Planet favorite list updated successfully', favorite_list=favorite_list.serialize())

@app.route('/planet-favorite-lists/<int:favorite_list_id>', methods=['DELETE'])
def delete_planet_favorite_list(favorite_list_id):
    favorite_list = Planet_Favorite_List.query.get(favorite_list_id)
    if favorite_list:
        db.session.delete(favorite_list)
        db.session.commit()
        return jsonify(message='Planet favorite list deleted successfully')
    else:
        return jsonify(message='Planet favorite list not found'), 404



# ... (definición de la clase Vehicle_Favorite_List)

@app.route('/vehicle-favorite-lists', methods=['GET'])
def get_vehicle_favorite_lists():
    favorite_lists = Vehicle_Favorite_List.query.all()
    return jsonify(favorite_lists=[favorite_list.serialize() for favorite_list in favorite_lists])

@app.route('/vehicle-favorite-lists', methods=['POST'])
def create_vehicle_favorite_list():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    user_id = data.get('user_id')

    new_vehicle_favorite_list = Vehicle_Favorite_List(vehicle_id=vehicle_id, user_id=user_id)
    db.session.add(new_vehicle_favorite_list)
    db.session.commit()

    return jsonify(message='Vehicle favorite list created successfully', favorite_list=new_vehicle_favorite_list.serialize()), 201

@app.route('/vehicle-favorite-lists/<int:favorite_list_id>', methods=['GET'])
def get_vehicle_favorite_list(favorite_list_id):
    favorite_list = Vehicle_Favorite_List.query.get(favorite_list_id)
    if favorite_list:
        return jsonify(favorite_list.serialize())
    else:
        return jsonify(message='Vehicle favorite list not found'), 404

@app.route('/vehicle-favorite-lists/<int:favorite_list_id>', methods=['PUT'])
def update_vehicle_favorite_list(favorite_list_id):
    favorite_list = Vehicle_Favorite_List.query.get(favorite_list_id)
    if not favorite_list:
        return jsonify(message='Vehicle favorite list not found'), 404

    data = request.get_json()
    favorite_list.vehicle_id = data.get('vehicle_id', favorite_list.vehicle_id)
    favorite_list.user_id = data.get('user_id', favorite_list.user_id)

    db.session.commit()

    return jsonify(message='Vehicle favorite list updated successfully', favorite_list=favorite_list.serialize())

@app.route('/vehicle-favorite-lists/<int:favorite_list_id>', methods=['DELETE'])
def delete_vehicle_favorite_list(favorite_list_id):
    favorite_list = Vehicle_Favorite_List.query.get(favorite_list_id)
    if favorite_list:
        db.session.delete(favorite_list)
        db.session.commit()




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)