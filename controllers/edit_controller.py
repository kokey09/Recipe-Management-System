from flask import render_template, request, redirect, url_for, flash, jsonify, session, Blueprint,current_app
from datetime import datetime
from werkzeug.utils import secure_filename

from models.ingredient import Ingredient
from models.account import Account
from models.account import db
from models.recipe import Recipe
from models.review import Review
from flask_bcrypt import Bcrypt
import os
import json

edit_controller_bp = Blueprint('edit_controller',__name__,template_folder='templates',static_folder='static')
bcrypt = Bcrypt()

@edit_controller_bp.route('/edit_account/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    user = get_authenticated_user()

    if not user or user.type != 'admin':
        flash('You must be logged in as an admin to edit an account.', 'error')
        return redirect(url_for('authentication_controller.login'))

    account = Account.query.get(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if request.method == 'POST':
        account.type = request.form.get('type')
        is_deleted = request.form.get('is_deleted', '0') == '1'
        account.is_deleted = is_deleted

        db.session.commit()
        return redirect(url_for('dashboard_controller.accounts'))

    return render_template('edit_account.html', account=account, user=user)


#@edit_controller_bp.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
#def edit_recipe(id):
#    recipe = Recipe.query.get(id)
#    user = None

    # Check if the user is logged in
#    if 'user_id' in session:
#        user_id = session['user_id']
#        user = Account.query.get(user_id)

#    if request.method == 'POST':
#       is_deleted = request.form.get('is_deleted', '0') == '1'  # Get the is_deleted value as an integer
#        try:
#            recipe.is_deleted = bool(is_deleted)
#            db.session.commit()
#            flash("Recipe updated successfully.", "success")
#            return redirect(url_for('dashboard_controller.recipes'))

#       except Exception as e:
#            print(f"Error updating recipe: {str(e)}")
#            db.session.rollback()
#            flash("Error updating recipe. Please try again.", "error")

#    return render_template('edit_recipes.html', recipe=recipe, id=id, user=user)
HARMFUL_KEYWORDS = [
    'tae', 'lason', 'ewan', 'cyanide', 'mercury', 'lead', 'arsenic', 'raw meat',
    'rotten eggs', 'moldy cheese', 'spoiled milk', 'uncooked chicken', 'raw pork',
    'unwashed vegetables', 'expired canned goods', 'contaminated water', 'tainted seafood',
    'unpasteurized milk', 'unrefrigerated leftovers', 'bobo'
]

def save_image_file(image_file, directory):
    filename = secure_filename(image_file.filename)
    image_directory = os.path.join(current_app.root_path, '..', 'views', 'static', directory)
    os.makedirs(image_directory, exist_ok=True)
    image_path = os.path.join(image_directory, filename)
    image_file.save(image_path)
    return filename

@edit_controller_bp.route('/user_edit_recipe/<int:id>', methods=['GET', 'POST'])
def user_edit_recipe(id):
    recipe = Recipe.query.get(id)
    user = None

    # Check if the user is logged in
    user = get_authenticated_user()

    if user and recipe.account_id != user.id or recipe.is_deleted:
        session['notif'] = ("error","You do not have permission to edit this recipe.", "error")
        return redirect(url_for('user_end_controller.shared_recipe'))
    
    elif not user:
        return redirect(url_for('authentication_controller.login'))

    if request.method == 'POST':
        recipe.name = request.form.get('recipe_name')
        recipe.instructions = request.form.get('instructions')

        
        with open('views/static/json/harmful_keywords.json', 'r') as f:
            HARMFUL_KEYWORDS = json.load(f)

        if any(keyword in recipe.name.lower() for keyword in HARMFUL_KEYWORDS) or any(keyword in recipe.instructions.lower() for keyword in HARMFUL_KEYWORDS):
            session['harmful_array'] = "Recipe contains inappropriate content and cannot be updated."
            return redirect(url_for('user_end_controller.shared_recipe'))  # Redirect to an appropriate error page

        filename = None  # Initialize filename to None

        image_file = request.files.get('image_file')
        if image_file:
            filename = save_image_file(image_file, 'recipes-img-table')  # Use save_image_file function here

            recipe.image_url = f'static/recipes-img-table/{filename}'

        try:
            db.session.commit()
            session['notif'] = ("Added","Recipe updated successfully.", "success")
            return redirect(url_for('user_end_controller.shared_recipe'))
        except Exception as e:
            print(f"Error updating recipe: {str(e)}")
            db.session.rollback()
            flash("Error updating recipe. Please try again.", "error")
    return render_template('user_edit_recipe.html', recipe=recipe, id=id, user=user)


@edit_controller_bp.route('/edit_ingredient/<int:id>', methods=['GET', 'POST'])
def edit_ingredient(id):
    user = get_authenticated_user()

    if not user or user.type != 'admin':
        flash('You must be logged in as an admin to edit an ingredient.', 'error')
        return redirect(url_for('authentication_controller.login'))

    ingredient = Ingredient.query.get(id)

    if request.method == 'POST':
        # Update the ingredient's details based on the form data
        ingredient.name = request.form.get('name')
        ingredient.description = request.form.get('description')

        with open('views/static/json/harmful_keywords.json', 'r') as f:
            HARMFUL_KEYWORDS = json.load(f)

        if any(keyword in ingredient.name.lower() for keyword in HARMFUL_KEYWORDS) or any(keyword in ingredient.description.lower() for keyword in HARMFUL_KEYWORDS):
            session['harmful_array'] = "Recipe contains inappropriate content and cannot be updated."
            return redirect(url_for('dashboard_controller.ingredients'))

        db.session.commit()
        session['notif'] = ("Success","Ingredient updated successfully","success")
        return redirect(url_for('dashboard_controller.ingredients'))

    return render_template('edit_ingredients.html', ingredient=ingredient, id=id, user=user)


@edit_controller_bp.route('/change_status/<int:recipe_id>', methods=['POST'])
def change_status(recipe_id):
   
    recipe = Recipe.query.get_or_404(recipe_id) # Assuming you have a Recipe model with a status field
    # Update the status field based on the form data
    new_status = request.form.get('new_status')  # Adjust the actual field name
    recipe.status = new_status
    recipe.status_changed_at = db.func.current_timestamp()
   
    user = get_authenticated_user() # Add the current user's id to the status_changed_by field
    if user:
        recipe.status_changed_by = user.id
    # Save changes to the database
    db.session.commit()
    session['notif']  = ("Success","Recipe status updated successfully","success")
    # Redirect back to the deleted recipes page
    return redirect(url_for('dashboard_controller.recipes'))


@edit_controller_bp.route('/recover_recipe/<int:id>', methods=['POST'])
def recover_recipe(id):
    user = get_authenticated_user()
    recipe = Recipe.query.get_or_404(id)
    recipe.recovered_at = db.func.current_timestamp()
    recipe.is_deleted = False
    recipe.recovered_by = user.id  # Set the recovered_by field
    db.session.commit()
    session['notif'] = ("Recovered","Recipe recovered successfully","success")
    # Return a JSON response indicating success
    return jsonify({"message": "Recipe recovered successfully"})


@edit_controller_bp.route('/mass_recover_recipes', methods=['POST'])
def mass_recover_recipes():
    user = get_authenticated_user()

    selected_ids = request.form.getlist('ids[]')

    for recipe_id in selected_ids:
        recipe = Recipe.query.get_or_404(int(recipe_id))
        recipe.recovered_at = db.func.current_timestamp()
        recipe.is_deleted = False
        recipe.recovered_by = user.id  # Set the recovered_by field
        db.session.commit()
        session['notif'] = ("Recovered","Recipe recovered successfully","success")

    return jsonify({'message': 'Selected recipes recovered successfully'}), 200


def get_authenticated_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return Account.query.get(user_id)