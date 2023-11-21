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
