$(document).ready(function () {
    $("#searchButton").click(function () {
        var query = $("#searchInput-ingredients").val().toLowerCase();
        var filter = $("#columnSelector").val();

        $(".ingredients-table tbody tr").each(function () {
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
                var text = row.find("td:nth-child(" + (filter === "ingredient_id" ? "1" : filter === "name" ? "2" : filter === "description" ? "3" : "4") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});
