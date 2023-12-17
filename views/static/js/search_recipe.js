$(document).ready(function () {
    const savedQuery = localStorage.getItem('recipeSearchQuery') || '';
    const savedFilter = localStorage.getItem('recipeSearchFilter') || 'all';

    $("#search-Input-recipe").val(savedQuery);
    $("#columnSelector").val(savedFilter);

    function handleSearch() {
        const query = $("#search-Input-recipe").val().toLowerCase();
        const filter = $("#columnSelector").val();

        localStorage.setItem('recipeSearchQuery', query);
        localStorage.setItem('recipeSearchFilter', filter);

        $(".recipes-table tbody tr").each(function () {
            const row = $(this);
            let text = "";

            switch (filter) {
                case "recipe_id":
                    text = row.find("td:nth-child(2)").text().toLowerCase(); //for recipe_id
                    break;
                case "name":
                    text = row.find("td:nth-child(3)").text().toLowerCase(); //for name
                    break;
                case "account_id":
                    text = row.find("td:nth-child(4) p:first-child").text().toLowerCase(); //for account_id
                    break;
                case "account_username":
                    text = row.find("td:nth-child(4) p:last-child").text().toLowerCase(); //for account_username
                    break;
                case "created_at":
                    text = row.find("td:nth-child(5)").text().toLowerCase(); //for created_at
                    break;
                case "recovered_by":
                     text = row.find("td:nth-child(6)").text().toLowerCase(); //for recovered_at
                    break;
                case "recovered_by_username":
                    text = row.find("td:nth-child(6)").text().toLowerCase(); //for recovered_at
                    break;
                case "recovered_at":
                    text = row.find("td:nth-child(7)").text().toLowerCase(); //for recovered_at
                    break;
                case "status":
                    text = row.find("td:nth-child(8)").text().toLowerCase(); //for status
                    break;
                case "status_changed_by_id":
                    text = row.find("td:nth-child(9) p:first-child").text().toLowerCase(); //for status_changed_by_id
                    break;
                case "status_changed_by_username":
                    text = row.find("td:nth-child(9) p:last-child").text().toLowerCase(); //for status_changed_by_username
                    break;
                case "status_changed_at":
                    text = row.find("td:nth-child(10)").text().toLowerCase(); //for status_changed_at
                    break;
                case "all":
                case "":
                    text = row.text().toLowerCase();
                    break;
                default:
                    const columnIndex = filter === "recipe_id" ? 2 : filter === "name" ? 3 : 4;
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

    handleSearch();

    $("#search-Input-recipe, #columnSelector").on('input change', handleSearch);
});

function refreshSearch() {
    $("#columnSelector").val("all");
    $("#search-Input-recipe").val("");
    $("#search-Input-recipe").trigger("input");
}