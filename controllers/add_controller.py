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

def save_image_file(image_file, directory):
    filename = secure_filename(image_file.filename)
    image_directory = os.path.join(current_app.root_path, 'static', directory)
    os.makedirs(image_directory, exist_ok=True)
    image_path = os.path.join(image_directory, filename)
    image_file.save(image_path)
    return filename

@add_controller_bp.route('/add_review', methods=['POST'])
def add_review():

    if request.method == 'POST':

        user = get_authenticated_user()
        recipe_id = request.args.get('recipe_id')

        if not user or not recipe_id:
            return redirect(url_for('authentication_controller.login'))

        review_text = request.form.get('review_text')
        rating = request.form.get('rating')
        image_file = request.files.get('image_file')
        filename = save_image_file(image_file, 'reviews-img-table') if image_file else None

        new_review = Review(
            recipe_id=recipe_id,
            account_id=user.id,
            review_text=review_text,
            rating=rating,
            image_url=f'static/reviews-img-table/{filename}' if filename else None
        )

        db.session.add(new_review)
        db.session.commit()
        session['added_review'] = 'Thanks you for your feedback!'

    return redirect(url_for('user_end_controller.recipe_instruction', recipe_id=recipe_id))

@add_controller_bp.route('/add_recipe', methods=['POST'])
def add_recipe():
    if request.method == 'POST':

        user = get_authenticated_user()

        if not user:
            return redirect(url_for('authentication_controller.login'))

        recipe_name = request.form.get('recipe_name')
        instructions = request.form.get('instructions')
        image_file = request.files.get('image_file')
        filename = save_image_file(image_file, 'recipes-img-table') if image_file else None

        new_recipe = Recipe(
            name=recipe_name,
            instructions=instructions,
            image_url=f'static/recipes-img-table/{filename}' if filename else None,
            account_id=user.id
        )

        try:
            db.session.add(new_recipe)
            db.session.commit()
            session['added_recipe'] = "Recipe added successfully"
        except Exception as e:
            logging.error(f"Error adding recipe: {str(e)}")
            db.session.rollback()

        if user.type == 'normal':
            return redirect(url_for('user_end_controller.shared_recipe'))

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
            try:
                db.session.commit()
                session['added_ingredients'] = "Ingredient added successfully"
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error adding ingredient: {str(e)}")

    return redirect(url_for('dashboard_controller.ingredients')) 


@add_controller_bp.route('/connect_recipe_ingredient', methods=['POST'])
def connect_recipe_ingredient():
    if request.method == 'POST':
        
        recipe_id = request.form.get('recipe_id')
        ingredient_id = request.form.get('ingredient_id')

        new_recipe_ingredient = RecipeIngredient(recipe_id=recipe_id, ingredient_id=ingredient_id)
        db.session.add(new_recipe_ingredient)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error connecting recipe and ingredient: {str(e)}")

    return redirect(url_for('dashboard_controller.recipe_ingredients'))

@add_controller_bp.route('/add_favorite', methods=['POST'])
def add_favorite():
    notif = None

    if request.method == 'POST':
        
        recipe_id = request.form.get('recipe_id')
        user = get_authenticated_user()

        if not user or not recipe_id:
            return redirect(url_for('authentication_controller.login'))

        existing_favorite = Favorite.query.filter_by(recipe_id=recipe_id, account_id=user.id).first()

        if existing_favorite and existing_favorite.is_deleted:
            existing_favorite.is_deleted = False
            notif = "Favorite added successfully"
        elif existing_favorite:
            notif = "You already have this recipe as your favorite"
        else:
            favorite = Favorite(recipe_id=recipe_id, account_id=user.id, timestamp=datetime.utcnow())
            db.session.add(favorite)
            notif = "Favorite added successfully"

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding favorite: {str(e)}")
            notif = "Error adding favorite"

    return notif


def get_authenticated_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return Account.query.get(user_id)