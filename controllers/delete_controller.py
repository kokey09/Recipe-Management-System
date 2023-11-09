from flask import render_template, request, redirect, url_for, flash, jsonify, session, Blueprint,current_app

from werkzeug.utils import secure_filename

from models.ingredient import Ingredient
from models.account import Account
from models.account import db
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from models.review import Review
from flask_bcrypt import Bcrypt
import os
import logging

delete_controller_bp = Blueprint('delete_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()

@delete_controller_bp.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    if request.method == 'POST':
        account_to_delete = Account.query.get(account_id)
        if account_to_delete:
            try:
                # Soft delete the account
                account_to_delete.is_deleted = True
                db.session.commit()
                flash('Account deleted successfully', 'success')
            except Exception as e:
                flash('An error occurred while soft deleting the account: ' + str(e), 'error')
        else:
            flash('Account not found', 'error')
    return redirect(url_for('dashboard_controller.accounts'))

@delete_controller_bp.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    if request.method == 'POST':
        recipe_to_delete = Recipe.query.get(id)
        if recipe_to_delete:
            try:
                # Instead of physically deleting the recipe, set a flag to mark it as deleted
                recipe_to_delete.is_deleted = True
                db.session.commit()
                flash('Recipe deleted successfully', 'success')
            except Exception as e:
                flash('An error occurred while deleting the recipe', 'error')
        else:
            flash('Recipe not found', 'error')
    return redirect(url_for('dashboard_controller.recipes'))

@delete_controller_bp.route('/delete_ingredient/<int:id>', methods=['POST'])
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
    return redirect(url_for('dashboard_controller.ingredients'))


@delete_controller_bp.route('/disconnect_recipe_ingredient/<int:recipe_id>/<int:ingredient_id>', methods=['POST'])
def disconnect_recipe_ingredient(recipe_id, ingredient_id):
    if request.method == 'POST':
        recipe_ingredient_to_delete = RecipeIngredient.query.filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id).first()
        if recipe_ingredient_to_delete:
            db.session.delete(recipe_ingredient_to_delete)
            db.session.commit()
        return redirect(url_for('dashboard_controller.recipe_ingredients'))

    return render_template('disconnect_confirmation.html', recipe_id=recipe_id, ingredient_id=ingredient_id)

