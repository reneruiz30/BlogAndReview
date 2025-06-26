// Obtener el ID del blog del elemento HTML
const chatContainer = document.getElementById('chat-container');
const blogId = chatContainer.dataset.blogId; // Si usaste el atributo data-blog-id

// O si definiste la variable blogId directamente en el script HTML:
// const blogId = blogId; // Ya estaría disponible si la definiste arriba.

// Construir la URL del WebSocket
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + blogId // ¡Aquí usamos el ID del blog!
    + '/'
);

// ... el resto de tu código WebSocket ...

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // ... manejar el mensaje ...
    console.log(data.message);
    // Añade el mensaje al div de chat (ejemplo)
    document.querySelector('#chat-log').value += (data.user + ': ' + data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Socket de chat cerrado inesperadamente');
};

document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};