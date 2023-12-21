// dynamic js codes
// recipes and  shared_recipes html
$(document).ready(function () {
    // Function to delete a recipe
    function deleteRecipe(recipeId) {
        $.ajax({
            type: "POST",
            url: `/delete_recipe_admin/${recipeId}`,
            success: function (response) {
                // Assuming that the response contains a message
                alert(response);
                // Assuming that you want to reload the page after deletion
                location.reload();
            },
            error: function (error) {
                alert("Error deleting recipe");
            }
        });
    }

    // Event listener for delete buttons
    $(".delete-recipe-btn").click(function () {
        // Extract the recipe ID from the button's data attribute
        var recipeId = $(this).data("recipe-id");

        // Confirm before deletion
        if (confirm("Are you sure you want to delete this recipe?")) {
            // Call the deleteRecipe function
            deleteRecipe(recipeId);
        }
    });
});


// ________________________________________________________________________________________________________________


// deleted_recipe html
$(document).ready(function () {
    // Function to recover a recipe
    function recoverRecipe(recipeId) {
        $.ajax({
            type: "POST",
            url: `/recover_recipe/${recipeId}`,
            success: function (response) {
                // Assuming that the response contains a message
                alert(response);
                // Assuming that you want to reload the page after recovery
                location.reload();
            },
            error: function (error) {
                alert("Error recovering recipe");
            }
        });
    }

    // Event listener for recover buttons using event delegation
    $(document).on("click", ".recover-recipe-btn", function () {
        // Extract the recipe ID from the button's data attribute
        var recipeId = $(this).data("recipe-id");

        // Confirm before recovery
        if (confirm('Do you want to recover this recipe?')) {
            // Call the recoverRecipe function
            recoverRecipe(recipeId);
        }
    });
});

// ________________________________________________________________________________________________________________

// images required recipe.html
$(document).ready(function() {
    $('#submit-button').click(function(e) {
        if ($('#image_file').get(0).files.length === 0) {
            e.preventDefault();
            $('#file-error').show();
        }
    });
});

