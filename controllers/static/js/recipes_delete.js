$(document).ready(function() {
    $('.delete-button').click(function() {
        var recipeId = $(this).data('recipe-id');
        var confirmation = confirm("Are you sure you want to delete this recipe?");
        if (confirmation) {
            $.ajax({
                url: '/delete_recipe/' + recipeId, // Update the URL to match your Flask route
                type: 'POST',
                success: function(data) {
                    window.location.reload();
                }
            });
        }
    });
});