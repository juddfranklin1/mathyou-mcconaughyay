class PracticeProblem extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    async connectedCallback() {
        await this.waitForKaTeX();
        this.problemData = JSON.parse(this.getAttribute('problem-data'));
        this.renderContent();
        this.setupEventListeners();
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

    getInputTemplate() {
        switch(this.problemData.type) {
            case 'multiple_choice':
                return `
                    <div class="input-container multiple-choice">
                        ${this.problemData.choices.map((choice, index) => `
                            <div class="choice-item">
                                <input type="radio" id="choice-${index}" name="answer" value="${index}">
                                <label for="choice-${index}">${choice}</label>
                            </div>
                        `).join('')}
                        <button id="submit-btn">Submit Answer</button>
                    </div>
                `;
            case 'vector':
                return `
                    <div class="input-container vector">
                        <div class="vector-inputs">
                            [<input type="text" class="vector-component" placeholder="x">
                            <input type="text" class="vector-component" placeholder="y">
                            <input type="text" class="vector-component" placeholder="z">]
                        </div>
                        <button id="submit-btn">Submit Answer</button>
                    </div>
                `;
            case 'numerical':
            default:
                return `
                    <div class="input-container">
                        <input type="text" placeholder="Enter your answer..." id="answer-input">
                        <button id="submit-btn">Submit Answer</button>
                    </div>
                `;
        }
    }

    renderContent() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin: 20px 0;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .problem-container {
                    margin-bottom: 20px;
                }
                .problem-header {
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #2c3e50;
                }
                .problem-text {
                    margin-bottom: 15px;
                    line-height: 1.6;
                }
                .input-container {
                    margin-top: 15px;
                }
                input[type="text"] {
                    padding: 8px;
                    border: 2px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                    width: 200px;
                    margin-right: 10px;
                }
                .vector-inputs {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    margin-bottom: 15px;
                }
                .vector-component {
                    width: 80px !important;
                }
                .choice-item {
                    margin: 10px 0;
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                .choice-item:hover {
                    background-color: #f0f0f0;
                }
                .choice-item input[type="radio"] {
                    margin-right: 10px;
                }
                .choice-item label {
                    cursor: pointer;
                    display: inline-block;
                    width: calc(100% - 30px);
                }
                button {
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: background-color 0.3s;
                    margin-top: 10px;
                }
                button:hover {
                    background-color: #45a049;
                }
                .feedback {
                    margin-top: 15px;
                    padding: 10px;
                    border-radius: 4px;
                    display: none;
                }
                .feedback.success {
                    background-color: #dff0d8;
                    color: #3c763d;
                    border: 1px solid #d6e9c6;
                    display: block;
                }
                .feedback.error {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    display: block;
                }
                .difficulty {
                    display: inline-block;
                    padding: 4px 8px;
                    background: #e9ecef;
                    border-radius: 4px;
                    font-size: 0.9em;
                    color: #495057;
                    margin-bottom: 10px;
                }
                .explanation {
                    margin-top: 15px;
                    padding: 15px;
                    background-color: #e8f4f8;
                    border-radius: 4px;
                    display: none;
                }
            </style>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
            <div class="problem-container">
                <div class="difficulty">Difficulty: ${this.problemData.difficulty}</div>
                <div class="problem-header">Practice Problem</div>
                <div class="problem-text">${this.problemData.problem}</div>
                ${this.getInputTemplate()}
                <div id="feedback" class="feedback"></div>
                <div id="explanation" class="explanation"></div>
            </div>
        `;

        // Render any math in the problem text
        const mathElements = this.shadowRoot.querySelectorAll('.problem-text, .choice-item label');
        mathElements.forEach(element => {
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

    checkAnswer() {
        const feedback = this.shadowRoot.getElementById('feedback');
        const explanation = this.shadowRoot.getElementById('explanation');
        let isCorrect = false;

        switch(this.problemData.type) {
            case 'multiple_choice':
                const selectedOption = this.shadowRoot.querySelector('input[name="answer"]:checked');
                if (selectedOption) {
                    isCorrect = parseInt(selectedOption.value) === this.problemData.answer;
                }
                break;

            case 'vector':
                const components = Array.from(this.shadowRoot.querySelectorAll('.vector-component'))
                    .map(input => input.value.trim());
                const expectedComponents = JSON.parse(this.problemData.answer);
                isCorrect = components.every((comp, index) => 
                    comp === expectedComponents[index].toString());
                break;

            case 'numerical':
            default:
                const userAnswer = this.shadowRoot.getElementById('answer-input').value.trim();
                isCorrect = userAnswer === this.problemData.answer.toString();
                break;
        }

        if (isCorrect) {
            feedback.textContent = "Excellent work! That's correct! You're getting really good at this! 🎉";
            feedback.className = 'feedback success';
        } else {
            feedback.textContent = "Not quite right, but don't give up! Try reviewing the concept and attempt again. You've got this! 💪";
            feedback.className = 'feedback error';
        }

        // Show explanation regardless of correctness
        explanation.style.display = 'block';
        explanation.innerHTML = `<strong>Explanation:</strong><br>${this.problemData.explanation}`;
        if (window.renderMathInElement) {
            window.renderMathInElement(explanation, {
                delimiters: [
                    {left: "$", right: "$", display: false},
                    {left: "$$", right: "$$", display: true}
                ],
                throwOnError: false
            });
        }
    }

    setupEventListeners() {
        const submitBtn = this.shadowRoot.getElementById('submit-btn');
        submitBtn.addEventListener('click', () => this.checkAnswer());

        // Add enter key support for numerical input
        if (this.problemData.type === 'numerical') {
            const answerInput = this.shadowRoot.getElementById('answer-input');
            answerInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    submitBtn.click();
                }
            });
        }
    }
}

window.customElements.define('practice-problem', PracticeProblem);