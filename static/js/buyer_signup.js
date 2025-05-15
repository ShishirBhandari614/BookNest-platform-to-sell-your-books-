document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('buyerSignupForm');
    const inputs = form.querySelectorAll('input');

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
        // Find the error message element that's a sibling of the input
        const errorElement = field.parentElement.querySelector('.error-message');
        let isValid = true;

        // Clear previous error
        errorElement.textContent = '';
        field.style.backgroundColor = '';

        // Required field validation
        if (field.required && !field.value.trim()) {
            errorElement.textContent = 'This field is required';
            errorElement.style.color = '#ff3333';
            field.style.backgroundColor = '#f8f9fe';
            isValid = false;
        }

        // Email validation
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                errorElement.textContent = 'Please enter a valid email address';
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
                isValid = false;
            } else {
                // Check for duplicate email
                checkDuplicateEmail(field.value, errorElement, field);
            }
        }

        // Username validation
        if (field.id === 'username' && field.value) {
            checkDuplicateUsername(field.value, errorElement, field);
        }

        // Phone number validation
        if (field.id === 'phone_number' && field.value) {
            const phoneRegex = /^\+?[\d\s-]{10,}$/;
            if (!phoneRegex.test(field.value)) {
                errorElement.textContent = 'Please enter a valid phone number';
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
                isValid = false;
            }
        }

        // Password validation
        if (field.id === 'password' && field.value) {
            if (field.value.length < 8) {
                errorElement.textContent = 'Password must be at least 8 characters long';
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
                isValid = false;
            }
            if (!/[A-Z]/.test(field.value)) {
                errorElement.textContent = 'Password must contain at least one uppercase letter';
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
                isValid = false;
            }
            if (!/[a-z]/.test(field.value)) {
                errorElement.textContent = 'Password must contain at least one lowercase letter';
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
                isValid = false;
            }
            if (!/[0-9]/.test(field.value)) {
                errorElement.textContent = 'Password must contain at least one number';
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
                isValid = false;
            }
        }

        // Password confirmation validation
        if (field.id === 'password2' && field.value) {
            const password = document.getElementById('password');
            if (field.value !== password.value) {
                errorElement.textContent = 'Passwords do not match';
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
                isValid = false;
            }
        }

        return isValid;
    }

    // Function to check duplicate email
    function checkDuplicateEmail(email, errorElement, field) {
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
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
            } else {
                errorElement.textContent = '';
                field.style.backgroundColor = '';
            }
        })
        .catch(error => {
            console.error('Error checking email:', error);
            errorElement.textContent = 'Error checking email availability. Please try again.';
            errorElement.style.color = '#ff3333';
        });
    }

    // Function to check duplicate username
    function checkDuplicateUsername(username, errorElement, field) {
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
                errorElement.style.color = '#ff3333';
                field.style.backgroundColor = '#f8f9fe';
            } else {
                errorElement.textContent = '';
                field.style.backgroundColor = '';
            }
        })
        .catch(error => {
            console.error('Error checking username:', error);
            errorElement.textContent = 'Error checking username availability. Please try again.';
            errorElement.style.color = '#ff3333';
        });
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
        fetch('/buyer-signup/', {
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
                            const errorElement = input.nextElementSibling;
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
                window.location.href = '/buyer-login/';
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
