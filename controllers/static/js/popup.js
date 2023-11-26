
// recipe instruction
function addReview() {
    const reviewOverlay = document.getElementById('reviewOverlay');
    const reviewPopup = document.getElementById('reviewPopup');

    reviewOverlay.style.display = 'block';
    reviewPopup.style.display = 'block';
}

function closeReview() {
    const reviewOverlay = document.getElementById('reviewOverlay');
    const reviewPopup = document.getElementById('reviewPopup');

    reviewOverlay.style.display = 'none';
    reviewPopup.style.display = 'none';
}

function redirectToLogin() {
    const loginUrl = "/login";

    window.location.href = loginUrl;
}

//ingredient dashboard
function openPopup(){
    const Overlay = document.getElementById('Overlay');
    const Popup = document.getElementById('Popup');

    Overlay.style.display = 'block';
    Popup.style.display = 'block';
}

function closePopup(){
    const Overlay = document.getElementById('Overlay');
    const Popup = document.getElementById('Popup');

    Overlay.style.display = 'none';
    Popup.style.display = 'none';
}


//recipe change status
function openChangeStatusModal(recipeId) {
    // Set the action attribute of the form dynamically
    document.getElementById('changeStatusForm').action = `/change_status/${recipeId}`;
    document.getElementById('recipeIdDisplay').innerText = recipeId;  // Display recipeId for debugging
    document.getElementById('ChangeStatusModal').style.display = 'block';
}

function closeChangeStatusModal() {
   document.getElementById('ChangeStatusModal').style.display = 'none';
}
function changeStatus(status) {
    // Set the selected status to the hidden input field
   document.getElementById('new_status').value = status;
   // Submit the form
   document.getElementById('changeStatusForm').submit();
}



