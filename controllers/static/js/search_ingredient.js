$(document).ready(function () {
    $("#searchInput-ingredients").on('input', function () {
        const query = $(this).val().toLowerCase();
        const filter = $("#columnSelector").val();

        $(".ingredients-table tbody tr").each(function () {
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
                const text = row.find("td:nth-child(" + (filter === "ingredient_id" ? "1" : filter === "name" ? "2" : filter === "description" ? "3" : "4") + ")").text().toLowerCase();
                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});

