import os
from flask import Flask
from extensions import db, bcrypt, login_manager
from auth_routes import auth
from inventory_routes import inventory
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inventory.db')

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(inventory, url_prefix='/inventory')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
