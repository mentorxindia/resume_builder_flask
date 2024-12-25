class ResumeController {
    constructor() {
        this.createResumeBtn = document.getElementById('createResumeBtn');
        if (this.createResumeBtn) {
            this.createResumeBtn.addEventListener('click', this.createResumeHandler.bind(this));
            this.loadResumes();
        }
    }

    async loadResumes() {
        try {
            const resumes = await this.fetchAllResumes();
            const grid = document.getElementById('resumesGrid');
            grid.innerHTML = ''; // Clear existing content

            if (resumes.length === 0) {
                grid.innerHTML = '<p class="text-muted">No resumes found. Create your first resume above!</p>';
                return;
            }

            resumes.forEach((resume) => {
                const card = document.createElement('div');
                card.className = 'col-md-3 mb-3';
                card.innerHTML = `
                  <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${resume.name}</h5>
                            <p class="card-text">Created: ${new Date(resume.created_at).toLocaleDateString()}</p>
                            <div class="d-flex justify-content-end gap-2">
                                <button class="btn btn-sm btn-primary" onclick="editResume(${resume.id})"><i class="fas fa-edit"></i> Edit</button>
                                <button class="btn btn-sm btn-success" onclick="viewResume(${resume.id})"><i class="fas fa-eye"></i> View</button>
                                <button class="btn btn-sm btn-danger" onclick="deleteResume(${resume.id})"><i class="fas fa-trash"></i> Delete</button>
                            </div>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
        } catch (error) {
            console.error('Error loading resumes:', error);
        }
    }

    async createResumeHandler() {
        const resumeName = document.getElementById('newResumeName').value.trim();
        if (!resumeName) {
            alert('Please enter a resume name.');
            return;
        }

        try {
            const newResume = await this.createResume(resumeName);
            if (newResume) {
                alert(`Resume "${resumeName}" created successfully!`);
                this.loadResumes(); // Refresh resumes grid
                document.getElementById('newResumeName').value = ''; // Clear input box
            }
        } catch (error) {
            console.error('Error creating resume:', error);
            alert('Failed to create resume. Please try again.');
        }
    }

    async fetchAllResumes() {
        try {
            const response = await fetch('/api/resume/', {
                method: "GET",
                headers: this._getAuthHeaders(),
            });
            if (!response.ok) throw new Error(`Error fetching resumes: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    async createResume(name) {
        try {
            const response = await fetch('/api/resume', {
                method: "POST",
                headers: {
                    ...this._getAuthHeaders(),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name }),
            });
            if (!response.ok) throw new Error(`Error creating resume: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error(error);
        }
    }

    async deleteResume(id) {
        try {
            const response = await fetch(`/api/resume/${id}`, {
                method: "DELETE",
                headers: this._getAuthHeaders(),
            });
            if (!response.ok) throw new Error(`Error deleting resume: ${response.statusText}`);
            alert('Resume deleted successfully!');
            this.loadResumes(); // Refresh resumes grid
        } catch (error) {
            console.error(error);
            alert('Failed to delete resume. Please try again.');
        }
    }

    // Get authentication headers (JWT token)
    _getAuthHeaders() {
        const token = localStorage.getItem('token');
        return { Authorization: `Bearer ${token}` };
    }
}

// Global action functions for simplicity
function viewResume(id) {
    window.location.href = `/resume/preview/${id}`;
}

function editResume(id) {
    window.location.href = `/resume/${id}`;
    controller.prefillResumeData(id);

}

function deleteResume(id) {
    const confirmed = confirm('Are you sure you want to delete this resume?');
    if (confirmed) {
        const controller = new ResumeController();
        controller.deleteResume(id);
    }
}



// Initialize ResumeController
document.addEventListener('DOMContentLoaded', () => new ResumeController());
