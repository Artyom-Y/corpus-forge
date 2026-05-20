const chatBox = document.getElementById("chat-box");
const inputBox = document.getElementById("input-box");
const sendButton = document.getElementById("send-btn");

function appendMessage( message, sender) {
    const messageDiv = document.createElement('div');
    // Add classes to the messages and shi
    messageDiv.classList.add('message', `${sender}-msg`);
    messageDiv.textContent = message;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function handleSendMessage() {
    const userText = inputBox.value.trim();
    if (userText === '') return;

    appendMessage(userText, 'user');
    inputBox.value = '';

    inputBox.disabled = true;
    sendButton.disabled = true;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: userText})
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        appendMessage(data.reply, 'ai');
    } catch (error) {
        console.error("Error communicating with AI:", error);
        appendMessage("Sorry, I'm having trouble connecting right now.", 'error');
    } finally {
        inputBox.disabled = false;
        sendButton.disabled = false;

        inputBox.focus();
    }
}

sendButton.addEventListener('click', handleSendMessage);

inputBox.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        handleSendMessage();
    }
});