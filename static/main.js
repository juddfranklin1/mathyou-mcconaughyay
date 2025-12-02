document.addEventListener('DOMContentLoaded', function() {
    // Initialize KaTeX Auto-render
    if (window.renderMathInElement) {
        renderMathInElement(document.body, {
            delimiters: [
                {left: "$", right: "$", display: false},
                {left: "$$", right: "$$", display: true}
            ]
        });
    }

    const select = document.getElementById('concept-select');
    if (!select) {
        return; // Do nothing if there's no select dropdown on the page
    }

    const formulaDiv = document.getElementById('formula');
    const explanationDiv = document.getElementById('explanation');
    const formulaLabel = document.getElementById('formula-label');
    const conceptTypeHeading = document.querySelector('h1[data-concept-type]');
    
    if (!conceptTypeHeading) {
        return; // Do nothing if the concept type isn't specified
    }
    const conceptType = conceptTypeHeading.dataset.conceptType;

    select.addEventListener('change', function() {
        const concept = select.value;
        if (!concept) return;

        let endpoint = '';
        if (conceptType === 'linear-algebra') {
            endpoint = `/concept?name=${encodeURIComponent(concept)}`;
        } else if (conceptType === 'calculus') {
            endpoint = `/calculus_concept?name=${encodeURIComponent(concept)}`;
        }

        if (!endpoint) return;

        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                if (data.formula) {
                    formulaLabel.style.display = '';
                    formulaDiv.innerHTML = '';
                    if (window.katex) {
                        try {
                            katex.render(data.formula, formulaDiv, {displayMode: true});
                        } catch (e) {
                            formulaDiv.textContent = data.formula;
                        }
                    } else {
                        formulaDiv.innerHTML = `<span class='math'>${data.formula}</span>`;
                    }
                } else {
                    formulaLabel.style.display = 'none';
                    formulaDiv.innerHTML = '';
                }

                if (data.explanation) {
                    explanationDiv.innerHTML = '';
                    if (window.renderMathInElement) {
                        explanationDiv.innerHTML = data.explanation;
                        renderMathInElement(explanationDiv, {delimiters: [
                            {left: "$", right: "$", display: false},
                            {left: "$$", right: "$$", display: true}
                        ]});
                    } else {
                        explanationDiv.textContent = data.explanation;
                    }
                } else {
                    explanationDiv.innerHTML = '';
                }
            });
    });
});
