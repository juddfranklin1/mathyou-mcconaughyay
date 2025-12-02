"""Data for differential calculus concepts."""

DIFFERENTIAL_CALCULUS_CONCEPTS = {
    "Derivative": {
        "formula": r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
        "explanation": "Notation: $f'(x)$ or $\\frac{dy}{dx}$ denotes the derivative of the function $f(x)$. This notation represents the instantaneous rate of change of the function, or the slope of the tangent line at point $x$. It's the core concept of differential calculus. The limit notation $\\lim_{h \\to 0}$ indicates we're looking at changes as they become infinitely small."
    },
    "Power Rule": {
        "formula": r"\frac{d}{dx}(x^n) = nx^{n-1}",
        "explanation": "This rule shows how to find the derivative of a variable raised to a power. The notation $\\frac{d}{dx}$ is an operator that means 'take the derivative with respect to $x$'. When applied to $x^n$, it gives us $nx^{n-1}$, where the power decreases by 1 and we multiply by the original power. It's a shortcut that saves us from using the limit definition every time."
    },
    "Product Rule": {
        "formula": r"\frac{d}{dx}(uv) = u\frac{dv}{dx} + v\frac{du}{dx}",
        "explanation": "Used for differentiating the product of two functions, $u$ and $v$. The expression $\\frac{d}{dx}(uv)$ represents the derivative of their product. The result, $u\\frac{dv}{dx} + v\\frac{du}{dx}$, shows we can't just multiply the derivatives - we need both functions and their derivatives. It's a reminder that calculus has its own rules for multiplication!"
    },
    "Quotient Rule": {
        "formula": r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v\frac{du}{dx} - u\frac{dv}{dx}}{v^2}",
        "explanation": "For differentiating the ratio $\\frac{u}{v}$ of two functions. The result $\\frac{v\\frac{du}{dx} - u\\frac{dv}{dx}}{v^2}$ follows the mnemonic 'low d-high minus high d-low, square the bottom and away we go!' The denominator $v^2$ shows why we need the quotient rule - division in calculus requires special care."
    },
    "Chain Rule": {
        "formula": r"\frac{d}{dx}f(g(x)) = f'(g(x))g'(x)",
        "explanation": "Used for differentiating composite functions (a function inside another function). Given $y = f(g(x))$, the chain rule states $\\frac{dy}{dx} = f'(g(x))g'(x)$. It's like a Russian doll of derivatives: $f'(g(x))$ is the derivative of the outer function evaluated at $g(x)$, and $g'(x)$ is the derivative of the inner function."
    }
}