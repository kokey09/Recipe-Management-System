$(document).ready(function () {
    const savedQuery = localStorage.getItem('deletedRecipeSearchQuery') || '';
    const savedFilter = localStorage.getItem('deletedRecipeSearchFilter') || 'all';

    $("#search-Input-recipe").val(savedQuery);
    $("#columnSelector").val(savedFilter);

    function handleSearch() {
        const query = $("#search-Input-recipe").val().toLowerCase();
        const filter = $("#columnSelector").val();

        localStorage.setItem('deletedRecipeSearchQuery', query);
        localStorage.setItem('deletedRecipeSearchFilter', filter);

        $(".recipes-table tbody tr").each(function () {
            const row = $(this);
            let text = "";

            switch (filter) {
                case "all":
                case "":
                    text = row.text().toLowerCase(); // All columns
                    break;
                case "status":
                    text = row.find("td:nth-child(8)").text().toLowerCase(); // Status
                    break;
                case "account_id":
                    text = row.find("td:nth-child(4)").text().toLowerCase(); // Account ID
                    break;
                case "account_username":
                    text = row.find("td:nth-child(5)").text().toLowerCase(); // Account Username
                    break;
                case "deleted_at":
                    text = row.find("td:nth-child(7)").text().toLowerCase(); // Deleted At
                    break;
                case "status_changed_at":
                    text = row.find("td:nth-child(9)").text().toLowerCase(); // Status Changed At
                    break;
                case "recipe_id":
                    text = row.find("td:nth-child(2)").text().toLowerCase(); // Recipe ID
                    break;
                case "name":
                    text = row.find("td:nth-child(3) p").text().toLowerCase(); // column: Name
                    break;
                default:
                    const columnIndex = filter === "recipe_id" ? 2 : filter === "name" ? 3 : filter === "status" ? 8 : 4;
                    text = row.find("td:nth-child(" + columnIndex + ")").text().toLowerCase(); // Default columns: Recipe ID, Name, Status, or 4th column
                    break;
            }

            if (text.includes(query)) {
                row.show();
            } else {
                row.hide();
            }
        });
    }

    handleSearch();

    $("#search-Input-recipe, #columnSelector").on('input change', handleSearch);
});

function refreshSearch() {
    $("#columnSelector").val("all");
    $("#search-Input-recipe").val("");
    $("#search-Input-recipe").trigger("input");
}