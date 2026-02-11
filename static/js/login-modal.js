class LoginModal extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
        this.setupEventListeners();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <link rel="stylesheet" href="/static/css/web-components/login-modal.css">
            <div class="modal-overlay" id="overlay">
                <div class="modal-content">
                    <button class="close-btn" id="close">&times;</button>
                    <div id="login-container">
                        <h2>Login Required</h2>
                        <div class="error" id="error-msg"></div>
                        <form id="login-form">
                            <input type="email" id="email" placeholder="Email Address" required>
                            <input type="password" id="password" placeholder="Password" required>
                            <button type="submit">Login</button>
                        </form>
                    </div>
                    <div id="success-msg" style="display: none; text-align: center;">
                        <h2>Alright, alright, alright.</h2>
                        <p>You're in. Let's keep livin'.</p>
                    </div>
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        const form = this.shadowRoot.getElementById('login-form');
        const overlay = this.shadowRoot.getElementById('overlay');
        const closeBtn = this.shadowRoot.getElementById('close');

        const closeModal = () => this.hide();

        closeBtn.addEventListener('click', closeModal);
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeModal();
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = this.shadowRoot.getElementById('email').value;
            const password = this.shadowRoot.getElementById('password').value;
            const errorMsg = this.shadowRoot.getElementById('error-msg');

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    // Show success message
                    this.shadowRoot.getElementById('login-container').style.display = 'none';
                    this.shadowRoot.getElementById('success-msg').style.display = 'block';
                    
                    // Dispatch event for main.js to pick up
                    window.dispatchEvent(new CustomEvent('user-login-success'));

                    setTimeout(() => {
                        this.hide();
                    }, 2000);
                } else {
                    errorMsg.textContent = data.message || 'Login failed';
                    errorMsg.style.display = 'block';
                }
            } catch (err) {
                errorMsg.textContent = 'An error occurred. Please try again.';
                errorMsg.style.display = 'block';
            }
        });
    }

    show() { this.shadowRoot.getElementById('overlay').classList.add('open'); }
    hide() { 
        this.shadowRoot.getElementById('overlay').classList.remove('open'); 
        this.shadowRoot.getElementById('error-msg').style.display = 'none';
        this.shadowRoot.getElementById('login-form').reset();
        // Reset view state
        this.shadowRoot.getElementById('login-container').style.display = 'block';
        this.shadowRoot.getElementById('success-msg').style.display = 'none';
    }
}
customElements.define('login-modal', LoginModal);