// Function to handle search
function handleSearch(searchInputId, cardClass) {
    const searchInput = document.getElementById(searchInputId);
    const cards = document.querySelectorAll(cardClass);
    const noDataFoundMessage = document.createElement("p");
    noDataFoundMessage.textContent = "Data not found";
    noDataFoundMessage.style.display = "none";
    noDataFoundMessage.style.fontSize = "20px"; // Set the font size to 20px
    document.body.appendChild(noDataFoundMessage);

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();
        let dataFound = false;

        for (const card of cards) {
            const cardName = card.querySelector('.contentbx h3').textContent.toLowerCase();
            if (cardName.includes(searchText)) {
                card.style.display = "block";
                dataFound = true;
            } else {
                card.style.display = "none";
            }
        }

        noDataFoundMessage.style.display = dataFound ? "none" : "block";
    });
}

// Use the function on DOMContentLoaded
document.addEventListener("DOMContentLoaded", function() {
    handleSearch("searchInput", ".card");
});