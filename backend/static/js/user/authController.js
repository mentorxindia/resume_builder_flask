import { RestAPIUtil, NonAuthenticatedRestAPIUtil } from '../common/restAPIUtil.js';

class AuthController {
    constructor() {
        this.loginForm = document.getElementById('loginForm');
        this.registerForm = document.getElementById('registerForm');
        
        if (this.loginForm) {
            this.loginForm.addEventListener('submit', this.handleLogin.bind(this));
        }

        if (this.registerForm) {
            this.registerForm.addEventListener('submit', this.handleRegister.bind(this));
        }

        this.logoutButton = document.getElementById('logoutButton');
        if (this.logoutButton) {
            this.logoutButton.addEventListener('click', this.handleLogout.bind(this));
        }

        const registerLink = document.getElementById('registerFormLink');
        if (registerLink) {
            registerLink.addEventListener('click', this.showRegisterForm.bind(this));
        }

        const loginLink = document.getElementById('loginFormLink');
        if (loginLink) {
            loginLink.addEventListener('click', this.showLoginForm.bind(this));
        }
    }

    async handleRegister(event) {
        event.preventDefault();
    
        const fullName = document.getElementById('registerName').value;
        const email = document.getElementById('registerEmail').value;
        const phone = document.getElementById('registerPhone').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('registerConfirmPassword').value;
        const gender = document.getElementById('registerGender').value;
        const terms = document.getElementById('registerTerms').checked;
    
        const registerError = document.getElementById('registerError');
    
        // Validate password match
        if (password !== confirmPassword) {
            registerError.textContent = 'Passwords do not match.';
            registerError.style.display = 'block';
            return;
        }
    
        if (!terms) {
            registerError.textContent = 'You must agree to the terms and conditions.';
            registerError.style.display = 'block';
            return;
        }
    
        try {
            const data = await NonAuthenticatedRestAPIUtil.post('user/register', {
                fullName,
                email,
                phone,
                password,
                gender
            });
    
            if (data) {
                alert('Registration successful! You can now log in.');
                window.location.href = '/';
            } else {
                registerError.textContent = `Registration failed.`;
                registerError.style.display = 'block';
            }
        } catch (error) {
            registerError.textContent = error.message;
            registerError.style.display = 'block';
        }
    }
    
    async handleLogin(event) {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const data = await NonAuthenticatedRestAPIUtil.post('user/login', { email, password });
            if (data) {
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user_full_name', data.user.full_name);
                switch (data.user.role) {
                    case "admin":
                        window.location.href = "/dashboard_admin";
                        break;
                    case "support":
                        window.location.href = "/dashboard_support";
                        break;
                    case "user":
                    default:
                        window.location.href = "/dashboard";
                }
            } else {
                document.getElementById('loginError').textContent = `Login failed with status: ${response.status}`;
                document.getElementById('loginError').style.display = 'block';
            }
        } catch (error) {
            document.getElementById('loginError').textContent = error.message;
            document.getElementById('loginError').style.display = 'block';
        }
    }

    async handleLogout() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                alert('No token found, you are not logged in.');
                return;
            }

            const data = await RestAPIUtil.post('user/logout', {}, true);

            if (data) {
                localStorage.removeItem('token');
                window.location.href = '/';
            } else {
                alert(`Error logging out`);
                console.error('Logout failed');
                window.location.href = '/';
            }
        } catch (error) {
            alert('Error logging out');
            console.error('Logout error:', error);
            window.location.href = '/';
        }
    }

    showRegisterForm(event) {
        event.preventDefault();
        if (this.registerForm && this.loginForm) {
            this.registerForm.style.display = 'block';
            this.loginForm.style.display = 'none';
        }
    }

    showLoginForm(event) {
        event.preventDefault();
        if (this.loginForm && this.registerForm) {
            this.loginForm.style.display = 'block';
            this.registerForm.style.display = 'none';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AuthController();
});
