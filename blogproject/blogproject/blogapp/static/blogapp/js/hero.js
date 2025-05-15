

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

