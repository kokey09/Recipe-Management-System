function validateForm() {
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    if (password !== confirm_password) {
        // Display an alert if passwords do not match
        alert("Your password and confirm password do not match.");
        return false; // Prevent form submission
    }
    return true; // Allow form submission if passwords match
}
