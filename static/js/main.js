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

    // Handle dynamic login UI updates
    window.addEventListener('user-login-success', () => {
        const loginLink = document.querySelector('a[href="/login"]');
        if (loginLink) {
            const parent = loginLink.parentNode;
            const baseClass = loginLink.className;

            // Create Profile Link
            const profileLink = document.createElement('a');
            profileLink.href = '/profile';
            profileLink.textContent = 'Profile';
            profileLink.className = baseClass;

            // Create Logout Link
            const logoutLink = document.createElement('a');
            logoutLink.href = '/logout';
            logoutLink.textContent = 'Logout';
            logoutLink.className = baseClass;

            // Insert new links and remove login
            if (parent.tagName === 'LI') {
                // If inside a list (common in navs), create new list items
                const profileLi = document.createElement('li'); profileLi.appendChild(profileLink);
                const logoutLi = document.createElement('li'); logoutLi.appendChild(logoutLink);
                parent.replaceWith(profileLi, logoutLi);
            } else {
                // Direct replacement
                loginLink.replaceWith(profileLink, document.createTextNode(' '), logoutLink);
            }
        }

        // Also remove the register link
        const registerLink = document.querySelector('a[href="/register"]');
        if (registerLink) {
            const parent = registerLink.parentNode;
            // If the link is inside a list item, remove the whole item
            if (parent.tagName === 'LI') {
                parent.remove();
            } else {
                registerLink.remove();
            }
        }
    });
});
