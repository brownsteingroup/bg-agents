const form = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const responseDiv = document.getElementById('response');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    responseDiv.innerText = "";
    const message = userInput.value;
    const ws = new WebSocket(`ws://${window.location.host}/ws?message=${encodeURIComponent(message)}`);
    ws.onopen = () => {
        console.log("WebSocket connection opened");
    };
    ws.onmessage = (event) => {
        responseDiv.innerText += event.data;
    };
    ws.onclose = () => {
        console.log("WebSocket connection closed");
    };
});