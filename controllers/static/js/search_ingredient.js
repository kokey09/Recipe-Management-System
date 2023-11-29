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

        $(".ingredients-table tbody tr").each(function () {
            const row = $(this);

            if (filter === "all" || filter === "") {
                if (query === "" || row.text().toLowerCase().includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            } else {
                const columnIndex = filter === "ingredient_id" ? 1 : filter === "name" ? 2 : filter === "description" ? 3 : 4;
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
    $("#searchInput-ingredients").on('input', handleSearch);
});


