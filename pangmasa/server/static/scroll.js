document.addEventListener('scroll', () => {
    const nav = document.getElementById('nav');

    if (window.scrollY > 0) {
        nav.classList.add('scrolled');
    }

    else {
        nav.classList.remove('scrolled');
    }
})