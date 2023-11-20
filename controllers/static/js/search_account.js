$(document).ready(function () {
    $("#searchButton").click(function () {
        const query = $("#searchInput-account").val().toLowerCase();
        const filter = $("#columnSelector").val();

        $("table tbody tr").each(function () {
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
                const text = row.find("td:nth-child(" + (filter === "id" ? "1" : filter === "username" ? "2" : filter === "email" ? "4" : filter === "type" ? "5" : filter === "date_created" ? "6" : filter === "is_deleted" ? "7" : "8") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});