from flask import render_template, request, redirect, url_for, flash, session, Blueprint,jsonify
from datetime import datetime

from models.ingredient import Ingredient
from models.account import Account
from models.account import db
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from models.favorites import Favorite

from flask_bcrypt import Bcrypt



delete_controller_bp = Blueprint('delete_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()
# delete account
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




# delete main function
def delete_recipe_base(model, id, redirect_page):
    user = get_authenticated_user()

    if request.method == 'POST' and user:
        # Include the logic for retrieving the entity based on the model type
        if model == 'recipe':
            entity_to_delete = Recipe.query.get(id)
        else:
            entity_to_delete = None

        if entity_to_delete:
            try:
                entity_to_delete.deleted_at = db.func.current_timestamp()
                entity_to_delete.is_deleted = True
                db.session.commit()
                session['deleted_recipe'] = "deleted successfully"
                return jsonify({'message': f'{model.capitalize()} deleted successfully'}), 200
            except Exception as e:
                return jsonify({'error': f'Internal server error: {str(e)}'}), 500

        return jsonify({'error': f'{model.capitalize()} not found'}), 404

    return jsonify({'error': 'Invalid request'}), 400




# delete main function extension for admin
@delete_controller_bp.route('/delete_recipe_admin/<int:id>', methods=['POST'])
def delete_recipe_admin(id):
    return delete_recipe_base('recipe', id, 'dashboard_controller.recipes')




# delete main function extension for user end
@delete_controller_bp.route('/delete_shared_recipe/<int:id>', methods=['POST'])
def delete_shared_recipe(id):
    result = delete_recipe_base('recipe', id, 'user_end_controller.shared_recipe')
    if isinstance(result, tuple) and len(result) == 2 and result[1] == 200:
        return redirect(url_for('user_end_controller.shared_recipe'))
    return result




@delete_controller_bp.route('/mass_recipe_deletion', methods=['POST'])
def mass_recipe_deletion():
    selected_ids = request.form.getlist('ids[]')

    for recipe_id in selected_ids:
        delete_recipe_base('recipe', int(recipe_id), 'dashboard_controller.recipes')

    return jsonify({'message': 'Selected recipes deleted successfully'}), 200





@delete_controller_bp.route('/delete_ingredient/<int:id>', methods=['POST'])
def delete_ingredient(id):
    if request.method == 'POST':
        ingredient_to_delete = Ingredient.query.get(id)
        if ingredient_to_delete:
            try:
                db.session.delete(ingredient_to_delete)
                db.session.commit()
                session['deleted_ingredients'] = "deleted successfully"
                
            except Exception as e:
                session['error'] = "you cannot delete this ingredients, please disconnect it first on recipe ingredients"
        else:
            flash('Ingredient not found', 'error')
    return redirect(url_for('dashboard_controller.ingredients'))





@delete_controller_bp.route('/mass_delete_ingredients', methods=['POST'])
def mass_delete_ingredients():
    if request.method == 'POST':
        selected_ids = request.form.getlist('ids[]')
        try:
            Ingredient.query.filter(Ingredient.ingredient_id.in_(selected_ids)).delete(synchronize_session='fetch')
            db.session.commit()
            flash('Ingredients deleted successfully', 'success')
        except Exception as e:
            flash('An error occurred while deleting ingredients', 'error')

    return jsonify({"message": "Ingredients deleted successfully"})





@delete_controller_bp.route('/delete_favorite/<int:id>', methods=['POST'])
def delete_favorite(id):
    if request.method == 'POST':
        favorite_to_delete = Favorite.query.get(id)
        if favorite_to_delete:
            try:
                # Soft delete the favorite
                favorite_to_delete.is_deleted = True
                db.session.commit()
                flash('Favorite deleted successfully', 'success')
            except Exception as e:
                flash('An error occurred while soft deleting the favorite: ' + str(e), 'error')
        else:
            flash('Favorite not found', 'error')
    return redirect(url_for('user_end_controller.favorites'))



@delete_controller_bp.route('/disconnect_recipe_ingredient/<int:recipe_id>/<int:ingredient_id>', methods=['POST'])
def disconnect_recipe_ingredient(recipe_id, ingredient_id):
    if request.method == 'POST':
        recipe_ingredient_to_delete = RecipeIngredient.query.filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id).first()
        if recipe_ingredient_to_delete:
            db.session.delete(recipe_ingredient_to_delete)
            db.session.commit()
        return redirect(url_for('dashboard_controller.recipe_ingredients'))

    return render_template('disconnect_confirmation.html', recipe_id=recipe_id, ingredient_id=ingredient_id)





def get_authenticated_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return Account.query.get(user_id)
    else:
        flash('You need to log in first', 'error')
        return None