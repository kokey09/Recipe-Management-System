$(document).ready(function () {
    $("#searchInput-reviews").on('input', function () {
        const query = $(this).val().toLowerCase();
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
                const text = row.find("td:nth-child(" + (filter === "review_id" ? "1" : filter === "recipe_id" ? "2" : filter === "recipe_name" ? "3" : filter === "account_id" ? "4" : filter === "account_username" ? "5" : filter === "review_text" ? "6" : filter === "rating" ? "7" : filter === "date_created" ? "8" : "9") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});

