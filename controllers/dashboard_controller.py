from flask import  render_template, request, redirect, url_for, Blueprint,current_app,session,flash,make_response

from models.recipe import Recipe
from models.ingredient import Ingredient
from models.account import Account
from models.recipe_ingredient import RecipeIngredient
from models.review import Review

dashboard_controller_bp = Blueprint('dashboard_controller',__name__,template_folder='templates',static_folder='static')

@dashboard_controller_bp.route('/recipes')
def recipes():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            recipes_data = Recipe.query.all()
            return render_template('recipes.html', recipes=recipes_data, user=user)
        else:
            flash('User not found', 'error')
            return redirect(url_for('user_end_controller.user_page'))
    else:
        flash('Please log in to access recipes', 'error')
        return redirect(url_for('authentication_controller.login'))

@dashboard_controller_bp.route('/ingredients')
def ingredients():
    user = None

    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            ingredients_data = Ingredient.query.all()
            return render_template('ingredients.html', ingredients=ingredients_data,user=user)
        else:
            return redirect(url_for('user_end_controller.user_page'))
    else:
        flash('Please log in to access ingredients.','error')
        return redirect(url_for('authentication_controller.login'))

@dashboard_controller_bp.route('/recipe_ingredients')
def recipe_ingredients():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            recipes_data = Recipe.query.all()
            ingredients_data = Ingredient.query.all()
            recipe_ingredients_data = RecipeIngredient.query.all()

            return render_template(
                'recipe_ingredients.html',
                recipe_ingredients=recipe_ingredients_data,
                recipes=recipes_data,
                ingredients=ingredients_data,
                user=user
            )
        else:
            flash('You do not have access to view recipe ingredients', 'error')
            return redirect(url_for('user_end_controller.user_page'))
    else:
        flash('Please log in to access recipe ingredients', 'error')
        return redirect(url_for('authentication_controller.login'))

@dashboard_controller_bp.route('/reviews_dashboard')
def reviews_dashboard():
    reviews = Review.query.all()

    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            return render_template('reviews_dashboard.html', user=user, reviews=reviews)
        else:
            return redirect(url_for('user_end_controller.user_page'))

    else:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('authentication_controller.login'))

@dashboard_controller_bp.route('/accounts')
def accounts():
    accounts_data = Account.query.all()

    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            return render_template('accounts.html', accounts=accounts_data, user=user)
        else:
            flash('You do not have permission to access accounts.', 'error')
            return redirect(url_for('user_end_controller.user_page'))
    else:
        flash('Please log in to access accounts.', 'error')
        return redirect(url_for('authentication_controller.login'))

@dashboard_controller_bp.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            return render_template('dashboard.html', user=user)
        else:
            return redirect(url_for('user_end_controller.user_page'))

    else:
        flash('Please log in to access the dashboard', 'error')
        return redirect(url_for('authentication_controller.login'))