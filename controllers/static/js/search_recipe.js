//recipe
$(document).ready(function () {
    $("#searchButton").click(function () {
        var query = $("#search-Input-recipe").val().toLowerCase();
        var filter = $("#columnSelector").val();

        $(".recipes-table tbody tr").each(function () {
            var row = $(this);

            if (filter === "all" || filter === "") {
                if (query === "") {
                    row.show();
                } else {
                    var rowText = row.text().toLowerCase();
                    if (rowText.includes(query)) {
                        row.show();
                    } else {
                        row.hide();
                    }
                }
            } else {
                var text = row.find("td:nth-child(" + (filter === "recipe_id" ? "1" : filter === "name" ? "2" : filter === "instructions" ? "3" : "4") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});