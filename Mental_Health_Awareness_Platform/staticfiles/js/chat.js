(function() {
    // Get the chat room name from the data attribute of the body tag
    const chatRoomNameElement = document.getElementById('chat-room-name');
    if (chatRoomNameElement) {
        const chatRoomName = JSON.parse(chatRoomNameElement.textContent);

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
            if (chatLog) {
                const messageElement = document.createElement('div');
                messageElement.textContent = message;
                chatLog.appendChild(messageElement);
            } else {
                console.error('Chat log element not found');
            }
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
        if (chatMessageSubmit) {
            chatMessageSubmit.onclick = function(e) {
                const message = chatMessageInput ? chatMessageInput.value : '';
                if (message && chatSocket) {
                    chatSocket.send(JSON.stringify({
                        'message': message
                    }));
                    chatMessageInput.value = '';  // Clear input after sending
                }
            };
        } else {
            console.error('Chat message submit button not found');
        }

        // Optional: Allow pressing Enter to send the message
        if (chatMessageInput) {
            chatMessageInput.onkeyup = function(e) {
                if (e.keyCode === 13 && chatMessageSubmit) {  // Enter key
                    chatMessageSubmit.click();
                }
            };
        } else {
            console.error('Chat message input field not found');
        }
    } else {
        console.error('Chat room name element not found');
    }
})();
