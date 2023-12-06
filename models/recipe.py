from controllers import db
from sqlalchemy import Enum
from datetime import datetime


class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text)
    image_url = db.Column(db.String(512))
    is_deleted = db.Column(db.Boolean, default=False)  # Define is_deleted as a boolean column
    created_at = db.Column(db.DateTime, nullable=False,server_default=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    recovered_at = db.Column(db.DateTime, nullable=True, default=None)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    status = db.Column(Enum('pending', 'declined', 'approved', name='status_enum'), default='pending', nullable=False)
    status_changed_at = db.Column(db.DateTime, nullable=False, default=None)

    account = db.relationship('Account', backref='recipes')

