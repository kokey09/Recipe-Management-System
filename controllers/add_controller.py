from flask import render_template, request, redirect, url_for, flash, jsonify, session, Blueprint,current_app

from werkzeug.utils import secure_filename

from models.ingredient import Ingredient
from models.account import Account
from models.account import db
from models.recipe import Recipe
from models.review import Review
from models.recipe_ingredient import RecipeIngredient
from models.favorites import Favorite
from datetime import datetime  # Import datetime

from flask_bcrypt import Bcrypt
import os
import logging

add_controller_bp = Blueprint('add_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()

@add_controller_bp.route('/add_review', methods=['POST'])
def add_review():
    if request.method == 'POST':
        # Retrieve the review data from the form
        review_text = request.form.get('review_text')
        rating = request.form.get('rating')
        image_file = request.files.get('image_file')

        account_id = None
        if 'user_id' in session:
            account_id = session['user_id']

        filename = None

        # Retrieve recipe_id from the query parameters
        recipe_id = request.args.get('recipe_id')

        if account_id and recipe_id:
            if image_file:
                filename = secure_filename(image_file.filename)
                image_directory = os.path.join(current_app.root_path, 'static', 'reviews-img-table')
                os.makedirs(image_directory, exist_ok=True)
                image_path = os.path.join(image_directory, filename)
                image_file.save(image_path)

            new_review = Review(recipe_id=recipe_id, account_id=account_id, review_text=review_text, rating=rating, image_url=f'static/reviews-img-table/{filename}' if filename else None)

            db.session.add(new_review)
            db.session.commit()

            return redirect(url_for('user_end_controller.recipe_instruction', recipe_id=recipe_id))
        else:
            flash('You must be logged in to submit a review or provide a valid recipe_id.', 'error')
            return redirect(url_for('authentication_controller.login'))
    else:
        return redirect(url_for('some_other_route'))


@add_controller_bp.route('/add_recipe', methods=['POST'])
def add_recipe():
    if request.method == 'POST':
        # Retrieve account_id and user type from the session
        account_id = session.get('user_id')

        if account_id:
            # Access form data
            recipe_name = request.form.get('recipe_name')
            instructions = request.form.get('instructions')
            image_file = request.files.get('image_file')

            # Retrieve user based on user_id from the session
            user = Account.query.get(account_id)

            if user:
                if image_file:
                    # Save the uploaded image to a directory
                    filename = secure_filename(image_file.filename)
                    image_directory = os.path.join(current_app.root_path, 'static', 'recipes-img-table')
                    os.makedirs(image_directory, exist_ok=True)  # Create the directory if it doesn't exist
                    image_path = os.path.join(image_directory, filename)
                    image_file.save(image_path)

                try:
                    # Create a new Recipe object and save it to the database with the image path and account_id
                    new_recipe = Recipe(
                        name=recipe_name,
                        instructions=instructions,
                        image_url=f'static/recipes-img-table/{filename}' if image_file else None,
                        account_id=account_id
                    )
                    db.session.add(new_recipe)
                    db.session.commit()

                    logging.info("Recipe added successfully")

                    # Redirect based on user type
                    if user.type == 'normal':
                        return redirect(url_for('user_end_controller.shared_recipe'))

                except Exception as e:
                    logging.error(f"Error adding recipe: {str(e)}")
                    db.session.rollback()

    return redirect(url_for('dashboard_controller.recipes'))


@add_controller_bp.route('/add-ingredient', methods=['POST'])
def add_ingredient():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        existing_ingredient = Ingredient.query.filter_by(name=name).first()
        if existing_ingredient is None:
            new_ingredient = Ingredient(name=name, description=description)
            db.session.add(new_ingredient)
            db.session.commit()

        return redirect(url_for('dashboard_controller.ingredients'))  # Change 'ingredients' to 'ingredient_controller.ingredients'


@add_controller_bp.route('/connect_recipe_ingredient', methods=['POST'])
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

    return redirect(url_for('dashboard_controller.recipe_ingredients'))





@add_controller_bp.route('/add_favorite', methods=['POST'])
def add_favorite():
    # Get the recipe_id from the form submission
    recipe_id = request.form.get('recipe_id')

    # Get the currently authenticated user
    user = get_authenticated_user()

    if not user:
        return redirect(url_for('authentication_controller.login'))

    # Check if the user has already favorited this recipe
    existing_favorite = Favorite.query.filter_by(recipe_id=recipe_id, account_id=user.id).first()

    if existing_favorite:
        return "you already have this recipe as your favorite"

    # Create a new Favorite record with the current timestamp
    favorite = Favorite(recipe_id=recipe_id, account_id=user.id, timestamp=datetime.utcnow())

    # Add the new Favorite record to the database
    db.session.add(favorite)
    db.session.commit()

    return "Favorite added successfully"


def get_authenticated_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return Account.query.get(user_id)