from flask import  render_template, request, redirect, url_for, Blueprint,current_app,session,flash
from werkzeug.utils import secure_filename
import os

from models.recipe import Recipe
from models.ingredient import Ingredient
from models.account import Account
from models.recipe_ingredient import RecipeIngredient


from models.recipe import db


recipe_controller_bp = Blueprint('recipe_controller',__name__,template_folder='templates',static_folder='static')


@recipe_controller_bp.route('/recipes')
def recipes():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)
        recipes_data = Recipe.query.all()
        return render_template('recipes.html', recipes=recipes_data, user=user)
    else:
        flash('Please log in to access recipes.','error')
        return redirect(url_for('account_controller.login'))


@recipe_controller_bp.route('/add_recipe', methods=['POST'])
def add_recipe():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        instructions = request.form['instructions']
        image_file = request.files['image_file']  # Access the uploaded file

        if image_file:
            # Save the uploaded image to a directory
            filename = secure_filename(image_file.filename)
            image_directory = os.path.join(current_app.config['STATIC_FOLDER'], 'img-db')
            os.makedirs(image_directory, exist_ok=True)  # Create the directory if it doesn't exist
            image_path = os.path.join(image_directory, filename)
            image_file.save(image_path)

            try:
                # Create a new Recipe object and save it to the database with the image_path
                new_recipe = Recipe(name=recipe_name, instructions=instructions, image_url=image_path)
                db.session.add(new_recipe)
                db.session.commit()

                return redirect(url_for('recipe_controller_bp.recipes'))
            except Exception as e:
                print(f"Error adding recipe: {str(e)}")
                db.session.rollback()

    return redirect(url_for('recipe_controller.recipes'))



@recipe_controller_bp.route('/delete_recipe/<int:id>', methods=['GET', 'POST'])
def delete_recipe(id):
    if request.method == 'POST':
        recipe_to_delete = Recipe.query.get(id)  # Use Recipe.query.get(id) to get the recipe
        if recipe_to_delete:
            db.session.delete(recipe_to_delete)
            db.session.commit()
        return redirect(url_for('recipe_controller.recipes'))


@recipe_controller_bp.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get(id)

    if request.method == 'POST':
        # Update the recipe's details based on the form data
        recipe.name = request.form['name']
        recipe.instructions = request.form['instructions']

        # Check if a new image file is uploaded
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                # Save the uploaded image file and update the image URL
                filename = secure_filename(image_file.filename)
                image_directory = os.path.join(current_app.config['STATIC_FOLDER'], 'img-db')
                os.makedirs(image_directory, exist_ok=True)  # Create the directory if it doesn't exist
                image_path = os.path.join(image_directory, filename)
                image_file.save(image_path)
                recipe.image_url = f'static/img-db/{filename}'

        db.session.commit()
        return redirect(url_for('recipe_controller.recipes'))

    return render_template('edit_recipes.html', recipe=recipe, id=id)

@recipe_controller_bp.route('/recipe_instruction')
def recipe_instruction():
    recipe_name = request.args.get('recipe_name', None)
    ingredients = Ingredient.query.all()
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    if recipe_name:
        # Filter recipes by the selected recipe name
        recipes = Recipe.query.join(Recipe.recipe_ingredients).join(RecipeIngredient.ingredient).filter(
            Recipe.name == recipe_name).all()

        if recipes:
            return render_template('recipe_instruction.html', recipes=recipes,ingredients=ingredients, user=user)

    return "Recipe not found", 404  # Handle the case where the recipe name is not found