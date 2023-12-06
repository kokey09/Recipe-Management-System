from flask import  render_template, request, redirect, url_for, Blueprint,current_app,session,flash,make_response,jsonify

from models.recipe import Recipe
from models.ingredient import Ingredient
from models.account import Account
from models.recipe_ingredient import RecipeIngredient
from models.review import Review
from models.account import db

dashboard_controller_bp = Blueprint('dashboard_controller',__name__,template_folder='templates',static_folder='static')

@dashboard_controller_bp.route('/recipes')
def recipes():
    user = get_authenticated_user()

    if not user:
        flash('Please log in to access recipes', 'error')
        return redirect(url_for('authentication_controller.login'))

    if user.type != 'admin':
        return redirect(url_for('user_end_controller.user_page'))

    recipes_data = Recipe.query.filter_by(is_deleted=False).all()
    response = make_response(render_template('recipes.html', recipes=recipes_data, user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@dashboard_controller_bp.route('/deleted_recipes')
def deleted_recipes():
    user = get_authenticated_user()

    if not user or user.type != 'admin':
        return redirect(url_for('user_end_controller.user_page'))

    deleted_recipes_data = Recipe.query.filter_by(is_deleted=True).all()
    return render_template('deleted_recipes.html', deleted_recipes=deleted_recipes_data, user=user)

@dashboard_controller_bp.route('/ingredients')
def ingredients():
    user = get_authenticated_user()

    if not user:
        flash('Please log in to access ingredients.','error')
        return redirect(url_for('authentication_controller.login'))

    if user.type != 'admin':
        return redirect(url_for('user_end_controller.user_page'))

    ingredients_data = Ingredient.query.all()
    response = make_response(render_template('ingredients.html', ingredients=ingredients_data,user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@dashboard_controller_bp.route('/recipe_ingredients')
def recipe_ingredients():
    user = get_authenticated_user()

    if not user:
        flash('Please log in to access recipe ingredients', 'error')
        return redirect(url_for('authentication_controller.login'))

    if user.type != 'admin':
        flash('You do not have access to view recipe ingredients', 'error')
        return redirect(url_for('user_end_controller.user_page'))

    recipes_data = Recipe.query.all()
    ingredients_data = Ingredient.query.all()
    recipe_ingredients_data = RecipeIngredient.query.all()

    response = make_response(render_template(
        'recipe_ingredients.html',
        recipe_ingredients=recipe_ingredients_data,
        recipes=recipes_data,
        ingredients=ingredients_data,
        user=user
    ))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@dashboard_controller_bp.route('/reviews_dashboard')
def reviews_dashboard():
    user = get_authenticated_user()

    if not user:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('authentication_controller.login'))

    if user.type != 'admin':
        return redirect(url_for('user_end_controller.user_page'))

    reviews = Review.query.all()
    response = make_response(render_template('reviews_dashboard.html', user=user, reviews=reviews))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@dashboard_controller_bp.route('/accounts')
def accounts():
    user = get_authenticated_user()

    if not user:
        flash('Please log in to access accounts.', 'error')
        return redirect(url_for('authentication_controller.login'))

    if user.type != 'admin':
        flash('You do not have permission to access accounts.', 'error')
        return redirect(url_for('user_end_controller.user_page'))

    accounts_data = Account.query.all()
    response = make_response(render_template('accounts.html', accounts=accounts_data, user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@dashboard_controller_bp.route('/dashboard')
def dashboard():
    user = get_authenticated_user()

    if not user:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('authentication_controller.login'))

    if user.type != 'admin':
        return redirect(url_for('user_end_controller.user_page'))

    response = make_response(render_template('dashboard.html', user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@dashboard_controller_bp.route('/recipe_preview')
def recipe_preview():
    recipe_id = request.args.get('recipe_id', None, type=int)

    user = get_authenticated_user()

    if not user:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('authentication_controller.login'))

    if user.type != 'admin':
        return redirect(url_for('user_end_controller.user_page'))

    recipe = Recipe.query.get(recipe_id)
    return render_template('recipe_preview.html', id=recipe_id, recipe=recipe,user=user)

def get_authenticated_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return Account.query.get(user_id)