from controllers import db


class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text)
    image_url = db.Column(db.String(512))
    is_deleted = db.Column(db.Boolean, default=False)
