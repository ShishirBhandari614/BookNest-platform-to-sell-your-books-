document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    const inputs = form.querySelectorAll('input, textarea');

    // Toggle password visibility
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    });

    // Real-time validation
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
        });

        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all fields
        let isValid = true;
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            submitForm();
        }
    });

    function validateField(field) {
        const errorElement = field.parentElement.nextElementSibling;
        let isValid = true;

        // Clear previous error
        errorElement.textContent = '';

        // Required field validation
        if (field.required && !field.value.trim()) {
            errorElement.textContent = 'This field is required';
            isValid = false;
        }

        // Email validation
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                errorElement.textContent = 'Please enter a valid email address';
                isValid = false;
            } else {
                // Check for duplicate email
                checkDuplicateEmail(field.value, errorElement);
            }
        }

        // Username validation
        if (field.id === 'username' && field.value) {
            checkDuplicateUsername(field.value, errorElement);
        }

        // Phone number validation
        if (field.id === 'phone_number' && field.value) {
            const phoneRegex = /^\+?[\d\s-]{10,}$/;
            if (!phoneRegex.test(field.value)) {
                errorElement.textContent = 'Please enter a valid phone number';
                isValid = false;
            }
        }

        // Password validation
        if (field.id === 'password' && field.value) {
            if (field.value.length < 8) {
                errorElement.textContent = 'Password must be at least 8 characters long';
                isValid = false;
            }
            if (!/[A-Z]/.test(field.value)) {
                errorElement.textContent = 'Password must contain at least one uppercase letter';
                isValid = false;
            }
            if (!/[a-z]/.test(field.value)) {
                errorElement.textContent = 'Password must contain at least one lowercase letter';
                isValid = false;
            }
            if (!/[0-9]/.test(field.value)) {
                errorElement.textContent = 'Password must contain at least one number';
                isValid = false;
            }
        }

        // Password confirmation validation
        if (field.id === 'password2' && field.value) {
            const password = document.getElementById('password');
            if (field.value !== password.value) {
                errorElement.textContent = 'Passwords do not match';
                isValid = false;
            }
        }

        // Visual feedback
        field.parentElement.classList.toggle('error', !isValid);
        return isValid;
    }

    // Function to check duplicate email
    function checkDuplicateEmail(email, errorElement) {
        fetch('/check-email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                errorElement.textContent = 'This email is already registered. Please use another email or login.';
                errorElement.parentElement.classList.add('error');
            }
        })
        .catch(error => console.error('Error checking email:', error));
    }

    // Function to check duplicate username
    function checkDuplicateUsername(username, errorElement) {
        fetch('/check-username/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ username: username })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                errorElement.textContent = 'This username is already taken. Please choose another one.';
                errorElement.parentElement.classList.add('error');
            }
        })
        .catch(error => console.error('Error checking username:', error));
    }

    function submitForm() {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Collect all error messages
        let allErrors = [];
        
        // Check for any error messages in the form
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(el => {
            if (el.textContent.trim()) {
                allErrors.push(el.textContent.trim());
            }
        });

        // If there are any errors, show them in a single alert
        if (allErrors.length > 0) {
            alert(allErrors.join(', '));
            return;
        }

        // Show loading state
        const submitBtn = form.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Creating Account...';
        submitBtn.disabled = true;

        // Send the data to your backend
        fetch('/seller-signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => Promise.reject(err));
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'error') {
                // Handle field-specific errors
                if (data.errors) {
                    Object.entries(data.errors).forEach(([field, message]) => {
                        const input = document.getElementById(field);
                        if (input) {
                            const inputGroup = input.closest('.input-group');
                            inputGroup.classList.add('error');
                            const errorElement = inputGroup.nextElementSibling;
                            errorElement.textContent = message;
                            allErrors.push(message);
                        }
                    });
                    // Show all errors in a single alert
                    alert(allErrors.join(', '));
                }
                throw new Error('Please fix the errors above');
            }
            // Success case
            alert('Account created successfully! Redirecting to login page...');
            setTimeout(() => {
                window.location.href = '/seller-login/';
            }, 1500); // Wait 1.5 seconds before redirecting
        })
        .catch(error => {
            let errorMessage = 'An error occurred during signup';
            if (error.errors) {
                errorMessage = Object.values(error.errors).join(', ');
            } else if (error.detail) {
                errorMessage = error.detail;
            } else if (error.message) {
                errorMessage = error.message;
            }
            alert(errorMessage);
        })
        .finally(() => {
            // Reset button state
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}); 