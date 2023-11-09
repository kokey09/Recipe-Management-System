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

    from controllers.authentication_controller import authentication_controller_bp
    from controllers.edit_controller import edit_controller_bp
    from controllers.delete_controller import delete_controller_bp
    from controllers.add_controller import add_controller_bp
    from controllers.dashboard_controller import dashboard_controller_bp
    from controllers.user_end_controller import user_end_controller_bp

    app.register_blueprint(authentication_controller_bp)
    app.register_blueprint(edit_controller_bp)
    app.register_blueprint(delete_controller_bp)
    app.register_blueprint(add_controller_bp)
    app.register_blueprint(dashboard_controller_bp)
    app.register_blueprint(user_end_controller_bp)

    with app.app_context():
        db.create_all()

    return app


