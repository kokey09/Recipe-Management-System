$(document).ready(function () {
    // Retrieve the saved search query and filter from localStorage
    const savedQuery = localStorage.getItem('ingredientsSearchQuery') || '';
    const savedFilter = localStorage.getItem('ingredientsSearchFilter') || 'all';

    // Set the saved query and filter in the corresponding elements
    $("#searchInput-ingredients").val(savedQuery);
    $("#columnSelector").val(savedFilter);

    // Function to handle the search
    function handleSearch() {
        const query = $("#searchInput-ingredients").val().toLowerCase();
        const filter = $("#columnSelector").val();

        // Save the current search query and filter to localStorage
        localStorage.setItem('ingredientsSearchQuery', query);
        localStorage.setItem('ingredientsSearchFilter', filter);

        $(".table-body tbody tr").each(function () {
            const row = $(this);
            let text = "";

            // Update the switch statement in handleSearch function
            switch (filter) {
                case "all":
                case "":
                    text = row.text().toLowerCase();
                    break;
                case "ingredient_id":
                    text = row.find("td:nth-child(2)").text().toLowerCase();
                    break;
                case "name":
                    text = row.find("td:nth-child(3)").text().toLowerCase();
                    break;
                case "description":
                    text = row.find("td:nth-child(4)").text().toLowerCase();
                    break;
                // Add a case for your new column, adjust the index accordingly
                case "your_new_column":
                    text = row.find("td:nth-child(your_column_index)").text().toLowerCase();
                    break;
                default:
                    text = row.find("td:nth-child(2)").text().toLowerCase(); // Default to ingredient_id
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

    // Attach the handleSearch function to the input event of the search input
    $("#searchInput-ingredients").on('input', handleSearch);
});


function refreshSearch() {
    // Reset the select to the default value
    $("#columnSelector").val("all");

    // Clear the search input
    $("#searchInput-ingredients").val("");

    // Trigger the search event to update the table
    $("#searchInput-ingredients").trigger("input");
}

