class UserController {
    constructor() {
        this.profileForm = document.getElementById('profileForm');
        this.editButton = document.getElementById('editProfileButton');
        this.saveButton = document.getElementById('saveProfileButton');
        this.apiUrl = '/api/user';
        this.token = localStorage.getItem('token');

        if (!this.token) {
            alert('Unauthorized access. Please log in.');
            window.location.href = '/';
            return;
        }

        if (this.editButton) {
            this.editButton.addEventListener('click', this.enableEdit.bind(this));
        }

        if (this.saveButton) {
            this.saveButton.addEventListener('click', this.saveProfile.bind(this));
        }

        this.fetchUserProfile();
    }

    async fetchUserProfile() {
        try {
            const response = await fetch(this.apiUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${this.token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch user data: ' + response.statusText);
            }

            const data = await response.json();
            this.populateForm(data);
        } catch (error) {
            console.error('Error fetching user profile:', error);
            alert('Failed to load profile. Please try again later.');
        }
    }

    populateForm(data) {
        document.getElementById('userFullName').value = data.full_name || '';
        document.getElementById('userEmail').value = data.email || '';
        document.getElementById('userPhone').value = data.phone || '';

        const genderSelect = document.getElementById('userGender');
        genderSelect.value = data.gender || 'other';

        this.toggleEdit(false);
    }

    enableEdit() {
        this.toggleEdit(true);
    }

    async saveProfile(event) {
        event.preventDefault();

        const updatedData = {
            full_name: document.getElementById('userFullName').value,
            email: document.getElementById('userEmail').value,
            phone: document.getElementById('userPhone').value,
            gender: document.getElementById('userGender').value,
        };

        try {
            const response = await fetch(this.apiUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${this.token}`,
                },
                body: JSON.stringify(updatedData),
            });

            if (!response.ok) {
                throw new Error('Failed to update profile: ' + response.statusText);
            }

            alert('Profile updated successfully!');
            this.toggleEdit(false);
        } catch (error) {
            console.error('Error updating profile:', error);
            alert('Failed to update profile. Please try again.');
        }
    }

    toggleEdit(isEditable) {
        const fields = ['userFullName', 'userEmail', 'userPhone', 'userGender'];
        fields.forEach((fieldId) => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.disabled = !isEditable;
            }
        });

        this.editButton.style.display = isEditable ? 'none' : 'inline-block';
        this.saveButton.style.display = isEditable ? 'inline-block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UserController();
});
