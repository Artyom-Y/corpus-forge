const chatDisplay = document.getElementById("dialogue");
const chatInput = document.getElementById("input-box");
const chatForm = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");

function appendMessage(message, sender) {
    const messageDiv = document.createElement('div');
    // Add classes to the messages and shi
    messageDiv.classList.add('message', `${sender}-msg`);

    if (sender === 'ai') {
        const rawhtml = marked.parse(message)
        const cleanhtml = DOMPurify.sanitize(rawhtml);
        messageDiv.innerHTML = cleanhtml;
    } else {
        messageDiv.textContent = message;
    }

    chatDisplay.appendChild(messageDiv);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

async function loadHistory() {
    try {
        const response = await fetch('/history');

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const historyData = await response.json();

        historyData.forEach(msg => {
            if (msg.role && msg.parts && msg.parts.length > 0) {
                const sender = msg.role === 'model' ? 'ai' : 'user';
                const text = msg.parts[0].text;

                appendMessage(text, sender);
            }
        });
    } catch (error) {
        console.error("Error loading history:", error);
    }
}

async function handleSendMessage(event) {
    event.preventDefault();

    const userText = chatInput.value.trim();
    if (userText === '') return;

    appendMessage(userText, 'user');
    chatInput.value = '';

    chatInput.disabled = true;
    sendBtn.disabled = true;

    try {
        const response = await fetch('/dialogue', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: userText, collections_names: []})
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        if (data.error) {
            appendMessage(data.error, 'error');
        } else {
            appendMessage(data.reply, 'ai');
        }

    } catch (error) {
        console.error("Error communicating with AI:", error);
        appendMessage("Sorry, I'm having trouble connecting right now.", 'error');
    } finally {
        chatInput.disabled = false;
        sendBtn.disabled = false;

        chatInput.focus();
    }
}

chatForm.addEventListener('submit', handleSendMessage);
sendBtn.addEventListener('click', handleSendMessage);

chatInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        handleSendMessage(event);
    }
});

window.addEventListener('DOMContentLoaded', loadHistory);