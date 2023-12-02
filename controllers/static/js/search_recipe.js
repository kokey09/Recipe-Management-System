$(document).ready(function () {
    // Retrieve the saved search query and filter from localStorage
    const savedQuery = localStorage.getItem('recipeSearchQuery') || '';
    const savedFilter = localStorage.getItem('recipeSearchFilter') || 'all';

    // Set the saved query and filter in the corresponding elements
    $("#search-Input-recipe").val(savedQuery);
    $("#columnSelector").val(savedFilter);

    // Function to handle the search
    function handleSearch() {
        const query = $("#search-Input-recipe").val().toLowerCase();
        const filter = $("#columnSelector").val();

        // Save the current search query and filter to localStorage
        localStorage.setItem('recipeSearchQuery', query);
        localStorage.setItem('recipeSearchFilter', filter);

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
                    text = row.find("td:nth-child(7)").text().toLowerCase(); // Update index for status
                    break;
                case "account_id":
                    text = row.find("td:nth-child(5)").text().toLowerCase(); // Update index for account_id
                    break;
                case "account_username":
                    text = row.find("td:nth-child(6)").text().toLowerCase(); // Update index for account_username
                    break;
                case "image": // Update case for the image column
                    // You might want to modify this depending on how you want to handle image searching
                    text = row.find("td:nth-child(4) img").attr("alt").toLowerCase();
                    break;
                case "recipe_id":
                    text = row.find("td:nth-child(2)").text().toLowerCase(); // Update index for recipe_id
                    break;
                case "name":
                    text = row.find("td:nth-child(3)").text().toLowerCase(); // Update index for name
                    break;
                case "instructions":
                    text = row.find("td:nth-child(4)").text().toLowerCase(); // Update index for instructions
                    break;
                default:
                    const columnIndex = filter === "recipe_id" ? 2 : filter === "name" ? 3 : filter === "instructions" ? 4 : 5;
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