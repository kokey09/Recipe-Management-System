// Function to handle search
function handleSearch(searchInputId, listClass) {
    const searchInput = document.getElementById(searchInputId);
    const list = document.querySelector(listClass);
    const items = list.querySelectorAll("li");
    const noDataFoundMessage = document.createElement("p");
    noDataFoundMessage.textContent = "Data not found";
    noDataFoundMessage.style.display = "none";
    noDataFoundMessage.style.fontSize = "20px";
    noDataFoundMessage.style.textAlign = "center"; 
    noDataFoundMessage.style.width = "100%"; 

    list.appendChild(noDataFoundMessage);

    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase();
        let dataFound = false;

        for (const item of items) {
            const itemName = item.textContent.toLowerCase();
            if (itemName.includes(searchText)) {
                item.style.display = "block";
                dataFound = true;
            } else {
                item.style.display = "none";
            }
        }

        noDataFoundMessage.style.display = dataFound ? "none" : "block";
    });
}

// user base or page
document.addEventListener("DOMContentLoaded", function() {
    handleSearch("searchInput", ".recipe-list");
});

// ingredient display
document.addEventListener("DOMContentLoaded", function() {
    handleSearch("searchInput", ".ingredients-list");
});

//recipe display
document.addEventListener("DOMContentLoaded", function() {
    handleSearch("searchInput", ".recipe-list");
});