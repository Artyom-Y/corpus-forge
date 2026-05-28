const btnQuiz = document.getElementById('btn-quiz');
const btnFlashcards = document.getElementById('btn-flashcards');
const toolStatus = document.getElementById('tool-status');
const generatedList = document.getElementById('generated-tools-list');
const generatedHeader = document.getElementById('generated-tools-header');
const btnVisualize = document.getElementById('btn-visualize');

function addLinkToList(url, filename) {
    generatedHeader.style.display = 'block';

    const li = document.createElement('li');
    const link = document.createElement('a');
    
    link.href = url;
    link.target = '_blank';
    link.textContent = filename;
    link.classList.add('generated-file-link');

    const deleteBtn = document.createElement('button');
    deleteBtn.innerHTML = 'X';
    deleteBtn.classList.add('delete-tool-btn');
    deleteBtn.title = "Delete " + filename;

    deleteBtn.addEventListener('click', async () => {
        if (!confirm(`Are you sure you want to permanently delete ${filename}?`)) return;

        try {
            const response = await fetch('/delete_tool', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: filename })
            });

            if (response.ok) {
                li.remove(); 
                
                if (generatedList.children.length === 0) {
                    generatedHeader.style.display = 'none';
                }
            } else {
                const data = await response.json();
                alert("Failed to delete: " + data.error);
            }
        } catch (error) {
            console.error("Error deleting tool:", error);
            alert("A network error occurred.");
        }
    });

    li.appendChild(link);
    li.appendChild(deleteBtn);
    generatedList.appendChild(li);
}

async function loadToolsOnStartup() {
    try {
        const response = await fetch('/generated_tools');
        const data = await response.json();

        if (data.files && data.files.length > 0) {
            data.files.forEach(filename => {
                addLinkToList(`storage/output/${filename}`, filename);
            });
        }
    } catch (error) {
        console.error("Error loading past tools:", error);
    }
}

async function generateVisualization() {
    const checkedBoxes = document.querySelectorAll('.file-checkbox:checked');
    const selectedCollections = Array.from(checkedBoxes).map(checkbox => checkbox.value);

    console.log("Files checked:", selectedCollections);

    if (selectedCollections.length === 0) {
        alert("Please select at least one file to visualize.");
        return;
    }

    toolStatus.textContent = "Crafting interactive visualization... Please wait.";
    btnQuiz.disabled = true;
    btnFlashcards.disabled = true;
    btnVisualize.disabled = true;

    try {
        const response = await fetch('/generate_tool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({type: 'visualization', collections_names: selectedCollections})
        });

        const data = await response.json();

        if (response.ok) {
            toolStatus.textContent = "Success! Launching visualizer...";
            window.open(`storage/${data.url}`, '_blank');

            const filename = data.url.split('/').pop();

            addLinkToList(`storage/${data.url}`, filename);
        } else {
            toolStatus.textContent = "Error: " + data.error;
        }
    } catch (error) {
        console.error("Visualization error:", error);
        toolStatus.textContent = "A network error occurred.";
    } finally {
        btnQuiz.disabled = false;
        btnFlashcards.disabled = false;
        btnVisualize.disabled = false;
        setTimeout(() => { toolStatus.textContent = ""; }, 3000); 
    }
}

async function generateTool(type) {
    const checkedBoxes = document.querySelectorAll('.file-checkbox:checked');
    const selectedCollections = Array.from(checkedBoxes).map(checkbox => checkbox.value);

    if (selectedCollections.length === 0) {
        alert('Please select at least one file from the Files sidebar to use as context.');
        return;
    }

    toolStatus.textContent = `Generating ${type}... Please wait.`;
    btnQuiz.disabled = true;
    btnFlashcards.disabled = true;
    btnVisualize.disabled = true;

    try {
        const response = await fetch('/generate_tool', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type: type, collections_names: selectedCollections})
        });

        const data = await response.json();

        if (response.ok) {
            toolStatus.textContent = "Success! Click below to open";

            const filename = data.url.split('/').pop();
            addLinkToList(`storage/${data.url}`, filename);

        } else {
            toolStatus.textContent = `Error: ${data.error}`
        }
    } catch (error) {
        console.error("Tool generation error:", error);
        toolStatus.textContent = "A network error occurred.";
    } finally {
        btnQuiz.disabled = false;
        btnFlashcards.disabled = false;
        btnVisualize.disabled = false;
        
        setTimeout(() => {toolStatus.textContent = "";}, 3000)
    }
}

if (btnQuiz) btnQuiz.addEventListener('click', () => generateTool('quiz'));
if (btnFlashcards) btnFlashcards.addEventListener('click', () => generateTool('flashcards'));
if (btnVisualize) btnVisualize.addEventListener('click', generateVisualization);

window.addEventListener('DOMContentLoaded', loadToolsOnStartup);