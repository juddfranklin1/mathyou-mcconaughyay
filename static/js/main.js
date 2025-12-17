document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('[data-action="toggle-nav"]');
    const navMenu = document.querySelector('[data-target="nav-menu"]');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('is-active');
            navMenu.classList.toggle('is-open');
            document.body.classList.toggle('nav-open');
        });
    }
});
