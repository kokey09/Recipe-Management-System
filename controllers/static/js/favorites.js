$(document).ready(function() {
    // Delegate the click event to a common parent container to handle dynamically added elements
    $(document).on("click", ".favorite-btn", function() {
        const recipeId = $(this).data("recipe-id");

        // Ask for confirmation
        if (confirm("Add this recipe to your favorites?")) {
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
        if (response === "Favorite added successfully") {
            showPopup("Favorite added successfully");
        } else if (response === "you already have this recipe as your favorite") {
            showPopup("You already have this recipe as your favorite");
        }
    }


    function showPopup(message) {
        alert(message);
        // You can customize this function to display a popup/modal or update the DOM
    }
});

