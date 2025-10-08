# WebSocket Example with Xyra

This example demonstrates how to use WebSocket with the Xyra framework for real-time communication.

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Run the WebSocket chat server:
```bash
python main.py
```

The WebSocket server will start on `ws://localhost:8000/chat`.

## Usage

### Server

The server implements a simple chat room where:
- Clients connect to `/chat` endpoint
- Messages are broadcasted to all connected clients
- Connection/disconnection events are logged

### Client

You can connect using any WebSocket client. Here's a simple HTML/JavaScript example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
</head>
<body>
    <div id="messages"></div>
    <input type="text" id="messageInput" placeholder="Type message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        const ws = new WebSocket('ws://localhost:8000/chat');
        const messages = document.getElementById('messages');
        const input = document.getElementById('messageInput');

        ws.onopen = function(event) {
            console.log('Connected to WebSocket');
        };

        ws.onmessage = function(event) {
            const messageDiv = document.createElement('div');
            messageDiv.textContent = event.data;
            messages.appendChild(messageDiv);
        };

        ws.onclose = function(event) {
            console.log('Disconnected from WebSocket');
        };

        function sendMessage() {
            const message = input.value;
            if (message) {
                ws.send(message);
                input.value = '';
            }
        }

        // Send on Enter key
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```

## WebSocket Features Used

- **Connection handling**: `open`, `message`, `close` events
- **Broadcasting**: Messages sent to all connected clients
- **Client management**: Tracking connected clients
- **Real-time communication**: Bidirectional messaging

## Testing WebSocket

1. **Health check** (excluded from rate limiting):
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test rate limiting** by making many requests:
   ```bash
   for i in {1..105}; do curl -s http://localhost:8000/health; done
   ```

3. **Check rate limit headers**:
   ```bash
   curl -v http://localhost:8000/health
   ```

## API Reference

For more WebSocket features, see the [Xyra WebSocket documentation](https://github.com/xyra/framework/docs/websocket.md).