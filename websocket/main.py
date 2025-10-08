from xyra import App

app = App()

# Store connected clients (in production, use proper storage)
connected_clients = set()

def on_open(ws):
    connected_clients.add(ws)
    print(f"Client connected. Total clients: {len(connected_clients)}")
    ws.send("Welcome to chat room!")

def on_message(ws, message, opcode):
    print(f"Received: {message}")

    # Broadcast message to all clients
    for client in connected_clients:
        if client != ws:  # Don't send to sender
            client.send(f"User: {message}")

def on_close(ws, code, message):
    connected_clients.discard(ws)
    print(f"Client disconnected. Total clients: {len(connected_clients)}")

@app.get("/health")
def health():
    return {"status": "ok", "service": "websocket-chat"}

app.websocket("/chat", {
    "open": on_open,
    "message": on_message,
    "close": on_close
})

def main():
    print("🚀 Chat server with rate limiting running on ws://localhost:8000/chat")
    print("Health check: http://localhost:8000/health")
    app.listen(8000)

if __name__ == "__main__":
    main()