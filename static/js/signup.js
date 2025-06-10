document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const personalBtn = document.getElementById('personalBtn');
    const corporateBtn = document.getElementById('corporateBtn');
    const personalFields = document.getElementById('personalFields');
    const corporateFields = document.getElementById('corporateFields');
    const inputs = form.querySelectorAll('input, textarea');

    // Toggle account type
    personalBtn.addEventListener('click', function(e) {
        e.preventDefault();
        personalFields.style.display = 'block';
        corporateFields.style.display = 'none';
        personalBtn.classList.add('active');
        corporateBtn.classList.remove('active');
    });
    corporateBtn.addEventListener('click', function(e) {
        e.preventDefault();
        corporateFields.style.display = 'block';
        personalFields.style.display = 'none';
        corporateBtn.classList.add('active');
        personalBtn.classList.remove('active');
    });

    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
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

        // Remove 'required' from all hidden fields (not visible)
        document.querySelectorAll('#signupForm input[required], #signupForm select[required], #signupForm textarea[required]').forEach(function(input) {
            if (!input.offsetParent) { // Not visible
                input.removeAttribute('required');
            }
        });

        // Validate all fields
        let isValid = true;
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        // Collect all error messages
        let allErrors = [];
        const errorMessages = form.querySelectorAll('.error-message');
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
        if (isValid) {
            submitForm();
        }
    });

    function validateField(field) {
        // Find or create error message span
        let errorElement = field.parentElement.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains('error-message')) {
            errorElement = document.createElement('span');
            errorElement.className = 'error-message';
            field.parentElement.parentElement.appendChild(errorElement);
        }
        let isValid = true;
        errorElement.textContent = '';
        // Required field validation
        if (field.required && !field.value.trim()) {
            errorElement.textContent = 'This field is required';
            isValid = false;
        }
        // Email validation
        if ((field.id === 'email_personal' || field.id === 'email_corporate') && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                errorElement.textContent = 'Please enter a valid email address';
                isValid = false;
            } else {
                checkDuplicateEmail(field.value, errorElement);
            }
        }
        // Username validation (only for personal)
        if (field.id === 'username' && field.value) {
            checkDuplicateUsername(field.value, errorElement);
        }
        // Phone number validation
        if ((field.id === 'phone_personal' || field.id === 'phone_corporate') && field.value) {
            const phoneRegex = /^\+?[\d\s-]{10,}$/;
            if (!phoneRegex.test(field.value)) {
                errorElement.textContent = 'Please enter a valid phone number';
                isValid = false;
            } else {
                checkDuplicatePhone(field.value, errorElement);
            }
        }
        // Password validation (only for personal)
        if ((field.id === 'password_personal' || field.id === 'password_corporate' ) && field.value) {
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
        // Password confirmation validation (only for personal)
        if ((field.id === 'confirm_password' || field.id === 'confirm_password_corporate') && field.value) {
            const password = document.getElementById('password_personal');
            const password_corporate = document.getElementById('password_corporate');   
            if (field.id === 'confirm_password' && field.value !== password.value) {
                errorElement.textContent = 'Passwords do not match';
                isValid = false;
            }
            if (field.id === 'confirm_password_corporate' && field.value !== password_corporate.value) {
                errorElement.textContent = 'Passwords do not match';
                isValid = false;
            }
        }
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

    // Function to check duplicate phone number
    function checkDuplicatePhone(phone, errorElement) {
        fetch('/check-phone/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ phone: phone })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                errorElement.textContent = 'This phone number is already registered.';
                errorElement.parentElement.classList.add('error');
            }
        })
        .catch(error => console.error('Error checking phone:', error));
    }

    function submitForm() {
        // Determine account type
        const isPersonal = personalBtn.classList.contains('active');
        let data = {};

        if (isPersonal) {
            data = {
                username: document.getElementById('username').value,
                email: document.getElementById('email_personal').value,
                phone_number: document.getElementById('phone_personal').value,
                full_name: document.getElementById('name').value,
                password: document.getElementById('password_personal').value,
                password2: document.getElementById('confirm_password').value,
                seller_type: 'personal'
            };
        } else {
            data = {
                email: document.getElementById('email_corporate').value,
                username: document.getElementById('store_name').value, // If you want a separate username for corporate, change this accordingly
                phone_number: document.getElementById('phone_corporate').value,
                store_name: document.getElementById('store_name').value,
                address: document.getElementById('address').value,
                password: document.getElementById('password_corporate').value,
                password2: document.getElementById('confirm_password_corporate').value,
                seller_type: 'corporate'
            };
        }

        // Collect all error messages
        let allErrors = [];
        const errorMessages = form.querySelectorAll('.error-message');
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

        // Send the data to your backend (single view, single URL)
        fetch(form.action, {
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
                let allErrors = [];
                if (data.errors) {
                    Object.entries(data.errors).forEach(([field, message]) => {
                        allErrors.push(message);
                    });
                    alert(allErrors.join(', '));
                }
                throw new Error('Please fix the errors above');
            }
            // Success case
            alert('Account created successfully! Redirecting to login page...');
            setTimeout(() => {
                window.location.href = '/seller-login/';
            }, 1500);
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
            const submitBtn = form.querySelector('.submit-btn');
            submitBtn.textContent = 'Sign Up';
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