from controllers import db



class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key=True)

    # Define relationships to access related records
    recipe = db.relationship('Recipe', backref='recipe_ingredients', foreign_keys=[recipe_id])
    ingredient = db.relationship('Ingredient', backref='recipe_ingredients', foreign_keys=[ingredient_id])