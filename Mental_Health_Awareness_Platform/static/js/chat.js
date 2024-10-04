// Get the chat room name from the data attribute of the body tag
const chatRoomName = JSON.parse(document.getElementById('chat-room-name').textContent);

// Create a new WebSocket connection to the chat room
const chatSocket = new WebSocket(
    `ws://${window.location.host}/ws/chat/${chatRoomName}/`
);

// DOM elements
const chatLog = document.getElementById('chat-log');
const chatMessageInput = document.getElementById('chat-message-input');
const chatMessageSubmit = document.getElementById('chat-message-submit');

// Function to append messages to the chat log
function appendMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    chatLog.appendChild(messageElement);
}

// Handle incoming WebSocket messages
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    appendMessage(data.message);
};

// Handle WebSocket connection close
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// Send message on form submit
chatMessageSubmit.onclick = function(e) {
    const message = chatMessageInput.value;
    if (message) {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        chatMessageInput.value = '';  // Clear input after sending
    }
};

// Optional: Allow pressing Enter to send the message
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // Enter key
        chatMessageSubmit.click();
    }
};
