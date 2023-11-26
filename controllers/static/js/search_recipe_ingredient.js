$(document).ready(function () {
    $("#searchInput").on('input', function () {
        const query = $(this).val().toLowerCase();
        const filter = $("#columnSelector").val();

        $(".recipe-ingredient-table tbody tr").each(function () {
            const row = $(this);

            if (filter === "all" || filter === "") {
                if (query === "") {
                    row.show();
                } else {
                    const rowText = row.text().toLowerCase();
                    if (rowText.includes(query)) {
                        row.show();
                    } else {
                        row.hide();
                    }
                }
            } else {
                const text = row.find("td:nth-child(" + (filter === "recipe_id" ? "3" : filter === "recipe_name" ? "1" : filter === "ingredient_id" ? "5" : "4") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});

