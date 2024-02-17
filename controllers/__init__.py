from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail




import os
import cloudinary


db = SQLAlchemy()
mail = Mail()

cloudinary.config( 
  cloud_name = "dye3xqbdn", 
  api_key = "855798891421539", 
  api_secret = "j0nWfrODok-6Qf1KNASMcpePdyQ" 
)
 

print(os.getenv('CLOUDINARY_API_KEY'))

def create_app():

    app = Flask(__name__, 
                template_folder=os.path.join(os.getcwd(), 'views/templates'), 
                static_folder=os.path.join(os.getcwd(), 'views/static'))  # Create the Flask app instance here

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dashboard:dashboard@127.0.0.1/recipedb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STATIC_FOLDER'] = 'static'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  
    app.secret_key = os.getenv('SECRET_KEY')
    
  
    db.init_app(app)
    mail.init_app(app)


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


