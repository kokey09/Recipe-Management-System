// base.js
document.addEventListener('DOMContentLoaded', function () {
    // JavaScript to check the current URL and open the details if it matches
    const currentURL = window.location.pathname;
    const ingredientsDetails = document.getElementById('ingredients-details');

    const recipeIngredientsDetails = document.getElementById('recipe-ingredients-details');

    if (currentURL === '/ingredients' || currentURL === '/recipes' || currentURL === '/recipe_ingredients') {
        ingredientsDetails.open = true;
        recipeIngredientsDetails.open = true;
    }
});


