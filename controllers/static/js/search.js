// user base or page

document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const recipeList = document.querySelector(".recipe-list");
    const recipeItems = recipeList.querySelectorAll("li");

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();

        for (const recipeItem of recipeItems) {
            const recipeName = recipeItem.textContent.toLowerCase();
            if (recipeName.includes(searchText)) {
                recipeItem.style.display = "block";
            } else {
                recipeItem.style.display = "none";
            }
        }
    });
});

// ingredient display
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const ingredientList = document.querySelector(".ingredients-list");
    const ingredientItems = ingredientList.querySelectorAll("li");

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();

        for (const ingredientItem of ingredientItems) {
            const ingredientName = ingredientItem.textContent.toLowerCase();
            if (ingredientName.includes(searchText)) {
                ingredientItem.style.display = "block";
            } else {
                ingredientItem.style.display = "none";
            }
        }
    });
});

//recipe display
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const recipeList = document.querySelector(".recipe-list");
    const recipeItems = recipeList.querySelectorAll("li");

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();

        for (const recipeItem of recipeItems) {
            const recipeName = recipeItem.textContent.toLowerCase();
            if (recipeName.includes(searchText)) {
                recipeItem.style.display = "block";
            } else {
                recipeItem.style.display = "none";
            }
        }
    });
});













