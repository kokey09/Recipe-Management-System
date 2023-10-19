// account_delete.js
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-button");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const accountId = button.getAttribute("data-account-id");

            // Ask for confirmation before deleting
            const confirmed = window.confirm("Are you sure you want to delete this account?");

            if (confirmed) {
                // Send a request to the server to delete the account
                fetch(`/delete_account/${accountId}`, {
                    method: 'POST',
                })
                .then(response => {
                    if (response.ok) {
                        // Reload the page or remove the deleted account row from the table
                        window.location.reload(); // Reload the page for simplicity
                    } else {
                        // Handle the error if account deletion is unsuccessful
                        console.error('Error deleting account:', response.statusText);
                    }
                })
                .catch(error => {
                    // Handle other errors if needed
                    console.error('Error:', error);
                });
            }
        });
    });
});





















