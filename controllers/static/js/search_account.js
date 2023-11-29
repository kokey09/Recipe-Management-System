$(document).ready(function () {
    // Retrieve the saved search query and filter from localStorage
    const savedQuery = localStorage.getItem('accountSearchQuery') || '';
    const savedFilter = localStorage.getItem('accountSearchFilter') || 'all';
    // Set the saved query and filter in the corresponding elements
    $("#searchInput-account").val(savedQuery);
    $("#columnSelector").val(savedFilter);
    // Function to handle the search
    function handleSearch() {
        const query = $("#searchInput-account").val().toLowerCase();
        const filter = $("#columnSelector").val();
        // Save the current search query and filter to localStorage
        localStorage.setItem('accountSearchQuery', query);
        localStorage.setItem('accountSearchFilter', filter);

        $("table tbody tr").each(function () {
            const row = $(this);

            if (filter === "all" || filter === "") {
                if (query === "" || row.text().toLowerCase().includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            } else {
                const columnIndex = filter === "id" ? 1 : filter === "username" ? 2 : filter === "email" ? 4 : filter === "type" ? 5 : filter === "date_created" ? 6 : filter === "is_deleted" ? 7 : 8;
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
    $("#searchInput-account").on('input', handleSearch);
});

