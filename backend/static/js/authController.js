class AuthController {
    constructor() {
        this.loginForm = document.getElementById('loginForm');
        this.registerForm = document.getElementById('registerForm');
        
        // Bind event listeners for login and register forms
        if (this.loginForm) {
            this.loginForm.addEventListener('submit', this.handleLogin.bind(this));
        }

        if (this.registerForm) {
            this.registerForm.addEventListener('submit', this.handleRegister.bind(this));
        }

        // Bind the logout button
        this.logoutButton = document.getElementById('logoutButton');
        if (this.logoutButton) {
            this.logoutButton.addEventListener('click', this.handleLogout.bind(this));
        }

        // Bind the show/hide form functions
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

        // Validate terms and conditions
        if (!terms) {
            registerError.textContent = 'You must agree to the terms and conditions.';
            registerError.style.display = 'block';
            return;
        }

        try {
            // Send the registration data to the server
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    fullName,
                    email,
                    phone,
                    password,
                    gender
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert('Registration successful! You can now log in.');
                window.location.href = '/';  // Redirect to login page
            } else {
                // Display registration error message
                registerError.textContent = data.message;
                registerError.style.display = 'block';
            }
        } catch (error) {
            console.error('Registration error:', error);
            registerError.textContent = 'An error occurred. Please try again later.';
            registerError.style.display = 'block';
        }
    }

    async handleLogin(event) {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();

            if (response.ok) {
                // Store the JWT token in localStorage
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user_full_name', data.user.full_name);

                window.location.href = '/resume';  // Redirect to the dashboard page
            } else {
                // Display login error message
                document.getElementById('loginError').textContent = data.message;
                document.getElementById('loginError').style.display = 'block';
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    }

    async handleLogout() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                alert('No token found, you are not logged in.');
                return;
            }

            const response = await fetch('/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,  // Send the JWT token as a Bearer token in the Authorization header
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                localStorage.removeItem('token');  // Remove the token from localStorage
                window.location.href = '/';  // Redirect to login page
            } else {
                alert('Error logging out');
                window.location.href = '/'; 
            }
        } catch (error) {
            console.error('Logout error:', error);
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

new AuthController();
