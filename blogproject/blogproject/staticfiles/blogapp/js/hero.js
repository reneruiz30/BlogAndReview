

// hero.js OPTIMIZADO
document.addEventListener('DOMContentLoaded', () => {

    // ——— Cacheo de referencias ———
    const leftArrow  = document.querySelector('.carrusel-arrow.left');
    const rightArrow = document.querySelector('.carrusel-arrow.right');
    const container = document.getElementById('carruselCards');
    const cards = Array.from(document.querySelectorAll('.carrusel-card'));
    const heroBg = document.getElementById('heroBg');
    const mainTitle = document.getElementById('mainTitle');
    const indicator = document.getElementById('carruselIndicator');

    if (!container || !cards.length || !heroBg || !mainTitle || !indicator) return;

    // Oculta el carrusel y el fondo hasta que todo esté listo
    container.style.visibility = "hidden";
    heroBg.style.opacity = "0";

    let current = 0;
    let cardW = cards[0].offsetWidth || 200;
    const gap = 24;
    const loadedSet = new Set();

    function animateHeroBgKenBurns(newBg) {
        heroBg.classList.remove('kenburns');
        requestAnimationFrame(() => {
            heroBg.style.backgroundImage = `url('${newBg}')`;
            heroBg.classList.add('kenburns');
        });
    }

    function loadBg(card) {
        const src = card.dataset.bg;
        if (!src || loadedSet.has(src)) return;
        card.style.backgroundImage = `url('${src}')`;
        loadedSet.add(src);
    }

    function updateCarrusel() {
        // Animar las cards (CSS se encarga de la transición)
        cards.forEach((card, idx) => {
            card.classList.toggle('active', idx === current);
        });

        // Desplazamiento del carrusel con transición siempre activa
        const offset = (current - 2) * (cardW + gap);
        container.style.transform = `translateX(${-offset}px)`;

        const active = cards[current];
        mainTitle.textContent = active.dataset.title || '';
        indicator.textContent = String(current + 1).padStart(2, '0');

        loadBg(active);

        // Solo cambia el fondo y anima si la imagen es diferente
        const newBg = active.dataset.bg;
        const currentBg = heroBg.style.backgroundImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '');
        if (newBg && !currentBg.includes(newBg)) {
            heroBg.classList.add('fading');
            setTimeout(() => {
                heroBg.classList.remove('kenburns');
                heroBg.style.backgroundImage = `url('${newBg}')`;
                void heroBg.offsetWidth;
                heroBg.classList.add('kenburns');
                heroBg.classList.remove('fading');
            }, 400); // Debe coincidir con la transición de opacidad
        }
    }

    function moveCarrusel(dir) {
        current = (current + dir + cards.length) % cards.length;
        updateCarrusel();
    }

    container.addEventListener('click', e => {
        const card = e.target.closest('.carrusel-card');
        if (card && card.classList.contains('active') && card.dataset.url) {
            window.location.href = card.dataset.url;
        }
    });

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    window.addEventListener('resize', debounce(() => {
        if (cards.length) {
            cardW = cards[0].offsetWidth || 200;
            updateCarrusel();
        }
    }, 150));

    // Llama a updateCarrusel() inmediatamente para que el fondo se muestre desde el inicio
    updateCarrusel();

    // Precarga todas las imágenes de fondo antes de mostrar el carrusel y el fondo
    let loadedImages = 0;
    const bgImages = cards.map(card => card.dataset.bg).filter(Boolean);
    const heroBgImage = heroBg.style.backgroundImage
        .replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '');
    if (heroBgImage && !bgImages.includes(heroBgImage)) {
        bgImages.push(heroBgImage);
    }
    const totalImages = bgImages.length;

    function showCarrusel() {
        container.classList.add('ready'); // Activa la transición suave
        container.style.visibility = "visible";
        heroBg.style.transition = "opacity 0.6s";
        heroBg.style.opacity = "1";
        document.querySelectorAll('.user-info-header, .custom-header-actions').forEach(el => {
            el.classList.add('visible');
        });
        updateCarrusel();
    }

    if (leftArrow) leftArrow.addEventListener('click', () => moveCarrusel(-1));
    if (rightArrow) rightArrow.addEventListener('click', () => moveCarrusel(1));
    document.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft')  moveCarrusel(-1);
        if (e.key === 'ArrowRight') moveCarrusel(1);
    });

    if (totalImages === 0) {
        showCarrusel();
    } else {
        bgImages.forEach(src => {
            const img = new Image();
            img.src = src;
            img.onload = img.onerror = () => {
                loadedImages++;
                if (loadedImages === totalImages) {
                    showCarrusel();
                }
            };
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const chatToggleButton = document.getElementById('chatToggleButton');
    const chatWindow = document.getElementById('chatWindow');
    const closeChatButton = document.getElementById('closeChatButton');
    const chatMessagesContainer = document.querySelector('.chat-messages');
    const chatMessageInput = document.getElementById('chatMessageInput');
    const sendMessageButton = document.getElementById('sendMessageButton');

    // Function to toggle chat window visibility
    function toggleChatWindow() {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            // Scroll to the bottom of messages when opening
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
            chatMessageInput.focus(); // Focus on the input field
        }
    }

    // Event listener for opening the chat
    if (chatToggleButton) {
        chatToggleButton.addEventListener('click', toggleChatWindow);
    }

    // Event listener for closing the chat
    if (closeChatButton) {
        closeChatButton.addEventListener('click', toggleChatWindow);
    }

    // Function to send a message (for demonstration)
    function sendMessage() {
        const messageText = chatMessageInput.value.trim();
        if (messageText === '') {
            return; // Don't send empty messages
        }

        // Create new outgoing message element
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'outgoing');
        messageDiv.textContent = messageText;
        chatMessagesContainer.appendChild(messageDiv);

        // Clear input
        chatMessageInput.value = '';

        // Scroll to the bottom
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

        // Simulate a reply after a short delay (for demo purposes)
        setTimeout(() => {
            const replyDiv = document.createElement('div');
            replyDiv.classList.add('message', 'incoming');
            replyDiv.textContent = "Gracias por tu mensaje, te responderemos pronto.";
            chatMessagesContainer.appendChild(replyDiv);
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
        }, 1500); // Reply after 1.5 seconds
    }

    // Event listener for sending message on button click
    if (sendMessageButton) {
        sendMessageButton.addEventListener('click', sendMessage);
    }

    // Event listener for sending message on Enter key press
    if (chatMessageInput) {
        chatMessageInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Close chat window if clicking outside of it (optional, but good for UX)
    document.addEventListener('click', function(event) {
        if (chatWindow.classList.contains('active') &&
            !chatWindow.contains(event.target) &&
            !chatToggleButton.contains(event.target)) {
            toggleChatWindow();
        }
    });

    // Prevent clicks inside the chat window from propagating to document listener
    if (chatWindow) {
        chatWindow.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }
});