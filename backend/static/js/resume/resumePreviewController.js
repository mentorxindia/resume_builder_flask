import { RestAPIUtil } from '../common/restAPIUtil.js';
import { downloadPdf, extractIdFromURL } from '../common/util.js';


class ResumePreviewController {
    constructor() {
        this.resumeContent = document.getElementById('resumeContent');
        this.downloadResumeBtn = document.getElementById('downloadResumeBtn');

        if (this.downloadResumeBtn) {
            this.downloadResumeBtn.addEventListener('click', this.downloadResume.bind(this));
        }

        this.getResumePreview();
    }

    async getResumePreview() {
        if (!this.resumeContent) return;
        const resumeId = extractIdFromURL();

        try {
            const data = await RestAPIUtil.get(`resume/preview/${resumeId}`, 'text');
            this.resumeContent.innerHTML = data.resume;
        } catch (error) {
            console.error('Error fetching resume preview:', error);
        }
    }
    
    async downloadResume(event) {
        event.preventDefault();
        const resumeId = extractIdFromURL();
        const resumeContent = document.getElementById('resumeContent');
        downloadPdf(resumeId, resumeContent);
    }
    
}

document.addEventListener('DOMContentLoaded', () => new ResumePreviewController());
