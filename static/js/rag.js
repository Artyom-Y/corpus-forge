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

    const formData = new FormData();
    formData.append('file', file);

    try {
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
    }
});

function addFileToList(filename) {
    const li = document.createElement('li');
    li.textContent = filename;

    li.style.cursor = 'pointer';
    li.style.color = '#007BFF';
    li.style.textDecoration = 'underline';
    li.style.marginBottom = '10px';

    li.addEventListener('click', async () => {
        try {
            const response = await fetch(`/files/${filename}/content`);
            const data = await response.json();

            if (response.ok) {
                overlayTitle.textContent = filename;
                overlayContent.textContent = data.content;
                overlay.classList.add('active');
            } else {
                alert("Could not load content.");
            }
        } catch (error) {
            console.error("Error loading file content:", error);
        }
    });

    fileList.appendChild(li);
    document.createElement('br');
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