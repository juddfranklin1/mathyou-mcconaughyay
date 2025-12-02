class MathContent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    waitForKaTeX() {
        return new Promise(resolve => {
            const checkKaTeX = () => {
                if (window.katex && window.renderMathInElement) {
                    resolve();
                } else {
                    setTimeout(checkKaTeX, 100);
                }
            };
            checkKaTeX();
        });
    }

    convertToUrlSafe(str) {
        return str.replace(/[^a-zA-Z0-9]/g, '_');
    }

    convertFromUrlSafe(str) {
        const select = this.shadowRoot.getElementById('concept-select');
        // Find the original concept name by comparing URL-safe versions
        return Array.from(select.options)
            .find(opt => this.convertToUrlSafe(opt.value) === str)?.value;
    }

    loadConceptFromHash() {
        const hash = window.location.hash.slice(1); // Remove the # symbol
        if (hash) {
            const select = this.shadowRoot.getElementById('concept-select');
            const originalConcept = this.convertFromUrlSafe(hash);
            if (originalConcept) {
                select.value = originalConcept;
                // Trigger the change event to load the concept
                select.dispatchEvent(new Event('change'));
            }
        }
    }

    async renderContent() {
        const conceptType = this.getAttribute('concept-type');
        const concepts = JSON.parse(this.getAttribute('concepts') || '[]');
        
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    font-family: Arial, sans-serif;
                }
                .overview {
                    margin-bottom: 20px;
                    text-align: justify;
                }
                .overview p {
                    margin-bottom: 10px;
                }
                #concept-details {
                    margin-top: 30px;
                }
                #formula {
                    font-size: 1.3em;
                    margin-bottom: 15px;
                }
                #explanation {
                    font-size: 1em;
                    color: #333;
                }
                #study-plan {
                    margin-top: 30px;
                    border-top: 2px solid #eee;
                    padding-top: 20px;
                }
                #study-plan h3 {
                    color: #2c3e50;
                    margin-bottom: 20px;
                }
                #study-plan h4 {
                    color: #34495e;
                    margin: 15px 0 10px 0;
                }
                #study-plan ul {
                    list-style-type: none;
                    padding-left: 20px;
                }
                #study-plan ul li {
                    margin: 8px 0;
                    position: relative;
                }
                #study-plan ul li:before {
                    content: "•";
                    color: #3498db;
                    font-weight: bold;
                    position: absolute;
                    left: -15px;
                }
                select {
                    width: 100%;
                    padding: 8px;
                    margin-top: 10px;
                    margin-bottom: 20px;
                }
                label {
                    font-weight: bold;
                }
                ::slotted(div) {
                    font-family: Arial, sans-serif;
                }
                .katex {
                    font: normal 1.1em KaTeX_Main, Times New Roman, serif;
                    line-height: 1.2;
                    white-space: normal;
                    text-indent: 0;
                }
                .katex-display {
                    margin: 0.5em 0;
                }
                .katex-html {
                    white-space: normal;
                }
                .overview p {
                    line-height: 1.6;
                }
                #practice-section {
                    margin-top: 30px;
                    border-top: 2px solid #eee;
                    padding-top: 20px;
                }
                .concept-section {
                    margin-bottom: 20px;
                }
                .concept-section h4 {
                    color: #34495e;
                    padding-top: 20px;
                }
            </style>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
            <div class="overview">
                <slot name="overview"></slot>
            </div>
            <label for="concept-select">Choose a concept:</label>
            <select id="concept-select">
                <option value="" selected disabled>Select a concept</option>
                ${concepts.map(concept => `<option value="${concept}">${concept}</option>`).join('')}
            </select>
            <div id="concept-details">
                <div id="concept-details-container"></div>
                <div id="practice-section"></div>
            </div>
        `;

        // Initialize KaTeX for the overview content
        const slot = this.shadowRoot.querySelector('slot');
        const renderMath = (element) => {
            const paragraphs = element.getElementsByTagName('p');
            Array.from(paragraphs).forEach(p => {
                const text = p.innerHTML;
                const parts = text.split(/(\$[^\$]+\$)/g);
                const rendered = parts.map(part => {
                    if (part.startsWith('$') && part.endsWith('$')) {
                        const math = part.slice(1, -1);
                        try {
                            return window.katex.renderToString(math, {
                                displayMode: false,
                                throwOnError: false,
                                output: 'html',
                                strict: false
                            });
                        } catch (e) {
                            return part;
                        }
                    }
                    return part;
                });
                p.innerHTML = rendered.join('');
            });
        };

        slot.addEventListener('slotchange', () => {
            const elements = slot.assignedElements();
            elements.forEach(renderMath);
        });

        // Set up concept selection handling
        const select = this.shadowRoot.getElementById('concept-select');
        const conceptDetailsContainer = this.shadowRoot.getElementById('concept-details-container');

        select.addEventListener('change', () => {
            const concept = select.value;
            if (!concept) return;
            
            // Update URL hash when concept changes
            window.location.hash = this.convertToUrlSafe(concept);

            let endpoint = '';
            if (conceptType === 'linear-algebra') {
                endpoint = `/concept?name=${encodeURIComponent(concept)}`;
            } else if (conceptType === 'calculus') {
                endpoint = `/calculus_concept?name=${encodeURIComponent(concept)}`;
            } else if (conceptType === 'integration') {
                endpoint = `/integration_concept?name=${encodeURIComponent(concept)}`;
            } else if (conceptType === 'trigonometry') {
                endpoint = `/trigonometry_concept?name=${encodeURIComponent(concept)}`;
            }

            if (!endpoint) return;

            fetch(endpoint)
                .then(response => response.json())
                .then(data => {
                    // Clear all content
                    conceptDetailsContainer.innerHTML = '';
                    
                    const renderSection = (title, content) => {
                        if (!content || !content.trim()) return '';

                        // Render KaTeX for inline math
                        const renderedContent = content.split(/(\$[^\$]+\$)/g).map(part => {
                            if (part.startsWith('$') && part.endsWith('$')) {
                                const math = part.slice(1, -1);
                                try {
                                    return window.katex.renderToString(math, {
                                        displayMode: false,
                                        throwOnError: false
                                    });
                                } catch (e) {
                                    return part;
                                }
                            }
                            return part;
                        }).join('');

                        return `
                            <div class="concept-section">
                                <h4>${title}</h4>
                                <div>${renderedContent}</div>
                            </div>
                        `;
                    };

                    let contentHTML = '';
                    contentHTML += renderSection('Core Idea', data.core_idea);
                    contentHTML += renderSection('Real-World Application', data.real_world_application);
                    contentHTML += renderSection('Mathematical Demonstration', data.mathematical_demonstration);
                    contentHTML += renderSection('Explanation', data.explanation);

                    // Add study plan section if it exists
                    if (data.study_plan && data.study_plan.trim()) {
                        contentHTML += `
                            <div class="concept-section">
                                <h4>Study Plan</h4>
                                <div>${data.study_plan}</div>
                            </div>
                        `;
                    }

                    // Update the container with all content
                    conceptDetailsContainer.innerHTML = contentHTML;

                    // Render math in study plan if it exists
                    if (data.study_plan && window.renderMathInElement) {
                        window.renderMathInElement(
                            conceptDetailsContainer, 
                            {
                                delimiters: [
                                    {left: "$", right: "$", display: false},
                                    {left: "$$", right: "$$", display: true}
                                ],
                                throwOnError: false
                            }
                        );
                    }

                    // Handle practice problems
                    const practiceSection = this.shadowRoot.getElementById('practice-section');
                    const practiceProblems = JSON.parse(this.getAttribute('practice-problems') || '{}');
                    console.log('Practice problems for ' + concept + ':', practiceProblems[concept]);
                    if (practiceProblems[concept]) {
                        const problems = practiceProblems[concept];
                        if (Array.isArray(problems)) {
                            // Handle array of problems
                            try {
                                const renderedProblems = problems.map(problem => {
                                    console.log('Processing problem:', problem);
                                    // Properly escape the JSON string for HTML attribute
                                    const problemDataAttr = JSON.stringify(problem)
                                        .replace(/&/g, '&amp;')
                                        .replace(/'/g, '&apos;')
                                        .replace(/"/g, '&quot;')
                                        .replace(/</g, '&lt;')
                                        .replace(/>/g, '&gt;');
                                    
                                    return `
                                        <div style="margin-bottom: 20px;">
                                            <practice-problem problem-data="${problemDataAttr}"></practice-problem>
                                        </div>
                                    `;
                                }).join('');
                                
                                practiceSection.innerHTML = `
                                    <h3 style="color: #2c3e50; margin-bottom: 20px;">💪 Practice Problems</h3>
                                    ${renderedProblems}
                                `;
                                console.log('Practice section HTML updated');
                            } catch (error) {
                                console.error('Error rendering practice problems:', error);
                            }
                        } else {
                            // Handle single problem
                            practiceSection.innerHTML = `
                                <h3 style="color: #2c3e50; margin-bottom: 20px;">💪 Practice Problem</h3>
                                <practice-problem problem-data='${JSON.stringify(problems)}'></practice-problem>
                            `;
                        }
                    } else {
                        practiceSection.innerHTML = '';
                    }
                });
        });
    }

    async connectedCallback() {
        await this.waitForKaTeX();
        await this.renderContent();

        // Check for concept in URL hash and load it
        this.loadConceptFromHash();

        // Listen for hash changes
        window.addEventListener('hashchange', () => this.loadConceptFromHash());

        // Render initial content
        const elements = this.shadowRoot.querySelector('slot').assignedElements();
        elements.forEach(element => {
            if (window.renderMathInElement) {
                window.renderMathInElement(element, {
                    delimiters: [
                        {left: "$", right: "$", display: false},
                        {left: "$$", right: "$$", display: true}
                    ],
                    throwOnError: false
                });
            }
        });
    }
}

window.addEventListener('load', () => {
    customElements.define('math-content', MathContent);
});