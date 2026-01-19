class MathContent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.conceptCache = {};
        this.overviewCache = null;
    }

    static get observedAttributes() {
        return ['discipline-id', 'discipline-name'];
    }

    connectedCallback() {
        this.disciplineId = this.getAttribute('discipline-id');
        this.disciplineName = this.getAttribute('discipline-name');
        this.render();
        this.problems = this.dataset.problems ? JSON.parse(this.dataset.problems) : {};
        this.addEventListeners();
        this.handleInitialLoad();
        this.renderMathInOverview();
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
                
                .katex-html {
                    display: none;
                }
            </style>
            <div class="content-area">
                <div id="overview-content" class="active">
                    <slot name="overview"></slot>
                </div>
                <div id="concept-content"></div>
            </div>
        `;
    }

    addEventListeners() {
        // Note: The nav is in the light DOM, so we listen on the document.
        document.addEventListener('click', (event) => {
            // Use the data-attribute as the selector for robustness.
            const target = event.target.closest('[data-menu="concept-nav"] [data-concept]');
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
        // Use data-attributes for selection, scoped to the concept navigation.
        const navLink = document.querySelector(`[data-menu="concept-nav"] [data-concept="${conceptId}"]`);
        if (navLink) {
            document.querySelectorAll('[data-menu="concept-nav"] [data-concept]').forEach(link => link.classList.remove('active'));
            navLink.classList.add('active');

            if (conceptId === 'overview') {
                this.displayOverview();
            } else {
                this.fetchAndDisplayConcept(conceptId);
            }
        }
    }
    async displayOverview() {
        const overviewContent = this.shadowRoot.getElementById('overview-content');
        const conceptContent = this.shadowRoot.getElementById('concept-content');

        overviewContent.classList.add('active');
        conceptContent.classList.remove('active');

        if (this.overviewCache) {
            overviewContent.innerHTML = this.overviewCache;
            if (window.renderMathInElement) {
                window.renderMathInElement(overviewContent, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "$", right: "$", display: false},
                        {left: "\\(", right: "\\)", display: false},
                        {left: "\\[", right: "\\]", display: true}
                    ]
                });
            }
            return;
        }

        overviewContent.innerHTML = `<div class="loading"><p>Alright, alright, alright... just take a breath. Let the pixels load, man. We’re just cruising, we’ll be there in a second. Trust the process, brother.</p></div>`;
        const load_failure_excuse = `<p>Alright, alright, alright... look here now. There was a lot I was gonna tell you about ${this.disciplineName} you’re lookin’ for? It’s havin’ a little trouble launching, man. It’s not in the cards right now. Just keep livin’, though, we’ll get it another time. It’s just... not a green light.</p>`;

        try {
            const response = await fetch(`/api/overview?discipline=${this.disciplineId}`);
            if (response.ok) {
                const data = await response.json();
                if (data.overview) {
                    const formattedText = data.overview.split('\n').filter(line => line.trim() !== '').map(line => `<p>${line}</p>`).join('');
                    const overviewHtml = `<div class="overview-text">${formattedText}</div>`;
                    this.overviewCache = overviewHtml;
                    overviewContent.innerHTML = overviewHtml;

                    if (window.renderMathInElement) {
                        window.renderMathInElement(overviewContent, {
                            delimiters: [
                                {left: "$$", right: "$$", display: true},
                                {left: "$", right: "$", display: false},
                                {left: "\\(", right: "\\)", display: false},
                                {left: "\\[", right: "\\]", display: true}
                            ]
                        });
                    }
                } else {
                    overviewContent.innerHTML = load_failure_excuse;
                }
            } else {
                 overviewContent.innerHTML = load_failure_excuse;
            }
            this.overviewFetched = true;
        } catch (error) {
            console.error('Error fetching overview:', error);
            overviewContent.innerHTML = load_failure_excuse;
        }
    }

    renderMathInOverview() {
        // The overview content is passed via a slot. We need to render math in it.
        // We do this once, as the slotted content is not expected to change.
        if (window.renderMathInElement && !this.overviewRendered) {
            const overviewContent = this.shadowRoot.getElementById('overview-content');
            console.log("overview content:", overviewContent);
            window.renderMathInElement(overviewContent, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ]
            });
            this.overviewRendered = true; // Ensure we only do this once.
        }
    }

    async fetchAndDisplayConcept(conceptId) {
        const overviewContent = this.shadowRoot.getElementById('overview-content');
        const conceptContent = this.shadowRoot.getElementById('concept-content');
        
        overviewContent.classList.remove('active');
        conceptContent.classList.add('active');
        conceptContent.innerHTML = `<div class="loading">Loading...</div>`;

        // Use cache if available
        if (this.conceptCache[conceptId]) {
            this.renderConcept(this.conceptCache[conceptId], conceptId);
            return;
        }

        try {
            const response = await fetch(`/api/concept?discipline=${this.disciplineId}&concept=${conceptId}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            this.conceptCache[conceptId] = data; // Cache the response
            this.renderConcept(data, conceptId);
        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('Fetch aborted');
            }
            conceptContent.innerHTML = `<p>Error loading concept. Please try again.</p>`;
            console.error('Fetch error:', error);
        }
    }

    renderConcept(data, conceptSlug) {
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
                innerHtml += String.raw`<h3>${key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h3><div>${data[key]}</div>`;
            }
        });

        // By creating a wrapper, the animation is re-triggered on each render.
        conceptContent.innerHTML = `<div class="concept-wrapper">${innerHtml}</div>`;

        // Now, check for and load practice problems for this concept.
        let concept_slug = conceptSlug || window.location.hash.substring(1);
        if (this.problems && this.problems[concept_slug]) {
            this.loadPracticeProblems(concept_slug, conceptContent);
        }

        // Tell KaTeX to look for new math to render inside the updated content.
        if (window.renderMathInElement) {
            window.renderMathInElement(conceptContent, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ]
            });
        }
    }

    async loadPracticeProblems(conceptSlug, container) {
        const problemIds = this.problems[conceptSlug];
        if (!problemIds || problemIds.length === 0) return;

        const problemsContainer = document.createElement('div');
        problemsContainer.className = 'practice-problems-container';
        problemsContainer.innerHTML = '<h3>Practice Problems</h3>';
        container.appendChild(problemsContainer);

        // This is the fetch iterator you were looking for.
        for (const problemId of problemIds) {
            try {
                const response = await fetch(`/api/question/${problemId}`);
                if (!response.ok) throw new Error(`Failed to fetch question ${problemId}`);
                const questionData = await response.json();

                const problemElement = document.createElement('practice-problem');
                problemElement.setAttribute('data-question', JSON.stringify(questionData));
                problemsContainer.appendChild(problemElement);

                console.log('question data:', questionData);

            } catch (error) {
                console.error(`Error loading practice problem ${problemId}:`, error);
            }
        }
    }
}

customElements.define('math-content', MathContent);