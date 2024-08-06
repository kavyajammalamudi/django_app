document.addEventListener("DOMContentLoaded", function () {
    // Toggle password visibility
    const togglePassword = document.getElementById("toggle-password");
    const passwordField = document.getElementById("password");

    togglePassword.addEventListener("click", function () {
      const type = passwordField.type === "password" ? "text" : "password";
      passwordField.type = type;
      this.classList.toggle("fa-eye-slash");
    });

    // Toggle confirm password visibility
    const toggleConfirmPassword = document.getElementById(
      "toggle-confirm-password"
    );
    const confirmPasswordField =
      document.getElementById("confirm_password");

    toggleConfirmPassword.addEventListener("click", function () {
      const type =
        confirmPasswordField.type === "password" ? "text" : "password";
      confirmPasswordField.type = type;
      this.classList.toggle("fa-eye-slash");
    });
    
    document.getElementById('registration-form').addEventListener('submit', function(event) {
        var isValid = true;
    
        // Get all input fields
        var firstNameField = document.getElementById('first-name');
        var lastNameField = document.getElementById('last-name');
        var emailField = document.getElementById('email');
        var phoneField = document.getElementById('phone');
        var passwordField = document.getElementById('password');
        var confirmPasswordField = document.getElementById('confirm_password');
    
        // Get all error message elements
        var firstNameError = document.getElementById('first-name-error');
        var lastNameError = document.getElementById('last-name-error');
        var emailError = document.getElementById('email-error');
        var phoneError = document.getElementById('phone-error');
        var passwordError = document.getElementById('password-error');
        var confirmPasswordError = document.getElementById('confirm-password-error');
    
        // Clear previous error messages
        firstNameError.textContent = '';
        lastNameError.textContent = '';
        emailError.textContent = '';
        phoneError.textContent = '';
        passwordError.textContent = '';
        confirmPasswordError.textContent = '';
    
        // Validate fields
        if (!firstNameField.value.trim()) {
            firstNameError.textContent = 'First name is required.';
            isValid = false;
            firstNameField.value = ''; // Clear the field
        } else if (!/^[A-Za-z]+$/.test(firstNameField.value)) {
            firstNameError.textContent = 'First name must contain only alphabets.';
            isValid = false;
            firstNameField.value = ''; // Clear the field
        }
    
        if (!lastNameField.value.trim()) {
            lastNameError.textContent = 'Last name is required.';
            isValid = false;
            lastNameField.value = ''; // Clear the field
        } else if (!/^[A-Za-z]+$/.test(lastNameField.value)) {
            lastNameError.textContent = 'Last name must contain only alphabets.';
            isValid = false;
            lastNameField.value = ''; // Clear the field
        }
    
        if (!emailField.value.trim()) {
            emailError.textContent = 'Email is required.';
            isValid = false;
            emailField.value = ''; // Clear the field
        } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(emailField.value)) {
            emailError.textContent = 'Email must be a valid email address.';
            isValid = false;
            emailField.value = ''; // Clear the field
        }
    
        if (!phoneField.value.trim()) {
            phoneError.textContent = 'Phone number is required.';
            isValid = false;
            phoneField.value = ''; // Clear the field
        } else if (!/^\d{10}$/.test(phoneField.value)) {
            phoneError.textContent = 'Phone number must be 10 digits long and contain no letters.';
            isValid = false;
            phoneField.value = ''; // Clear the field
        }
    
        if (!passwordField.value.trim()) {
            passwordError.textContent = 'Password is required.';
            isValid = false;
            passwordField.value = ''; // Clear the field
            confirmPasswordField.value = ''; // Clear the field
        } else if (passwordField.value.length < 12 || passwordField.value.length > 16) {
            passwordError.textContent = 'Password must be between 12 and 16 characters long.';
            isValid = false;
            passwordField.value = ''; // Clear the field
            confirmPasswordField.value = ''; // Clear the field
        }
    
        if (!confirmPasswordField.value.trim()) {
            confirmPasswordError.textContent = 'Confirm Password is required.';
            isValid = false;
            passwordField.value = ''; // Clear the field
            confirmPasswordField.value = ''; // Clear the field
        } else if (passwordField.value !== confirmPasswordField.value) {
            confirmPasswordError.textContent = 'Passwords do not match.';
            isValid = false;
            passwordField.value = ''; // Clear the field
            confirmPasswordField.value = ''; // Clear the field
        }
    
        if (!isValid) {
            event.preventDefault(); // Prevent form submission
            // Clear password fields
        }
    });
    
  });