from flask import render_template, request, redirect, url_for, flash, jsonify, session, Blueprint,current_app

from werkzeug.utils import secure_filename

from models.ingredient import Ingredient
from models.account import Account
from models.account import db
from models.recipe import Recipe
from models.review import Review
from flask_bcrypt import Bcrypt
import os
import logging


edit_controller_bp = Blueprint('edit_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()

@edit_controller_bp.route('/edit_account/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    account = Account.query.get(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if request.method == 'POST':
        account.username = request.form.get('username')
        account.email = request.form.get('email')
        account.type = request.form.get('type')
        account.is_deleted = request.form.get('is_deleted')
        is_deleted = request.form.get('is_deleted', '0') == '1'
        account.is_deleted = is_deleted

        if 'password' in request.form:
            new_password = request.form['password']
            # Rehash the new password and update it in the database
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            account.password = hashed_password

        db.session.commit()
        return redirect(url_for('dashboard_controller.accounts'))

    return render_template('edit_account.html', account=account)

@edit_controller_bp.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get(id)
    user = None

    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    if request.method == 'POST':
        is_deleted = request.form.get('is_deleted', '0') == '1'  # Get the is_deleted value as an integer
        try:
            recipe.is_deleted = bool(is_deleted)
            db.session.commit()
            flash("Recipe updated successfully.", "success")
            return redirect(url_for('dashboard_controller.recipes'))

        except Exception as e:
            print(f"Error updating recipe: {str(e)}")
            db.session.rollback()
            flash("Error updating recipe. Please try again.", "error")

    return render_template('edit_recipes.html', recipe=recipe, id=id, user=user)

@edit_controller_bp.route('/user_edit_recipe/<int:id>', methods=['GET', 'POST'])
def user_edit_recipe(id):
    recipe = Recipe.query.get(id)
    user = None

    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and recipe.account_id != user_id or recipe.is_deleted:
            flash("You do not have permission to edit this recipe.", "error")
            return redirect(url_for('user_end_controller.shared_recipe'))

    if request.method == 'POST':
        recipe.name = request.form.get('recipe_name')
        recipe.instructions = request.form.get('instructions')
        filename = None  # Initialize filename to None

        image_file = request.files.get('image_file')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static', 'recipes-img-table', filename)
            image_file.save(image_path)
            recipe.image_url = f'static/recipes-img-table/{filename}'

        try:
            db.session.commit()
            flash("Recipe updated successfully.", "success")
            return redirect(url_for('user_end_controller.shared_recipe'))
        except Exception as e:
            print(f"Error updating recipe: {str(e)}")
            db.session.rollback()
            flash("Error updating recipe. Please try again.", "error")
    return render_template('user_edit_recipe.html', recipe=recipe, id=id, user=user)


@edit_controller_bp.route('/edit_ingredient/<int:id>', methods=['GET', 'POST'])
def edit_ingredient(id):
    ingredient = Ingredient.query.get(id)

    if request.method == 'POST':
        # Update the ingredient's details based on the form data
        ingredient.name = request.form.get('name')
        ingredient.description = request.form.get('description')

        db.session.commit()
        return redirect(url_for('dashboard_controller.ingredients'))

    return render_template('edit_ingredients.html', ingredient=ingredient, id=id)