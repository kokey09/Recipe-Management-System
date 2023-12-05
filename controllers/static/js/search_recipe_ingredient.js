$(document).ready(function () {
    // Retrieve the saved search query and filter from localStorage
    const savedQuery = localStorage.getItem('recipeIngredientSearchQuery') || '';
    const savedFilter = localStorage.getItem('recipeIngredientSearchFilter') || 'all';

    // Set the saved query and filter in the corresponding elements
    $("#searchInput").val(savedQuery);
    $("#columnSelector").val(savedFilter);

    // Function to handle the search
    function handleSearch() {
        const query = $("#searchInput").val().toLowerCase();
        const filter = $("#columnSelector").val();

        // Save the current search query and filter to localStorage
        localStorage.setItem('recipeIngredientSearchQuery', query);
        localStorage.setItem('recipeIngredientSearchFilter', filter);

        $(".table tbody tr").each(function () {
            const row = $(this);

            if (filter === "all" || filter === "") {
                if (query === "" || row.text().toLowerCase().includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            } else {
                const columnIndex = filter === "recipe_id" ? 3 : filter === "recipe_name" ? 1 : filter === "ingredient_id" ? 5 : 4;
                const text = row.find("td:nth-child(" + columnIndex + ")").text().toLowerCase();

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

    // Attach the handleSearch function to the input event of the search input
    $("#searchInput").on('input', handleSearch);
});


function refreshSearch() {
    // Reset the select to the default value
    $("#columnSelector").val("all");

    // Clear the search input
    $("#searchInput").val("");

    // Trigger the search event to update the table
    $("#searchInput").trigger("input");
}