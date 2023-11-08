$(document).ready(function () {
    $("#searchButton").click(function () {
        var query = $("#searchInput-account").val().toLowerCase();
        var filter = $("#columnSelector").val();

        $("table tbody tr").each(function () {
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
                var text = row.find("td:nth-child(" + (filter === "id" ? "1" : filter === "username" ? "2" : filter === "email" ? "4" : filter === "type" ? "5" : filter === "date_created" ? "6" : filter === "is_deleted" ? "7" : "8") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});