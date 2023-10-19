$(document).ready(function() {
    $('.delete-button').click(function() {
        var ingredientId = $(this).data('ingredient-id');
        var confirmation = confirm("Are you sure you want to delete this ingredient?");
        if (confirmation) {
            $.ajax({
                url: '/delete_ingredient/' + ingredientId,
                type: 'POST',
                success: function(data) {
                    window.location.reload();
                }
            });
        }
    });
});






