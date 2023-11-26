//recipe
$(document).ready(function () {
    $("#search-Input-recipe").on('input', function () {
        const query = $(this).val().toLowerCase();
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
                let text;

                if (filter === "status") {
                    text = row.find("td:nth-child(8)").text().toLowerCase(); // Assuming status is in the 8th column
                } else if (filter === "account_id") {
                    text = row.find("td:nth-child(5)").text().toLowerCase(); // Assuming account_id is in the 5th column
                } else if (filter === "account_username") {
                    text = row.find("td:nth-child(6)").text().toLowerCase(); // Assuming account_username is in the 6th column
                } else {
                    text = row.find("td:nth-child(" + (filter === "recipe_id" ? "1" : filter === "name" ? "2" : filter === "instructions" ? "3" : "4") + ")").text().toLowerCase();
                }

                if (text.includes(query)) {
                    row.show();
                } else {
                    row.hide();
                }
            }
        });
    });
});
