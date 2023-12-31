// ingredients.js
$(document).ready(function () {
    // Select All functionality
    $("#select-all-button").on("click", function () {
        $(".checkbox").prop("checked", true);
        showDeleteButton();
    });

    // Checkbox click event
    $(".checkbox").on("click", function () {
        showSelectAllButton();
        showDeleteButton();
    });

    // Delete Selected button click event for Ingredients
    $("#delete-selected-btn").on("click", function () {
        var selectedIds = [];

        // Get all checked checkboxes
        $(".checkbox:checked").each(function () {
            selectedIds.push($(this).data("ingredient-id"));
        });

        if (confirm('Are you sure you want to delete selected items?')) {
            if (selectedIds.length > 0) {
                // Perform mass deletion by sending selectedIds to the server
                $.ajax({
                    type: "POST",
                    url: "/mass_delete_ingredients",
                    data: { ids: selectedIds },
                    success: function (response) {
                        // Handle success, e.g., refresh the page or update the table
                        location.reload();
                    },
                    error: function (error) {
                        console.error("Error during mass deletion:", error);
                        // Handle error if needed
                    }
                });
            }
        }
    });

    // Function to show/hide Delete Selected button based on checkbox state
    function showDeleteButton() {
        var anyCheckboxChecked = $(".checkbox:checked").length > 0;
        $("#delete-selected-btn").toggle(anyCheckboxChecked);
    }

    // Function to show/hide Select All button based on checkbox state
    function showSelectAllButton() {
        var anyCheckboxUnchecked = $(".checkbox:not(:checked)").length > 0;
        $("#select-all-button").toggle(anyCheckboxUnchecked);
    }
});
