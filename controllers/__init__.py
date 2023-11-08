from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy()

def create_app():

    app = Flask(__name__)  # Create the Flask app instance here

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dashboard:dashboard@127.0.0.1/recipedb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STATIC_FOLDER'] = 'static'
    app.secret_key = 'your_secret_key'

    db.init_app(app)

    # Import blueprints within the create_app function to avoid circular imports
    from controllers.ingredient_controller import ingredient_controller_bp
    from controllers.recipe_controller import recipe_controller_bp
    from controllers.account_controller import account_controller_bp
    from controllers.recipe_ingredient_controller import recipe_ingredient_bp

    app.register_blueprint(ingredient_controller_bp)
    app.register_blueprint(recipe_controller_bp)
    app.register_blueprint(account_controller_bp)
    app.register_blueprint(recipe_ingredient_bp)


    with app.app_context():
        db.create_all()

    return app


