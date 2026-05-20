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