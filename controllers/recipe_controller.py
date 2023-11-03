from flask import  render_template, request, redirect, url_for, Blueprint,current_app,session,flash
from werkzeug.utils import secure_filename
import os

from models.recipe import Recipe
from models.ingredient import Ingredient
from models.account import Account
from models.recipe_ingredient import RecipeIngredient
from models.review import Review
from models.recipe import db



recipe_controller_bp = Blueprint('recipe_controller',__name__,template_folder='templates',static_folder='static')


@recipe_controller_bp.route('/recipes')
def recipes():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

        if user and user.type == 'admin':
            recipes_data = Recipe.query.all()
            return render_template('recipes.html', recipes=recipes_data, user=user)
        else:
            flash('User not found', 'error')
            return redirect(url_for('ingredient_controller.user_page'))
    else:
        flash('Please log in to access recipes', 'error')
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
            image_directory = os.path.join(current_app.root_path, 'static', 'recipes-img-table')
            os.makedirs(image_directory, exist_ok=True)  # Create the directory if it doesn't exist
            image_path = os.path.join(image_directory, filename)
            image_file.save(image_path)

            try:
                # Create a new Recipe object and save it to the database with the image path
                new_recipe = Recipe(name=recipe_name, instructions=instructions, image_url=f'static/recipes-img-table/{filename}')
                db.session.add(new_recipe)
                db.session.commit()

                return redirect(url_for('recipe_controller_bp.recipes'))
            except Exception as e:
                print(f"Error adding recipe: {str(e)}")
                db.session.rollback()

    return redirect(url_for('recipe_controller.recipes'))


@recipe_controller_bp.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    if request.method == 'POST':
        recipe_to_delete = Recipe.query.get(id)
        if recipe_to_delete:
            try:
                db.session.delete(recipe_to_delete)
                db.session.commit()
                flash('Recipe deleted successfully', 'success')
            except Exception as e:
                flash('An error occurred while deleting the recipe', 'error')
        else:
            flash('Recipe not found', 'error')
    return redirect(url_for('recipe_controller.recipes'))


@recipe_controller_bp.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        instructions = request.form['instructions']
        image_file = request.files['image_file']
        filename = None  # Initialize filename to None

        if image_file:
            # Save the uploaded image to a directory
            filename = secure_filename(image_file.filename)
            image_directory = os.path.join(current_app.root_path, 'static', 'recipes-img-table')
            os.makedirs(image_directory, exist_ok=True)
            image_path = os.path.join(image_directory, filename)
            image_file.save(image_path)

        try:
            # Update the existing Recipe object with the new data and image path
            recipe = Recipe.query.get(id)
            recipe.name = recipe_name
            recipe.instructions = instructions
            if filename:  # Check if filename is not None
                recipe.image_url = f'static/recipes-img-table/{filename}'
            db.session.commit()
        except Exception as e:
            print(f"Error updating recipe: {str(e)}")
            db.session.rollback()

        return redirect(url_for('recipe_controller.recipes'))

    else:
        recipe = Recipe.query.get(id)
        return render_template('edit_recipes.html', recipe=recipe, id=id)

    return redirect(url_for('recipe_controller.recipes'))




@recipe_controller_bp.route('/recipe_instruction')
def recipe_instruction():
    recipe_id = request.args.get('recipe_id', None)  # Get the recipe_id from the query parameter
    user = None

    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    if recipe_id:
        # Filter recipes by the selected recipe_id
        recipes = Recipe.query.filter_by(recipe_id=recipe_id).all()
        if recipes:
            # Filter reviews by the selected recipe_id
            reviews = Review.query.filter_by(recipe_id=recipe_id).all()
            ingredients = Ingredient.query.all()
            # Calculate the number of reviews for the recipe
            recipe_reviews_count = len(reviews)

            return render_template('recipe_instruction.html', recipes=recipes, ingredients=ingredients, user=user,
                                   reviews=reviews, recipe_reviews_count=recipe_reviews_count)

    return "Recipe not found", 404  # Handle the case where the recipe_id is not found

@recipe_controller_bp.route('/recipe_display')
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

    return render_template('recipe_display.html', recipes=recipes, ingredients=ingredients, user=user, recipe_reviews_count=recipe_reviews_count)




@recipe_controller_bp.route('/recipe_review')
def recipe_review():
    recipe_id = request.args.get('recipe_id', type=int)  # Get the recipe_id from the query parameter
    if recipe_id is None:
        return "Recipe not found", 404

    recipe = Recipe.query.get(recipe_id)  # Retrieve the recipe based on recipe_id

    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = Account.query.get(user_id)

    return render_template('/recipe_review.html', recipe=recipe, user=user)




@recipe_controller_bp.route('/add_review/<int:recipe_id>', methods=['POST'])
def add_review(recipe_id):
    if request.method == 'POST':
        # Retrieve the review data from the form
        review_text = request.form.get('review_text')
        rating = request.form.get('rating')
        image_file = request.files.get('image_file')  # Access the uploaded file using get()

        account_id = None  # Initialize account_id to None
        # Check if the user is logged in
        if 'user_id' in session:
            account_id = session['user_id']  # Update to use account_id instead of user_id

        filename = None  # Initialize filename to None

        if account_id:
            # Save the uploaded image to a directory if provided
            if image_file:
                filename = secure_filename(image_file.filename)
                image_directory = os.path.join(current_app.root_path, 'static', 'reviews-img-table')
                os.makedirs(image_directory, exist_ok=True)  # Create the directory if it doesn't exist
                image_path = os.path.join(image_directory, filename)
                image_file.save(image_path)

            # Create a new Review object
            new_review = Review(recipe_id=recipe_id, account_id=account_id, review_text=review_text, rating=rating, image_url=f'static/reviews-img-table/{filename}' if filename else None)

            # Save the review to the database
            db.session.add(new_review)
            db.session.commit()

            return redirect(url_for('recipe_controller.recipe_instruction', recipe_id=recipe_id))
        else:
            # Handle the case where the user is not logged in
            flash('You must be logged in to submit a review.', 'error')
            return redirect(url_for('account_controller.login'))
    else:
        # Handle other HTTP methods if needed
        return redirect(url_for('some_other_route'))





