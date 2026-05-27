const btnQuiz = document.getElementById('btn-quiz');
const btnFlashcards = document.getElementById('btn-flashcards');
const toolStatus = document.getElementById('tool-status');
const generatedList = document.getElementById('generated-tools-list');
const generatedHeader = document.getElementById('generated-tools-header');

function addLinkToList(url, filename) {
    generatedHeader.style.display = 'block';

    const li = document.createElement('li');
    const link = document.createElement('a');
    
    link.href = url;
    link.target = '_blank';
    link.textContent = filename;
    link.classList.add('generated-file-link');

    li.appendChild(link);
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
        
        setTimeout(() => {toolStatus.textContent = "";}, 3000)
    }
}

if (btnQuiz) btnQuiz.addEventListener('click', () => generateTool('quiz'));
if (btnFlashcards) btnFlashcards.addEventListener('click', () => generateTool('flashcards'));

window.addEventListener('DOMContentLoaded', loadToolsOnStartup);