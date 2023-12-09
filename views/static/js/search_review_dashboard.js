
//review_dashboard

$(document).ready(function () {
    $("#searchButton").click(function () {
        const query = $("#searchInput-reviews").val().toLowerCase();
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
                const text = row.find("td:nth-child(" + (filter === "review_id" ? "1" : filter === "recipe_id" ? "2" : filter === "account_id" ? "3" : filter === "review_text" ? "4" : filter === "rating" ? "5" : filter === "timestamp" ? "6" : "7") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});