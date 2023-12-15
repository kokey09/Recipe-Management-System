// massRecover.js
$(document).ready(function() {
    // Select All functionality
    $("#select-all-button").on("click", function() {
        $(".checkbox").prop("checked", true);
        showMassRecoverButton();
    });

    // Checkbox click event
    $(".checkbox").on("click", function() {
        showSelectAllButton();
        showMassRecoverButton();
    });

    // Mass Recover button click event
    $("#mass-recover-button").on("click", function() {
        var selectedIds = [];
    
        // Get all checked checkboxes
        $(".checkbox:checked").each(function() {
            selectedIds.push($(this).attr("id").replace("checkbox-", ""));
        });
    
        if (selectedIds.length > 0) {
            // Confirm before performing mass recovery
            if (confirm('Are you sure you want to recover selected items?')) {
                // Perform mass recovery by sending selectedIds to the server
                $.ajax({
                    type: "POST",
                    url: "/mass_recover_recipes",
                    data: { ids: selectedIds },
                    success: function(response) {
                        // Clear all checkboxes
                        $(".checkbox:checked").prop("checked", false);
                        // Handle success, e.g., refresh the page or update the table
                        location.reload();
                    },
                    error: function(error) {
                        console.error("Error during mass recovery:", error);
                        // Handle error if needed
                    }
                });
            }
        }
    });

    // Function to show/hide Mass Recover button based on checkbox state
    function showMassRecoverButton() {
        var anyCheckboxChecked = $(".checkbox:checked").length > 0;
        $("#mass-recover-button").toggle(anyCheckboxChecked);
    }

    // Function to show/hide Select All button based on checkbox state
    function showSelectAllButton() {
        var anyCheckboxUnchecked = $(".checkbox:not(:checked)").length > 0;
        $("#select-all-button").toggle(anyCheckboxUnchecked);
    }
});
