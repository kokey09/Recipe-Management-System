 function myFunction() {
            const passwordInput = document.getElementById("password");
            const confirmPasswordInput = document.getElementById("confirm_password");

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                confirmPasswordInput.type = "text";
            } else {
                passwordInput.type = "password";
                confirmPasswordInput.type = "password";
            }
        }