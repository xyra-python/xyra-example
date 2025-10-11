from xyra import App

app = App()

# Test decorator syntax
@app.websocket("/echo")
def echo_handler(ws):
    print("Client connected to /echo")
    ws.send("Welcome to echo server!")

# Test method call syntax
def on_open(ws):
    print("Client connected to /chat")
    ws.subscribe("chat")
    ws.send("Welcome to chat room!")

def on_message(ws, message, opcode):
    print(f"Received: {message}")
    # Echo back
    ws.send(f"Echo: {message}")

def on_close(ws, code, message):
    print("Client disconnected from /chat")

app.websocket("/chat", {
    "open": on_open,
    "message": on_message,
    "close": on_close
})

if __name__ == "__main__":
    app.listen(8000)