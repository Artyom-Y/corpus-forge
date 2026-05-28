const uploadForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');
const overlay = document.getElementById('document-overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayContent = document.getElementById('overlay-content');
const closeBtn = document.getElementById('close-overlay-btn');

closeBtn.addEventListener('click', () => {
    overlay.classList.remove('active');
});

uploadForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) return;

    const submitBtn = uploadForm.querySelector('input[type="submit"]');
    const originalBtnText = submitBtn.value;

    const formData = new FormData();
    formData.append('file', file);

    try {
        submitBtn.disabled = true;
        submitBtn.value = 'Uploading...';

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
    
        const data = await response.json();

        if (response.ok) {
            addFileToList(data.filename);
            uploadForm.reset();
        } else {
            alert("Upload failed: " + data.error);
        }    
    } catch (error) {
        console.error("Error uploading file:", error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.value = originalBtnText;
    }
});

function addFileToList(filename) {
    const li = document.createElement('li');

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = filename.split('.')[0];
    checkbox.classList.add('file-checkbox');
    checkbox.addEventListener('click', (e) => e.stopPropagation());

    const nameSpan = document.createElement('span');
    nameSpan.textContent = filename;
    nameSpan.classList.add('file-name-text');
    nameSpan.addEventListener('click', async (e) => {
        try {
            const response = await fetch(`/files/${filename}/content`);
            const data = await response.json();
            if (response.ok) {
                overlayTitle.textContent = filename;
                overlayContent.textContent = data.content;
                overlay.classList.add('active');
            } else {
                alert("Could not load content");
            }
        } catch (error) {
            console.error("Error fetching content:",error);
        }
    });

    const deleteBtn = document.createElement('button');
    deleteBtn.innerHTML = 'X';
    deleteBtn.classList.add('delete-file-btn');
    deleteBtn.addEventListener('click', async (e) => {
        e.stopPropagation();
        
        if (!confirm(`Are you sure you want to delete ${filename}?`)) return;

        try {
            const response = await fetch('/delete_collection', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({file: filename})
            });

            if (response.ok) {
                li.remove();
            } else {
                alert("Failed to delete file from database");
            }
        } catch (error) {
            console.error("Error deleting file:", error);
        }
    });
    
    li.appendChild(checkbox);
    li.appendChild(nameSpan);
    li.appendChild(deleteBtn);

    fileList.appendChild(li);
}

async function loadFiles() {
    try {
        const response = await fetch('/files');
        const data = await response.json();

        fileList.innerHTML = '';

        data.files.forEach(filename => {
            addFileToList(filename);
        });
    } catch (error) {
        console.error("Error loading files:", error);
    }
}

window.addEventListener('DOMContentLoaded', loadFiles);