from flask import  render_template, request, redirect, url_for,  Blueprint,session,flash
from models.recipe_ingredient import RecipeIngredient

from models.recipe import Recipe
from models.ingredient import Ingredient
from models.account import Account
from models.review import Review
from models.ingredient import db




ingredient_controller_bp = Blueprint('ingredient_controller', __name__, template_folder='templates',static_folder='static')

@ingredient_controller_bp.route('/ingredients')
def ingredients():
    user = None

    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            ingredients_data = Ingredient.query.all()
            return render_template('ingredients.html', ingredients=ingredients_data,user=user)
        else:
            return redirect(url_for('ingredient_controller.user_page'))
    else:
        flash('Please log in to access ingredients.','error')
        return redirect(url_for('account_controller.login'))


@ingredient_controller_bp.route('/ingredient_display')
def ingredient_display():
    ingredients = Ingredient.query.all()

    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    return render_template('ingredient_display.html', ingredients=ingredients,user=user)

@ingredient_controller_bp.route('/add-ingredient', methods=['POST'])
def add_ingredient():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        new_ingredient = Ingredient(name=name, description=description)
        db.session.add(new_ingredient)
        db.session.commit()

        return redirect(url_for('ingredient_controller.ingredients'))  # Change 'ingredients' to 'ingredient_controller.ingredients'


@ingredient_controller_bp.route('/delete_ingredient/<int:id>', methods=['POST'])
def delete_ingredient(id):
    if request.method == 'POST':
        ingredient_to_delete = Ingredient.query.get(id)
        if ingredient_to_delete:
            try:
                db.session.delete(ingredient_to_delete)
                db.session.commit()
                flash('Ingredient deleted successfully', 'success')
            except Exception as e:
                flash('An error occurred while deleting the ingredient', 'error')
        else:
            flash('Ingredient not found', 'error')
    return redirect(url_for('ingredient_controller.ingredients'))


@ingredient_controller_bp.route('/edit_ingredient/<int:id>', methods=['GET', 'POST'])
def edit_ingredient(id):
    ingredient = Ingredient.query.get(id)

    if request.method == 'POST':
        # Update the ingredient's details based on the form data
        ingredient.name = request.form['name']
        ingredient.description = request.form['description']

        db.session.commit()
        return redirect(url_for('ingredient_controller.ingredients'))

    return render_template('edit_ingredients.html', ingredient=ingredient, id=id)




@ingredient_controller_bp.route('/')
def user_page():
    ingredients = Ingredient.query.all()
    recipes = Recipe.query.filter_by(is_deleted=False).order_by(Recipe.recipe_id.desc()).all()

    recipe_reviews_count = {}  # Dictionary to store the counts

    for recipe in recipes:
        recipe_reviews_count[recipe.recipe_id] = len(Review.query.filter_by(recipe_id=recipe.recipe_id).all())

    # Check if the user is logged in
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    return render_template('/user_page.html', recipes=recipes, ingredients=ingredients, user=user, recipe_reviews_count=recipe_reviews_count)


@ingredient_controller_bp.route('/about_us')
def about_us():
    ingredients = Ingredient.query.all()
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)
    return render_template('about_us.html',ingredients=ingredients, user=user)



