// Обработка мобильного меню
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Эффект прокрутки для шапки
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Слайдшоу для страницы Fly Yoga
const initSlideshow = () => {
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    let slideIndex = 0;

    if (slides.length === 0) return;

    function showSlide(n) {
        slideIndex = n;
        if (slideIndex >= slides.length) slideIndex = 0;
        if (slideIndex < 0) slideIndex = slides.length - 1;

        slides.forEach(slide => slide.style.display = 'none');
        slides[slideIndex].style.display = 'block';
    }

    function nextSlide() {
        showSlide(slideIndex + 1);
    }

    function prevSlide() {
        showSlide(slideIndex - 1);
    }

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', prevSlide);
        nextButton.addEventListener('click', nextSlide);
    }

    // Автоматическое переключение слайдов
    showSlide(0);
    setInterval(nextSlide, 5000);
};

// Модальное окно для изображений
const initImageModal = () => {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const closeBtn = modal?.querySelector('.close');

    if (!modal || !modalImg) return;

    window.openImageModal = (src) => {
        modal.style.display = 'block';
        modalImg.src = src;
        // Добавляем небольшую задержку перед добавлением класса show для анимации
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);
    };

    const closeModal = () => {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300); // Время должно совпадать с длительностью transition в CSS
    };

    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Добавляем обработку клавиши Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });
};

// Плавная прокрутка к секциям
const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
                // Закрываем мобильное меню при клике на ссылку
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });
};

// FAQ Accordion
const initFaq = () => {
    const questions = document.querySelectorAll('.faq-question');
    
    questions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            
            // Toggle active class on question
            question.classList.toggle('active');
            
            // Toggle max-height for answer animation
            if (question.classList.contains('active')) {
                answer.style.maxHeight = answer.scrollHeight + "px";
            } else {
                answer.style.maxHeight = 0;
            }
            
            // Close other items (Accordion behavior - optional, but user asked for harmony)
            questions.forEach(q => {
                if (q !== question && q.classList.contains('active')) {
                    q.classList.remove('active');
                    q.nextElementSibling.style.maxHeight = 0;
                }
            });
        });
    });
};

// Инициализация всех интерактивных элементов
document.addEventListener('DOMContentLoaded', () => {
    initSlideshow();
    initImageModal();
    initSmoothScroll();
    initFaq();
});