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
//recipe
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search-Input");
    const recipesTable = document.querySelector(".recipes-table");
    const rows = recipesTable.querySelectorAll("tbody tr");

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();

        rows.forEach(function(row) {
            const recipeId = row.querySelector("td:nth-child(1)").textContent.toLowerCase();
            const recipeName = row.querySelector("td:nth-child(2)").textContent.toLowerCase();

            if (recipeId.includes(searchText) || recipeName.includes(searchText)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});


//recipe_ingredient
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const recipeIngredientTable = document.querySelector(".recipe-ingredient-table");
    const rows = recipeIngredientTable.querySelectorAll("tbody tr");

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();

        rows.forEach(function(row) {
            const rowText = row.textContent.toLowerCase();

            if (rowText.includes(searchText)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});


//ingredients
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput-ingredients");
    const ingredientsTable = document.querySelector(".ingredients-table");
    const rows = ingredientsTable.querySelectorAll("tbody tr");

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();

        rows.forEach(function(row) {
            const ingredientId = row.querySelector("td:nth-child(1)").textContent.toLowerCase();
            const ingredientName = row.querySelector("td:nth-child(2)").textContent.toLowerCase();

            if (ingredientId.includes(searchText) || ingredientName.includes(searchText)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});

// Accounts
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput-account");
    const accountTable = document.querySelector("table");
    const rows = accountTable.querySelectorAll("tbody tr");

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();

        rows.forEach(function(row) {
            // Get the account ID from the first column (td:nth-child(1))
            const accountId = row.querySelector("td:nth-child(1)").textContent.toLowerCase();

            if (accountId.includes(searchText)) {
                row.style.display = ""; // Show the table row
            } else {
                row.style.display = "none"; // Hide the table row
            }
        });
    });
});




