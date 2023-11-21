from flask import  render_template, request, redirect, url_for, Blueprint,current_app,session,flash,make_response

from models.recipe import Recipe
from models.ingredient import Ingredient
from models.account import Account
from models.recipe_ingredient import RecipeIngredient
from models.review import Review

user_end_controller_bp = Blueprint('user_end_controller',__name__,template_folder='templates',static_folder='static')




@user_end_controller_bp.route('/')
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

    response = make_response(render_template('user_page.html', recipes=recipes, ingredients=ingredients, user=user, recipe_reviews_count=recipe_reviews_count))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@user_end_controller_bp.route('/about_us')
def about_us():
    ingredients = Ingredient.query.all()
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)
    response = make_response(render_template('about_us.html',ingredients=ingredients, user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@user_end_controller_bp.route('/ingredient_display')
def ingredient_display():
    ingredients = Ingredient.query.all()

    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    response = make_response (render_template('ingredient_display.html', ingredients=ingredients,user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@user_end_controller_bp.route('/recipe_display')
def recipe_display():
    ingredients = Ingredient.query.all()
    ingredient_id = request.args.get('ingredient_id', None)
    if ingredient_id:
        recipes = Recipe.query.join(Recipe.recipe_ingredients).join(RecipeIngredient.ingredient).filter(
            Ingredient.ingredient_id == ingredient_id).all()
    else:
        recipes = Recipe.query.all()

    # Load the number of reviews for each recipe
    recipe_reviews_count = {}  # Dictionary to store the counts

    for recipe in recipes:
        recipe_reviews_count[recipe.recipe_id] = len(Review.query.filter_by(recipe_id=recipe.recipe_id).all())

    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    response = make_response (render_template('recipe_display.html', recipes=recipes, ingredients=ingredients, user=user, recipe_reviews_count=recipe_reviews_count))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response



@user_end_controller_bp.route('/recipe_instruction')
def recipe_instruction():
    recipe_id = request.args.get('recipe_id', None, type=int)
    user = None

    recipe = Recipe.query.get_or_404(recipe_id)

    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    recipes = Recipe.query.filter_by(recipe_id=recipe_id).all()
    reviews = Review.query.filter_by(recipe_id=recipe_id).all()
    ingredients = Ingredient.query.all()
    recipe_reviews_count = len(reviews)

    response = make_response(render_template('recipe_instruction.html', recipes=recipes, ingredients=ingredients, user=user,
                             reviews=reviews, recipe_reviews_count=recipe_reviews_count, recipe=recipe))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@user_end_controller_bp.route('/user_profile_dashboard')
def user_profile_dashboard():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)
    else:
        flash('Please log in to access profile dashboard.', 'error')
        return redirect(url_for('authentication_controller.login'))
    response = make_response(render_template('user_profile_dashboard.html', user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@user_end_controller_bp.route('/user_add_recipe')
def user_add_recipe():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)
    else:
        flash('Please log in to access profile dashboard.', 'error')
        return redirect(url_for('authentication_controller.login'))

    response = make_response(render_template('user_add_recipe.html', user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@user_end_controller_bp.route('/shared_recipe')
def shared_recipe():
    recipes = Recipe.query.filter_by(is_deleted=False).order_by(Recipe.recipe_id.desc()).all()

    recipe_reviews_count = {}  # Dictionary to store the counts

    for recipe in recipes:
        recipe_reviews_count[recipe.recipe_id] = len(Review.query.filter_by(recipe_id=recipe.recipe_id).all())

    # Check if the user is logged in
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)
    else:
        flash('Please log in to access profile dashboard.', 'error')
        return redirect(url_for('authentication_controller.login'))

    response = make_response (render_template('shared_recipe.html', recipes=recipes, user=user, recipe_reviews_count=recipe_reviews_count))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response
