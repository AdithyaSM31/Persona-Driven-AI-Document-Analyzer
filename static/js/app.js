// Persona AI - Enhanced Interactive JavaScript
// Dark Mode, Particle Animation, Modal Window

// DOM Elements
const html = document.documentElement;
const analysisForm = document.getElementById('analysisForm');
const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');
const fileList = document.getElementById('fileList');
const analyzeBtn = document.getElementById('analyzeBtn');

const inputSection = document.getElementById('inputSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

const metadata = document.getElementById('metadata');
const topSections = document.getElementById('topSections');
const detailedAnalysis = document.getElementById('detailedAnalysis');
const errorMessage = document.getElementById('errorMessage');

const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const retryBtn = document.getElementById('retryBtn');
const themeToggle = document.getElementById('themeToggle');

const analysisModal = document.getElementById('analysisModal');
const modalOverlay = document.getElementById('modalOverlay');
const modalClose = document.getElementById('modalClose');
const modalCloseBtn = document.getElementById('modalCloseBtn');
const modalTitle = document.getElementById('modalTitle');
const modalBody = document.getElementById('modalBody');

// State
let selectedFiles = [];
let analysisResults = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initParticles();
    setupEventListeners();
    checkServerHealth();
});

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const current = html.getAttribute('data-theme');
    const newTheme = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Particle Animation
