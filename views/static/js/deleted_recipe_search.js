$(document).ready(function () {
    // Retrieve the saved search query and filter from localStorage
    const savedQuery = localStorage.getItem('deletedRecipeSearchQuery') || '';
    const savedFilter = localStorage.getItem('deletedRecipeSearchFilter') || 'all';

    // Set the saved query and filter in the corresponding elements
    $("#search-Input-recipe").val(savedQuery);
    $("#columnSelector").val(savedFilter);

    // Function to handle the search
    function handleSearch() {
        const query = $("#search-Input-recipe").val().toLowerCase();
        const filter = $("#columnSelector").val();

        // Save the current search query and filter to localStorage
        localStorage.setItem('deletedRecipeSearchQuery', query);
        localStorage.setItem('deletedRecipeSearchFilter', filter);

        $(".recipes-table tbody tr").each(function () {
            const row = $(this);
            let text = "";

            // Update the switch statement in handleSearch function
            switch (filter) {
                case "all":
                case "":
                    text = row.text().toLowerCase();
                    break;
                case "status":
                    text = row.find("td:nth-child(9)").text().toLowerCase(); // Update index for status
                    break;
                case "account_id":
                    text = row.find("td:nth-child(5)").text().toLowerCase(); // Update index for account_id
                    break;
                case "account_username":
                    text = row.find("td:nth-child(6)").text().toLowerCase(); // Update index for account_username
                    break;
                case "deleted_at":
                    text = row.find("td:nth-child(8)").text().toLowerCase(); // Update index for deleted_at
                    break;
                case "status_changed_at":
                    text = row.find("td:nth-child(10)").text().toLowerCase(); // Update index for status_changed_at
                    break;
                case "recipe_id":
                    text = row.find("td:nth-child(2)").text().toLowerCase(); // Update index for recipe_id
                    break;
                case "name":
                    text = row.find("td:nth-child(3)").text().toLowerCase(); // Update index for name
                    break;
                default:
                    const columnIndex = filter === "recipe_id" ? 2 : filter === "name" ? 3 : filter === "status" ? 9 : 5;
                    text = row.find("td:nth-child(" + columnIndex + ")").text().toLowerCase();
                    break;
            }

            if (text.includes(query)) {
                row.show();
            } else {
                row.hide();
            }
        });
    }

    // Initial search
    handleSearch();

    // Attach the handleSearch function to the input and select change events
    $("#search-Input-recipe, #columnSelector").on('input change', handleSearch);
});

function refreshSearch() {
    // Reset the select to the default value
    $("#columnSelector").val("all");

    // Clear the search input
    $("#search-Input-recipe").val("");

    // Trigger the search event to update the table
    $("#search-Input-recipe").trigger("input");
}
