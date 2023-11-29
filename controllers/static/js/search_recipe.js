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

            if (filter === "all" || filter === "") {
                if (query === "" || row.text().toLowerCase().includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            } else {
                let text;

                if (filter === "status") {
                    text = row.find("td:nth-child(8)").text().toLowerCase();
                } else if (filter === "account_id") {
                    text = row.find("td:nth-child(5)").text().toLowerCase();
                } else if (filter === "account_username") {
                    text = row.find("td:nth-child(6)").text().toLowerCase();
                } else {
                    const columnIndex = filter === "recipe_id" ? 1 : filter === "name" ? 2 : filter === "instructions" ? 3 : 4;
                    text = row.find("td:nth-child(" + columnIndex + ")").text().toLowerCase();
                }

                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    }

    // Initial search
    handleSearch();

    // Attach the handleSearch function to the input and select change events
    $("#search-Input-recipe, #columnSelector").on('input change', handleSearch);
});

