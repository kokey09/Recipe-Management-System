//recipe
$(document).ready(function () {
    $("#searchButton").click(function () {
        const query = $("#search-Input-recipe").val().toLowerCase();
        const filter = $("#columnSelector").val();

        $(".recipes-table tbody tr").each(function () {
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
                const text = row.find("td:nth-child(" + (filter === "recipe_id" ? "1" : filter === "name" ? "2" : filter === "instructions" ? "3" : "4") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});