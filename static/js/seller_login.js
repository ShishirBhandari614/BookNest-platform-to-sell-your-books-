document.getElementById('sellerLoginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('seller-email').value;
    const password = document.getElementById('seller-password').value;

    try {
        const response = await fetch('/seller-login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            // Redirect to seller dashboard
            window.location.href = '/seller-dashboard/';
        } else {
            showError('sellerLoginForm', data.detail || 'Login failed. Please try again.');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('sellerLoginForm', 'An error occurred. Please try again.');
    }
});

// Toggle password visibility
const togglePassword = document.querySelector('.toggle-password');
togglePassword.addEventListener('click', function() {
    const input = this.previousElementSibling;
    const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
    input.setAttribute('type', type);
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});

// Helper function to show errors
function showError(formId, message) {
    const form = document.getElementById(formId);
    const errorSpan = form.querySelector('.error-message');
    errorSpan.textContent = message;
    errorSpan.style.display = 'block';
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