function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const particleCount = 50;

    class Particle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.radius = Math.random() * 2 + 1;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(139, 92, 246, 0.3)';
            ctx.fill();
        }
    }

    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        // Draw connections
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(139, 92, 246, ${0.2 * (1 - distance / 100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    animate();

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// Event Listeners
function setupEventListeners() {
    analysisForm.addEventListener('submit', handleFormSubmit);
    fileInput.addEventListener('change', handleFileSelection);
    
    const fileUploadLabel = document.querySelector('.file-upload-label');
    fileUploadLabel.addEventListener('dragover', handleDragOver);
    fileUploadLabel.addEventListener('dragleave', handleDragLeave);
    fileUploadLabel.addEventListener('drop', handleDrop);
    
    newAnalysisBtn.addEventListener('click', resetForm);
    retryBtn.addEventListener('click', resetForm);
    themeToggle.addEventListener('click', toggleTheme);
    
    // Modal listeners
    modalClose.addEventListener('click', closeModal);
    modalCloseBtn.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);
}

// Server Health Check
async function checkServerHealth() {
    try {
        const response = await fetch('/api/health');
        if (!response.ok) {
            console.error('Health check failed:', response.status);
            return;
        }
        const data = await response.json();
        
        if (!data.model_loaded) {
            console.warn('Model not loaded');
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Form Submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const persona = document.getElementById('persona').value.trim();
    const jobToBeDone = document.getElementById('job_to_be_done').value.trim();
    
    if (!persona || !jobToBeDone) {
        alert('Please fill in all required fields');
        return;
    }
    
    if (selectedFiles.length === 0) {
        alert('Please upload at least one PDF file');
        return;
    }
    
    await analyzeDocuments(persona, jobToBeDone);
}

// File Handling
function handleFileSelection(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.style.borderColor = 'var(--primary)';
}

function handleDragLeave(e) {
    e.currentTarget.style.borderColor = 'var(--border)';
}

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.style.borderColor = 'var(--border)';
    
    const files = Array.from(e.dataTransfer.files).filter(file => 
        file.type === 'application/pdf'
    );
    
    if (files.length > 0) {
        addFiles(files);
    } else {
        alert('Please drop PDF files only');
    }
}

function addFiles(files) {
    files.forEach(file => {
        if (!selectedFiles.find(f => f.name === file.name)) {
            selectedFiles.push(file);
        }
    });
    
    updateFileList();
    updateFileLabel();
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
    updateFileLabel();
}

function updateFileList() {
    if (selectedFiles.length === 0) {
        fileList.innerHTML = '';
        return;
    }
    
    fileList.innerHTML = selectedFiles.map((file, index) => `
        <div class="file-item">
            <div class="file-item-info">
                <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                    <polyline points="13 2 13 9 20 9"/>
                </svg>
                <span class="file-name">${file.name}</span>
            </div>
            <button type="button" class="remove-file" onclick="removeFile(${index})">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        </div>
    `).join('');
}

function updateFileLabel() {
    if (selectedFiles.length === 0) {
        fileLabel.textContent = 'Choose PDF files or drag & drop';
    } else if (selectedFiles.length === 1) {
        fileLabel.textContent = '1 file selected';
    } else {
        fileLabel.textContent = `${selectedFiles.length} files selected`;
    }
}

// Analysis
async function analyzeDocuments(persona, jobToBeDone) {
    inputSection.style.display = 'none';
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    try {
        const formData = new FormData();
        formData.append('persona', persona);
        formData.append('job_to_be_done', jobToBeDone);
        
        selectedFiles.forEach(file => {
            formData.append('files[]', file);
        });
        
        console.log('Analyzing documents...');
        
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }
        
        const results = await response.json();
        analysisResults = results;
        console.log('Analysis complete');
        displayResults(results);
        
    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'Failed to analyze documents');
    }
}

// Display Results
function displayResults(results) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Metadata
    metadata.innerHTML = `
        <div class="metadata-item">
            <span class="metadata-label">Documents</span>
            <span class="metadata-value">${results.metadata.input_documents.length}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Persona</span>
            <span class="metadata-value">${results.metadata.persona}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Processing Time</span>
            <span class="metadata-value">${results.metadata.processing_time}s</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Timestamp</span>
            <span class="metadata-value">${new Date(results.metadata.processing_timestamp).toLocaleString()}</span>
        </div>
    `;
    
    // Top Sections
    topSections.innerHTML = results.extracted_sections.map((section, index) => `
        <div class="section-card" onclick="showDetailedAnalysis(${index})">
            <div class="section-header">
                <div class="section-rank">${section.importance_rank}</div>
                <div class="section-info">
                    <div class="section-title-text">${section.section_title}</div>
                    <div class="section-meta">
                        <span>📄 ${section.document}</span>
                        <span>📖 Page ${section.page_number}</span>
                        ${section.relevance_score ? `
                            <span class="section-badge">${section.relevance_score}% Match</span>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    // Detailed Analysis
    detailedAnalysis.innerHTML = results.sub_section_analysis.map((analysis, index) => `
        <div class="analysis-card" onclick="showDetailedAnalysis(${index})">
            <div class="analysis-header">
                <span class="analysis-title">${analysis.document}</span>
                <span class="analysis-page">Page ${analysis.page_number}</span>
            </div>
            <p class="analysis-text">${analysis.refined_text}</p>
        </div>
    `).join('');
    
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Modal Functions
function showDetailedAnalysis(index) {
    if (!analysisResults) return;
    
    const section = analysisResults.extracted_sections[index];
    const analysis = analysisResults.sub_section_analysis[index];
    
    modalTitle.textContent = section.section_title;
    modalBody.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h3 style="font-size: 1.125rem; font-weight: 700; margin-bottom: 1rem;">Section Information</h3>
            <div style="display: grid; gap: 1rem;">
                <p><strong>Document:</strong> ${section.document}</p>
                <p><strong>Page:</strong> ${section.page_number}</p>
                <p><strong>Rank:</strong> #${section.importance_rank}</p>
                ${section.relevance_score ? `<p><strong>Relevance:</strong> ${section.relevance_score}% Match</p>` : ''}
            </div>
        </div>
        <div>
            <h3 style="font-size: 1.125rem; font-weight: 700; margin-bottom: 1rem;">Full Analysis</h3>
            <p style="line-height: 1.8; color: var(--text); opacity: 0.9;">${analysis.refined_text}</p>
        </div>
    `;
    
    analysisModal.classList.add('active');
}

function closeModal() {
    analysisModal.classList.remove('active');
}

// Error Display
function showError(message) {
    loadingSection.style.display = 'none';
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

// Reset Form
function resetForm() {
    selectedFiles = [];
    analysisForm.reset();
    updateFileList();
    updateFileLabel();
    
    inputSection.style.display = 'block';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    inputSection.scrollIntoView({ behavior: 'smooth' });
}

// Make functions globally available
window.removeFile = removeFile;
window.showDetailedAnalysis = showDetailedAnalysis;
