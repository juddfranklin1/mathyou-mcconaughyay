class MathContent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.conceptCache = {};
    }

    static get observedAttributes() {
        return ['discipline-id'];
    }

    connectedCallback() {
        this.disciplineId = this.getAttribute('discipline-id');
        this.render();
        this.addEventListeners();
        this.handleInitialLoad();
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'discipline-id' && oldValue !== newValue) {
            this.disciplineId = newValue;
        }
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin-top: 1.5rem;
                }
                .content-area {
                    padding: 1.5rem;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                    min-height: 300px;
                }
                .concept-title {
                    margin-top: 0;
                    color: #333;
                    border-bottom: 2px solid #007bff;
                    padding-bottom: 0.5rem;
                }
                .formula {
                    font-size: 1.2rem;
                    margin: 1rem 0;
                    padding: 1rem;
                    background-color: #fff;
                    border-left: 4px solid #007bff;
                }
                .explanation p {
                    line-height: 1.6;
                }
                #overview-content, #concept-content {
                    display: none;
                }
                #overview-content.active, #concept-content.active {
                    display: block;
                }
                .loading {
                    text-align: center;
                    padding: 2rem;
                    color: #888;
                }

                /* Animation for new content fading in */
                @keyframes fadeIn {
                    from {
                        opacity: 0;
                        transform: translateY(15px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .concept-wrapper {
                    animation: fadeIn 0.4s ease-out;
                }
            </style>
            <div class="content-area">
                <div id="overview-content" class="active">
                    <slot name="overview"></slot>
                </div>
                <div id="concept-content"></div>
            </div>
        `;
        // Ensure MathJax typesets the initial content if any
        if (window.MathJax) {
            window.MathJax.typesetPromise();
        }
    }

    addEventListeners() {
        // Note: The nav is in the light DOM, so we listen on the document.
        document.addEventListener('click', (event) => {
            const target = event.target.closest('.concept-link');
            if (!target) return;
            
            // We don't preventDefault, allowing the hash to change.
            const conceptId = target.dataset.concept;
            this.updateContent(conceptId);
        });

        // Also listen for back/forward browser navigation
        window.addEventListener('hashchange', () => {
            this.handleInitialLoad();
        });
    }

    handleInitialLoad() {
        const conceptId = window.location.hash.substring(1) || 'overview';
        this.updateContent(conceptId);
    }

    updateContent(conceptId) {
        const navLink = document.querySelector(`.concept-link[data-concept="${conceptId}"]`);
        if (navLink) {
            document.querySelectorAll('.concept-link').forEach(link => link.classList.remove('active'));
            navLink.classList.add('active');

            if (conceptId === 'overview') {
                this.displayOverview();
            } else {
                this.fetchAndDisplayConcept(conceptId);
            }
        }
    }
    displayOverview() {
        this.shadowRoot.getElementById('overview-content').classList.add('active');
        this.shadowRoot.getElementById('concept-content').classList.remove('active');
    }

    async fetchAndDisplayConcept(conceptId) {
        const overviewContent = this.shadowRoot.getElementById('overview-content');
        const conceptContent = this.shadowRoot.getElementById('concept-content');
        
        overviewContent.classList.remove('active');
        conceptContent.classList.add('active');
        conceptContent.innerHTML = `<div class="loading">Loading...</div>`;

        // Use cache if available
        if (this.conceptCache[conceptId]) {
            this.renderConcept(this.conceptCache[conceptId]);
            return;
        }

        try {
            const response = await fetch(`/api/concept?discipline=${this.disciplineId}&concept=${conceptId}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            this.conceptCache[conceptId] = data; // Cache the response
            this.renderConcept(data);
        } catch (error) {
            conceptContent.innerHTML = `<p>Error loading concept. Please try again.</p>`;
            console.error('Fetch error:', error);
        }
    }

    renderConcept(data) {
        const conceptContent = this.shadowRoot.getElementById('concept-content');
        // Wrap the content in a div to apply the animation
        let innerHtml = `<h2 class="concept-title">${data.name || 'Concept'}</h2>`;
        if (data.formula) {
            innerHtml += `<div class="formula">$$${data.formula}$$</div>`;
        }
        if (data.explanation) {
            innerHtml += `<div class="explanation">${data.explanation}</div>`;
        }
        // Add other fields like core_idea, real_world_application etc. if they exist
        ['core_idea', 'real_world_application', 'mathematical_demonstration', 'study_plan'].forEach(key => {
            if (data[key]) {
                innerHtml += `<h3>${key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h3><div>${data[key]}</div>`;
            }
        });

        // By creating a wrapper, the animation is re-triggered on each render.
        conceptContent.innerHTML = `<div class="concept-wrapper">${innerHtml}</div>`;

        // Tell MathJax to look for new math to render
        if (window.MathJax) {
            window.MathJax.typesetPromise([conceptContent]);
        }
    }
}

customElements.define('math-content', MathContent);