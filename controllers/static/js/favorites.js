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
        showPopup("Success","Favorite added successfully", "success");
    } else if (lowerCaseResponse.includes("already have this recipe as your favorite")) {
        showPopup("Info","You already have this recipe as your favorite", "info");
    } else if (lowerCaseResponse.includes("restored from soft deletion")) {
        showPopup("Info","Favorite added successfully (restored from soft deletion)","info");
    }
}

    function showPopup(type,message, type) {
        swal(type, message, type);
    }
});

