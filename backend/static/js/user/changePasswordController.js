import { RestAPIUtil } from '../common/restAPIUtil.js';


class UserChangePasswordController {
    constructor() {
        this.changePasswordForm = document.getElementById('changePasswordForm');

        if (this.changePasswordForm) {
            this.changePasswordForm.addEventListener('submit', this.changePassword.bind(this));
        }
    }

    async changePassword(event) {
        event.preventDefault();

        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const errorMessage = document.getElementById('errorMessage');

        if (newPassword !== confirmPassword) {
            errorMessage.textContent = 'New and Confirm password do not match.';
            errorMessage.style.display = 'block';
            return;
        }

        try {
            await RestAPIUtil.post(
                `user/change_password`,
                {
                    current_password: currentPassword,
                    new_password: newPassword,
                }
            );

            alert('Password changed successfully!');
            this.changePasswordForm.reset();
            errorMessage.style.display = 'none';
        } catch (error) {
            console.error('Error changing password:', error);
            errorMessage.textContent = error.message || 'Failed to change password. Please try again.';
            errorMessage.style.display = 'block';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UserChangePasswordController();
});
