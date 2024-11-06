from flask import Flask
from extensions import db, bcrypt, login_manager
from auth_routes import auth  # Import auth blueprint
from inventory_routes import inventory  # Import inventory blueprint
from models import User  # Import User model to register with SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'

# Initialize extensions with the app instance
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirects unauthenticated users to 'auth.login'

# Define user_loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints with their URL prefixes
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(inventory, url_prefix='/inventory')

# Ensure tables are created within the application context
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
