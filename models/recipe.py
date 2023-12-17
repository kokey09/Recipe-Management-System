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
    deleted_by = db.Column(db.Integer, db.ForeignKey('account.id'))  # New column
    recovered_at = db.Column(db.DateTime, nullable=True, default=None)
    recovered_by = db.Column(db.Integer, db.ForeignKey('account.id'))  # New column

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    status = db.Column(Enum('pending', 'declined', 'approved', name='status_enum'), default='pending', nullable=False)
    status_changed_at = db.Column(db.DateTime, nullable=False, default=None)
    status_changed_by = db.Column(db.Integer, db.ForeignKey('account.id'))

    account = db.relationship('Account', foreign_keys=[account_id], backref='created_recipes')
    status_changer = db.relationship('Account', foreign_keys=[status_changed_by], backref='status_changes')
    deleter = db.relationship('Account', foreign_keys=[deleted_by], backref='deleted_recipes')  # New relationship
    recoverer = db.relationship('Account', foreign_keys=[recovered_by], backref='recovered_recipes')  # New relationship

