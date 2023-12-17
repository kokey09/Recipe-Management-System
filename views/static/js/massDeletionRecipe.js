// script.js
$(document).ready(function() {
    // Select All functionality
    $("#select-all-button").on("click", function() {
        $(".checkbox").prop("checked", true);
        showDeleteButton();
    });

    // Checkbox click event
    $(".checkbox").on("click", function() {
        showSelectAllButton();
        showDeleteButton();
    });

    // Delete Selected button click event
    $("#delete-selected-btn").on("click", function() {
        var selectedIds = [];
    
        // Get all checked checkboxes
        $(".checkbox:checked").each(function() {
            selectedIds.push($(this).attr("id").replace("checkbox-", ""));
        });
    
        if (selectedIds.length > 0) {
            // Confirm before performing mass deletion
            if (confirm('Are you sure you want to delete selected items?')) {
                // Perform mass deletion by sending selectedIds and userId to the server
                $.ajax({
                    type: "POST",
                    url: "/mass_recipe_deletion",
                    data: { 
                        ids: selectedIds,
                        deleted_by: userId  // Include the user's ID
                    },
                    success: function(response) {
                        // Handle success, e.g., refresh the page or update the table
                        location.reload();
                    },
                    error: function(error) {
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