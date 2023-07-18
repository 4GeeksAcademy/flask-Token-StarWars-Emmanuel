import os
from flask_admin import Admin

from flask_admin.contrib.sqla import ModelView

from models import db, User, Address, Planet, Character, Vehicle, Character_Favorite_List, Planet_Favorite_List, Vehicle_Favorite_List

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Star Wars Flask REST API', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))

    
    # Add Address model to the admin
    admin.add_view(ModelView(Address, db.session))

     # Add Planet model to the admin
    admin.add_view(ModelView(Planet, db.session))

    # Add Character model to the admin
    admin.add_view(ModelView(Character, db.session))

    # Add Vehicle model to the admin
    admin.add_view(ModelView(Vehicle, db.session))

    # Add Character_Favorite_List model to the admin
    admin.add_view(ModelView(Character_Favorite_List, db.session))

      # Add Planet_Favorite_List model to the admin
    admin.add_view(ModelView(Planet_Favorite_List, db.session))

      # Add Vehicle_Favorite_List model to the admin
    admin.add_view(ModelView(Vehicle_Favorite_List, db.session))

    