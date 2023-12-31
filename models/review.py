from controllers import db

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(512))
    date_created = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'), nullable=False)

    # Define a relationship to the Recipe model
    recipe = db.relationship('Recipe', backref='reviews')
    account = db.relationship('Account', backref='reviews')


