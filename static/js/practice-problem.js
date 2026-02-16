class PracticeProblem extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    async connectedCallback() {
        await this.waitForKaTeX();
        this.problemData = JSON.parse(this.getAttribute('data-question'));
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
            <link rel="stylesheet" href="/static/css/web-components/practice-problem.css">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
            <div class="problem-container">
                <div class="difficulty">Difficulty: ${this.problemData.difficulty}</div>
                <div class="problem-header">Practice Problem</div>
                <div class="problem-text">${this.problemData.problem}</div>
                ${this.getInputTemplate()}
                <div id="feedback" class="feedback"></div>
                <div id="explanation" class="explanation"></div>
                <button id="next-btn">Try Another</button>
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

    calculateLocalCorrectness(userAnswer) {
        const correctAnswer = this.problemData.answer;
        if (correctAnswer === undefined || correctAnswer === null) return null;

        if (Array.isArray(userAnswer)) {
            if (!Array.isArray(correctAnswer)) return false;
            if (userAnswer.length !== correctAnswer.length) return false;
            return userAnswer.every((val, index) => 
                String(val).trim() === String(correctAnswer[index]).trim()
            );
        }
        return String(userAnswer).trim() === String(correctAnswer).trim();
    }

    async checkAnswer() {
        const feedback = this.shadowRoot.getElementById('feedback');
        const explanation = this.shadowRoot.getElementById('explanation');
        const submitBtn = this.shadowRoot.getElementById('submit-btn');
        
        // Disable button and show loading state
        submitBtn.disabled = true;
        const originalBtnText = submitBtn.textContent;
        submitBtn.textContent = 'Checking...';
        
        let userAnswer;

        // Extract the answer based on the problem type
        switch(this.problemData.type) {
            case 'multiple_choice':
                const selectedOption = this.shadowRoot.querySelector('input[name="answer"]:checked');
                if (selectedOption) {
                    userAnswer = parseInt(selectedOption.value);
                }
                break;

            case 'vector':
                userAnswer = Array.from(this.shadowRoot.querySelectorAll('.vector-component'))
                    .map(input => input.value.trim());
                break;

            case 'numerical':
            default:
                userAnswer = this.shadowRoot.getElementById('answer-input').value.trim();
                break;
        }

        // Basic client-side validation to ensure an answer was provided
        if (userAnswer === undefined || userAnswer === '' || (Array.isArray(userAnswer) && userAnswer.some(c => c === ''))) {
            feedback.textContent = "Please provide an answer before submitting.";
            feedback.className = 'feedback error';
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
            return;
        }

        // Local Check for Instant Feedback
        const isCorrectLocal = this.calculateLocalCorrectness(userAnswer);
        feedback.style.display = 'block';
        
        if (isCorrectLocal !== null) {
            feedback.className = isCorrectLocal ? 'feedback success' : 'feedback error';
            feedback.style.backgroundColor = '';
            feedback.innerHTML = `<strong>${isCorrectLocal ? "You're right, You're right, You're right!" : "Can't win 'em all. Let's get some learnin'."}</strong> <span style="opacity: 0.7;">Hold your horses while I cook up some thoughts on this...</span><div class="spinner"></div>`;
        } else {
            // Fallback if we can't check locally
            feedback.innerHTML = `Alright, alright, alright... let's see if the math is mathin'.<div class="spinner"></div>`;
            feedback.className = 'feedback';
            feedback.style.backgroundColor = '#e9ecef';
        }

        try {
            const response = await fetch('/api/question/submit_answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_id: this.problemData.id,
                    answer: userAnswer
                })
            });

            // Check if the request was redirected (e.g., to the login page)
            if (response.redirected || response.status === 401) {
                const loginModal = document.querySelector('login-modal');
                if (loginModal) {
                    feedback.style.display = 'none'; // Hide the "Please wait" message
                    loginModal.show();
                    return;
                }
                // Fallback if modal is missing
                feedback.style.backgroundColor = '';
                feedback.innerHTML = 'You must be <a href="/login" target="_top">logged in</a> to submit answers.';
                feedback.className = 'feedback error';
                return;
            }

            if (!response.ok) {
                throw new Error('Submission failed');
            }

            const result = await response.json();

            // Clear temporary styles
            feedback.style.backgroundColor = '';
            feedback.style.display = '';
            
            feedback.className = result.correct ? 'feedback success' : 'feedback error';
            feedback.innerHTML = result.explanation;

            // Show the "Try Another" button
            const nextBtn = this.shadowRoot.getElementById('next-btn');
            if (nextBtn) nextBtn.style.display = 'block';

            if (window.renderMathInElement) {
                window.renderMathInElement(feedback, {
                    delimiters: [
                        {left: "$", right: "$", display: false},
                        {left: "$$", right: "$$", display: true}
                    ],
                    throwOnError: false
                });
            }

        } catch (error) {
            console.error('Error submitting answer:', error);
            feedback.textContent = "An error occurred while submitting your answer. Please try again.";
            feedback.className = 'feedback error';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
        }
    }

    async loadNextQuestion() {
        const nextBtn = this.shadowRoot.getElementById('next-btn');
        const originalText = nextBtn.textContent;
        nextBtn.textContent = 'Loading...';
        nextBtn.disabled = true;

        try {
            const response = await fetch(`/api/question/next?current_id=${this.problemData.id}`);
            if (!response.ok) throw new Error('Failed to load next question');
            
            this.problemData = await response.json();
            this.renderContent();
            this.setupEventListeners();
        } catch (error) {
            console.error('Error loading next question:', error);
            nextBtn.textContent = 'Error';
            setTimeout(() => {
                nextBtn.textContent = originalText;
                nextBtn.disabled = false;
            }, 2000);
        }
    }

    setupEventListeners() {
        const submitBtn = this.shadowRoot.getElementById('submit-btn');
        submitBtn.addEventListener('click', () => this.checkAnswer());
        
        const nextBtn = this.shadowRoot.getElementById('next-btn');
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.loadNextQuestion());
        }

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