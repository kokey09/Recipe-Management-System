function addReview() {
    const reviewOverlay = document.getElementById('reviewOverlay');
    const reviewPopup = document.getElementById('reviewPopup');

    reviewOverlay.style.display = 'block';
    reviewPopup.style.display = 'block';
}
function addRecipe() {
    const addRecipeOverlay = document.getElementById('addRecipeOverlay');
    const addRecipePopup = document.getElementById('addRecipePopup');

    addRecipeOverlay.style.display = 'block';
    addRecipePopup.style.display = 'block';
}

function repository() {
    const repositoryOverlay = document.getElementById('repositoryOverlay');
    const repositoryPopup = document.getElementById('repositoryPopup');

    repositoryOverlay.style.display = 'block';
    repositoryPopup.style.display = 'block';
}

function closeRepository() {
    const repositoryOverlay = document.getElementById('repositoryOverlay');
    const repositoryPopup = document.getElementById('repositoryPopup');

    repositoryOverlay.style.display = 'none';
    repositoryPopup.style.display = 'none';
}


function closeReview() {
    const reviewOverlay = document.getElementById('reviewOverlay');
    const reviewPopup = document.getElementById('reviewPopup');

    reviewOverlay.style.display = 'none';
    reviewPopup.style.display = 'none';
}

function closeAddRecipe() {
    const addRecipeOverlay = document.getElementById('addRecipeOverlay');
    const addRecipePopup = document.getElementById('addRecipePopup');
    const recipeForm = document.getElementById('recipeForm'); // Add the ID to your form

    addRecipeOverlay.style.display = 'none';
    addRecipePopup.style.display = 'none';

    recipeForm.reset();
}

function redirectToLogin() {
    const loginUrl = "/login";

    window.location.href = loginUrl;
}
