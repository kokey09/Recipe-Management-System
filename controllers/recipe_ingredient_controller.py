from flask import  render_template, request, redirect, url_for, Blueprint,session,flash
from models.recipe_ingredient import RecipeIngredient
from models.recipe import Recipe
from models.ingredient import Ingredient


from models.recipe_ingredient import db


recipe_ingredient_bp = Blueprint('recipe_ingredient',__name__,template_folder='templates',static_folder='static')


@recipe_ingredient_bp.route('/recipe_ingredients')
def recipe_ingredients():
    if 'user_id' in session:
        recipe_ingredients_data = RecipeIngredient.query.all()
        recipes_data = Recipe.query.all()
        ingredients_data = Ingredient.query.all()

        return render_template(
            'recipe_ingredients.html',
            recipe_ingredients=recipe_ingredients_data,
            recipes=recipes_data,
            ingredients=ingredients_data,
        )
    else:
        flash('Please log in to access recipe ingredients.','error')
        return redirect(url_for('account_controller.login'))


@recipe_ingredient_bp.route('/connect_recipe_ingredient', methods=['POST'])
def connect_recipe_ingredient():
    if request.method == 'POST':
        recipe_id = request.form['recipe_id']
        ingredient_id = request.form['ingredient_id']

        try:
            # Create a new RecipeIngredient object and save it to the database
            new_recipe_ingredient = RecipeIngredient(recipe_id=recipe_id, ingredient_id=ingredient_id)
            db.session.add(new_recipe_ingredient)
            db.session.commit()

            return redirect(url_for('recipe_ingredients'))
        except Exception as e:
            print(f"Error connecting recipe and ingredient: {str(e)}")
            db.session.rollback()

    return redirect(url_for('recipe_ingredient.recipe_ingredients'))

@recipe_ingredient_bp.route('/disconnect_recipe_ingredient/<int:recipe_id>/<int:ingredient_id>', methods=['POST'])
def disconnect_recipe_ingredient(recipe_id, ingredient_id):
    if request.method == 'POST':
        recipe_ingredient_to_delete = RecipeIngredient.query.filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id).first()
        if recipe_ingredient_to_delete:
            db.session.delete(recipe_ingredient_to_delete)
            db.session.commit()
        return redirect(url_for('recipe_ingredient.recipe_ingredients'))

    return render_template('disconnect_confirmation.html', recipe_id=recipe_id, ingredient_id=ingredient_id)
