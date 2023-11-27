from controllers import db

class Favorite(db.Model):
    __tablename__ = 'favorites'
    favorite_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    recipe = db.relationship('Recipe', backref='favorites')
    account = db.relationship('Account', backref='favorites')