import { RestAPIUtil } from '../common/restAPIUtil.js';

class DeactivateAccountController {
    constructor() {
        this.deactivateButton = document.getElementById('deactivateButton');

        if (this.deactivateButton) {
            this.deactivateButton.addEventListener('click', this.confirmDeactivation.bind(this));
        }
    }

    confirmDeactivation() {
        if (confirm('Are you sure you want to deactivate your account?')) {
            this.deactivateAccount();
        }
    }

    async deactivateAccount() {
        try {
            const response = await RestAPIUtil.patch('user/deactivate_account');
            alert('Your account has been deactivated. If you want to reactivate it, please contact support.');
            window.location.href = '/';
        } catch (error) {
            console.error('Error deactivating account:', error);
            alert('Failed to deactivate account. Please try again.');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new DeactivateAccountController();
});
