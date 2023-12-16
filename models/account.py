from datetime import datetime
from flask_bcrypt import Bcrypt
from controllers import db  # Assuming you've defined the 'db' instance in a separate file
from models.review import Review
from sqlalchemy import Enum

bcrypt = Bcrypt()  # Initialize bcrypt

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(20), nullable=False, default='normal')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(Enum('unverified', 'verified', name='status_enum'), default='unverified', nullable=False)

def create_default_admin(app):
    with app.app_context():
        default_admin = Account.query.filter_by(username='admin').first()
        if not default_admin:
            # Hash the default admin's password
            admin_password = 'admin'  # You can set your desired default admin password
            hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')

            # Create the default admin account
            default_admin = Account(username='admin', email='admin@gmail.com', password=hashed_password, type='admin', status='verified')
            db.session.add(default_admin)
            db.session.commit()





