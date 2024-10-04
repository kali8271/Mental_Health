// script.js

// Establish a WebSocket connection to the Django server
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

// Get references to the chat log and input fields
const chatLog = document.getElementById('chat-log');
const chatMessageInput = document.getElementById('chat-message-input');
const chatMessageSubmit = document.getElementById('chat-message-submit');

// When a message is received from the WebSocket
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data.message;

    // Append the message to the chat log
    chatLog.value += message + '\n';
    chatLog.scrollTop = chatLog.scrollHeight;  // Scroll to the bottom
};

// When the WebSocket is closed
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// When the Send button is clicked
chatMessageSubmit.onclick = function(e) {
    const message = chatMessageInput.value;

    // Send the message to the server
    chatSocket.send(JSON.stringify({
        'message': message
    }));

    // Clear the input field
    chatMessageInput.value = '';
};

// Allow pressing Enter to send a message
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // Enter key
        chatMessageSubmit.click();  // Trigger the click event
    }
};
