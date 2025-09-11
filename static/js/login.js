// Modern Login Script
document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const passwordToggle = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('input[name="password"]');
    
    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function() {
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    }
    
    // Form submission handling
    const loginForm = document.querySelector('.modern-form');
    const submitBtn = document.querySelector('.submit-btn');
    
    if (loginForm && submitBtn) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.querySelector('input[name="username"]').value.trim();
            const password = document.querySelector('input[name="password"]').value;
            
            // Client-side validation
            if (!username) {
                e.preventDefault();
                showAlert('Please enter your username', 'error');
                document.querySelector('input[name="username"]').focus();
                return;
            }
            
            if (username.length < 3) {
                e.preventDefault();
                showAlert('Username must be at least 3 characters long', 'error');
                document.querySelector('input[name="username"]').focus();
                return;
            }
            
            if (!password) {
                e.preventDefault();
                showAlert('Please enter your password', 'error');
                document.querySelector('input[name="password"]').focus();
                return;
            }
            
            if (password.length < 6) {
                e.preventDefault();
                showAlert('Password must be at least 6 characters long', 'error');
                document.querySelector('input[name="password"]').focus();
                return;
            }
            
            // Add loading state
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.modern-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            fadeOutAndRemove(alert);
        }, 5000);
    });
    
    // Forgot password link
    const forgotLink = document.querySelector('.forgot-link');
    if (forgotLink) {
        forgotLink.addEventListener('click', function(e) {
            e.preventDefault();
            showAlert('Please contact support for password reset assistance', 'info');
        });
    }
    
    // Input field animations
    const inputs = document.querySelectorAll('.modern-input');
    inputs.forEach(input => {
        // Check if input has value on load
        if (input.value) {
            input.classList.add('has-value');
        }
        
        // Add/remove class based on input value
        input.addEventListener('input', function() {
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
        
        // Focus animations
        input.addEventListener('focus', function() {
            this.closest('.form-field').classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.closest('.form-field').classList.remove('focused');
        });
    });
    
    // Remember me functionality
    const rememberCheckbox = document.getElementById('rememberMe');
    const usernameInput = document.querySelector('input[name="username"]');
    
    // Load saved username if remember me was checked
    if (localStorage.getItem('rememberMe') === 'true' && usernameInput) {
        const savedUsername = localStorage.getItem('savedUsername');
        if (savedUsername) {
            usernameInput.value = savedUsername;
            usernameInput.classList.add('has-value');
            if (rememberCheckbox) {
                rememberCheckbox.checked = true;
            }
        }
    }
    
    // Save/remove username based on remember me
    if (loginForm && rememberCheckbox) {
        loginForm.addEventListener('submit', function() {
            if (rememberCheckbox.checked) {
                localStorage.setItem('rememberMe', 'true');
                localStorage.setItem('savedUsername', usernameInput.value);
            } else {
                localStorage.removeItem('rememberMe');
                localStorage.removeItem('savedUsername');
            }
        });
    }
    
    // Add parallax effect to background elements
    document.addEventListener('mousemove', function(e) {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        // Move circles
        const circles = document.querySelectorAll('.circle');
        circles.forEach((circle, index) => {
            const speed = (index + 1) * 0.5;
            const x = (mouseX - 0.5) * speed * 20;
            const y = (mouseY - 0.5) * speed * 20;
            circle.style.transform = `translate(${x}px, ${y}px)`;
        });
        
        // Move shapes
        const shapes = document.querySelectorAll('.shape');
        shapes.forEach((shape, index) => {
            const speed = (index + 1) * 0.3;
            const x = (mouseX - 0.5) * speed * 30;
            const y = (mouseY - 0.5) * speed * 30;
            shape.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
    
    // Feature cards hover effect
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Helper function to show alerts
function showAlert(message, type = 'info') {
    // Remove any existing alerts
    const existingAlerts = document.querySelectorAll('.modern-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `modern-alert alert-${type}`;
    alertDiv.innerHTML = `
        <div class="alert-icon">
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        </div>
        <div class="alert-message">${message}</div>
        <button type="button" class="alert-dismiss" onclick="this.closest('.modern-alert').remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    const formHeader = document.querySelector('.form-header');
    if (formHeader) {
        formHeader.insertAdjacentElement('afterend', alertDiv);
        
        // Animate in
        setTimeout(() => {
            alertDiv.style.opacity = '1';
            alertDiv.style.transform = 'translateY(0)';
        }, 10);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            fadeOutAndRemove(alertDiv);
        }, 5000);
    }
}

// Helper function to fade out and remove element
function fadeOutAndRemove(element) {
    if (element && element.parentNode) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            if (element.parentNode) {
                element.remove();
            }
        }, 300);
    }
}

// Prevent form resubmission on page refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

// Add ripple effect to buttons
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn')) {
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        ripple.style.left = e.offsetX + 'px';
        ripple.style.top = e.offsetY + 'px';
        e.target.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }
}); 