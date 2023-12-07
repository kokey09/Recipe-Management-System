$(document).ready(function() {
    // Delegate the click event to a common parent container to handle dynamically added elements
    $(document).on("click", ".favorite-btn", function() {
        const recipeId = $(this).data("recipe-id");

        // Ask for confirmation
        if (confirm("Do you want to Add this recipe to your favorites?")) {
            addFavorite(recipeId);
        }
    });

    function addFavorite(recipeId) {
        const url = "/add_favorite?" + new Date().getTime();

        $.ajax({
            url: url,
            method: "POST",
            data: { recipe_id: recipeId },
            success: function(response) {
                handleAddFavoriteResponse(response);
            },
            error: function(error) {
                console.error("Error adding favorite", error);
            }
        });
    }
function handleAddFavoriteResponse(response) {
    const lowerCaseResponse = response.toLowerCase();

    if (lowerCaseResponse.includes("added successfully")) {
        showPopup("Favorite added successfully", "success");
    } else if (lowerCaseResponse.includes("already have this recipe as your favorite")) {
        showPopup("You already have this recipe as your favorite", "info");
    } else if (lowerCaseResponse.includes("restored from soft deletion")) {
        showPopup("Favorite added successfully (restored from soft deletion)");
    }
}

    function showPopup(message, type) {
        swal("Info", message, type);
    }
});

