// Animations et interactions pour OCR Pro
document.addEventListener('DOMContentLoaded', function() {
    
    // Animation d'entrée pour les cartes de fonctionnalités
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Appliquer l'animation aux cartes de fonctionnalités
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.2}s, transform 0.6s ease ${index * 0.2}s`;
        observer.observe(card);
    });

    // Animation pour les conteneurs de résultats
    const resultContainers = document.querySelectorAll('.result-container');
    resultContainers.forEach((container, index) => {
        container.style.opacity = '0';
        container.style.transform = 'translateY(20px)';
        container.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`;
        observer.observe(container);
    });

    // Animation du logo au chargement
    const logo = document.querySelector('.logo-container img');
    if (logo) {
        logo.style.transform = 'scale(0.8)';
        logo.style.transition = 'transform 0.5s ease';
        setTimeout(() => {
            logo.style.transform = 'scale(1)';
        }, 100);
    }

    // Effet de pulsation pour les boutons d'action
    const actionButtons = document.querySelectorAll('.btn-primary, .btn-success');
    actionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('pulse-animation');
        });
        button.addEventListener('mouseleave', function() {
            this.classList.remove('pulse-animation');
        });
    });

    // Animation de progression pour les indicateurs de statut
    const statusIndicators = document.querySelectorAll('.status-indicator');
    statusIndicators.forEach(indicator => {
        indicator.style.opacity = '0';
        indicator.style.transform = 'translateX(20px)';
        indicator.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        
        setTimeout(() => {
            indicator.style.opacity = '1';
            indicator.style.transform = 'translateX(0)';
        }, 300);
    });

    // Amélioration de l'upload avec drag & drop
    const uploadLabel = document.getElementById('uploadLabel');
    if (uploadLabel) {
        uploadLabel.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = 'var(--accent-color)';
            this.style.backgroundColor = 'rgba(76, 201, 240, 0.1)';
            this.style.transform = 'scale(1.02)';
        });

        uploadLabel.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.borderColor = 'var(--primary-color)';
            this.style.backgroundColor = '';
            this.style.transform = 'scale(1)';
        });

        uploadLabel.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = 'var(--primary-color)';
            this.style.backgroundColor = '';
            this.style.transform = 'scale(1)';
        });
    }

    // Animation de chargement personnalisée
    function showLoadingAnimation(element) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner me-2';
        element.prepend(spinner);
        
        element.style.opacity = '0.7';
        element.style.pointerEvents = 'none';
    }

    function hideLoadingAnimation(element) {
        const spinner = element.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
        element.style.opacity = '1';
        element.style.pointerEvents = 'auto';
    }

    // Appliquer les animations de chargement aux boutons
    const loadingButtons = document.querySelectorAll('[data-loading]');
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            showLoadingAnimation(this);
            
            // Simuler une opération asynchrone
            setTimeout(() => {
                hideLoadingAnimation(this);
            }, 2000);
        });
    });

    // Animation smooth scroll pour les ancres
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Effet de typing pour les textes d'information
    function typeWriter(element, text, speed = 50) {
        let i = 0;
        element.innerHTML = '';
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    }

    // Animation des compteurs (si présents)
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        }
        updateCounter();
    }

    // Gestion des tooltips personnalisés
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            setTimeout(() => tooltip.classList.add('show'), 10);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.custom-tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });

    // Notification système
    function showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-info-circle me-2"></i>
            <span>${message}</span>
            <button class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    // Exposer les fonctions utiles globalement
    window.OCRPro = {
        showLoadingAnimation,
        hideLoadingAnimation,
        showNotification,
        typeWriter,
        animateCounter
    };
});

// Styles CSS pour les animations personnalisées
const customStyles = `
    .custom-tooltip {
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        z-index: 1000;
        opacity: 0;
        transform: translateY(5px);
        transition: opacity 0.3s ease, transform 0.3s ease;
        pointer-events: none;
    }
    
    .custom-tooltip.show {
        opacity: 1;
        transform: translateY(0);
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 300px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #28a745;
    }
    
    .notification-error {
        border-left: 4px solid #dc3545;
    }
    
    .notification-info {
        border-left: 4px solid #17a2b8;
    }
    
    .notification .btn-close {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        opacity: 0.5;
        margin-left: auto;
    }
    
    .notification .btn-close:hover {
        opacity: 1;
    }
`;

// Injecter les styles personnalisés
const styleSheet = document.createElement('style');
styleSheet.textContent = customStyles;
document.head.appendChild(styleSheet);
