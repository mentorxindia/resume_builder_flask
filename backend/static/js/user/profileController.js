import { RestAPIUtil } from '../common/restAPIUtil.js';

class UserProfileController {
    constructor() {
        this.profileForm = document.getElementById('profileForm');
        this.editButton = document.getElementById('editProfileButton');
        this.saveButton = document.getElementById('saveProfileButton');

        this.profileImageInput = document.getElementById('profileImageInput');
        this.profileImagePreview = document.getElementById('profileImagePreview');
        this.uploadImageButton = document.getElementById('uploadImageButton');

        this.uploadImageButton.addEventListener('click', () => this.profileImageInput.click());
        this.profileImageInput.addEventListener('change', () => this.previewProfileImage());

        if (this.editButton) {
            this.editButton.addEventListener('click', this.enableEdit.bind(this));
        }

        if (this.saveButton) {
            this.saveButton.addEventListener('click', this.saveProfile.bind(this));
        }

        this.getUserProfile();
    }

    async getUserProfile() {
        try {
            const data = await RestAPIUtil.get(`user`);
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

        if (data.profile_image) {
            this.profileImagePreview.src = `/${data.profile_image}`;
        }

        this.toggleEdit(false);
    }

    enableEdit() {
        this.toggleEdit(true);
    }

    convertFileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = (error) => reject(error);
            reader.readAsDataURL(file);
        });
    }

    async previewProfileImageWithBase64() {
        const file = this.profileImageInput.files[0];
        if (file) {
            try {
                const base64Image = await this.convertFileToBase64(file);
                this.profileImagePreview.src = base64Image;
            } catch (error) {
                console.error('Error converting file to Base64:', error);
                alert('Failed to load the image. Please try again.');
            }
        }
    }


    async previewProfileImage() {
        const file = this.profileImageInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                this.profileImagePreview.src = event.target.result;
            };
            reader.onerror = () => {
                alert('Failed to load the image. Please try again.');
            };
            reader.readAsDataURL(file);
        }
    }
    

    async saveProfile(event) {
        event.preventDefault();

        const updatedData = {
            full_name: document.getElementById('userFullName').value,
            email: document.getElementById('userEmail').value,
            phone: document.getElementById('userPhone').value,
            gender: document.getElementById('userGender').value,
            profile_image: null,
        };

        if (this.profileImageInput && this.profileImageInput.files.length > 0) {
            const file = this.profileImageInput.files[0];
            updatedData.profile_image = await this.convertFileToBase64(file);
        }

        try {
            await RestAPIUtil.put(`user`, updatedData);
            alert('Profile updated successfully!');
            this.toggleEdit(false);
        } catch (error) {
            console.error('Error updating profile:', error);
            alert('Failed to update profile. Please try again.');
        }
    }

    toggleEdit(isEditable) {
        const fields = ['userFullName', 'userEmail', 'userPhone', 'userGender', 'uploadImageButton'];
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
    new UserProfileController();
});
