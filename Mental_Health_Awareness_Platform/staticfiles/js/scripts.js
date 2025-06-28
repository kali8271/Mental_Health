(function() {
    const roomNameElement = document.getElementById('chat-room-name');
    let roomName;

    if (roomNameElement) {
        try {
            roomName = JSON.parse(roomNameElement.textContent);
        } catch (e) {
            console.error("Failed to parse room name:", e);
        }
    } else {
        roomName = "{{ room_name }}";  // Fallback to template variable
    }

    if (roomName) {
        const chatLog = document.getElementById('chat-log');
        const chatMessageInput = document.getElementById('chat-message-input');
        const chatMessageSubmit = document.getElementById('chat-message-submit');

        // Function to append messages to the chat log
        function appendMessage(message) {
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            chatLog.appendChild(messageElement);
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        // Helper function to get correct WebSocket protocol
        function getWebSocketProtocol() {
            return window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        }

        // Retry logic to handle reconnection attempts
        let maxRetries = 5;
        let retryCount = 0;

        function connectWebSocket() {
            const protocol = getWebSocketProtocol();
            const chatSocket = new WebSocket(`${protocol}${window.location.host}/ws/chat/${roomName}/`);

            // Handle incoming messages
            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                appendMessage(data.message);
            };

            // Handle connection closure
            chatSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
                if (retryCount < maxRetries) {
                    retryCount++;
                    console.log(`Reconnection attempt ${retryCount}...`);
                    setTimeout(connectWebSocket, 3000);  // Retry after 3 seconds
                } else {
                    console.error('Max reconnection attempts reached.');
                }
            };

            // Handle WebSocket errors
            chatSocket.onerror = function(e) {
                console.error('WebSocket error occurred:', e.message || e);
                chatSocket.close();  // Force the socket to close
            };

            // Send message on form submit
            chatMessageSubmit.onclick = function() {
                const message = chatMessageInput.value.trim();
                if (message) {
                    chatSocket.send(JSON.stringify({ 'message': message }));
                    chatMessageInput.value = '';
                }
            };

            // Allow Enter key to send message
            chatMessageInput.onkeyup = function(e) {
                if (e.keyCode === 13) {  // Enter key
                    chatMessageSubmit.click();
                }
            };
        }

        // Initiate WebSocket connection
        connectWebSocket();
    } else {
        console.error('Room name is not available.');
    }
})();
