"""Data for integration concepts."""

INTEGRATION_CONCEPTS = {
    "Definite Integral": {
        "formula": r"\int_a^b f(x)dx = \lim_{n \to \infty} \sum_{i=1}^n f(x_i)\Delta x",
        "explanation": "The definite integral $\int_a^b f(x)dx$ represents the signed area between the function $f(x)$ and the x-axis from $a$ to $b$. The notation shows it's the limit of Riemann sums as we make the subdivisions infinitely small ($\\Delta x \\to 0$). This fundamental concept connects areas, accumulation, and the antiderivative."
    },
    "Indefinite Integral": {
        "formula": r"\int f(x)dx = F(x) + C",
        "explanation": "The indefinite integral or antiderivative $\int f(x)dx$ gives us a family of functions $F(x) + C$ whose derivative is $f(x)$. The mysterious $C$ is the constant of integration, representing that if $F(x)$ is an antiderivative, then $F(x) + C$ is also an antiderivative for any constant $C$."
    },
    "Integration by Parts": {
        "formula": r"\int u\,dv = uv - \int v\,du",
        "explanation": "Integration by parts is based on the product rule of differentiation. When integrating a product, we can choose $u$ and $dv$ strategically. The notation $\\int u\\,dv$ represents finding an antiderivative where one factor ($u$) is treated as a coefficient of the differential of the other factor ($dv$)."
    },
    "U-Substitution": {
        "formula": r"\int f(g(x))g'(x)dx = \int f(u)du \quad \text{where } u = g(x)",
        "explanation": "U-substitution is the reverse of the chain rule. When we spot a function $g(x)$ and its derivative $g'(x)$, we can substitute $u = g(x)$. The notation shows how we transform a complex integral into a simpler one by making a clever substitution."
    },
    "Partial Fractions": {
        "formula": r"\frac{P(x)}{Q(x)} = \frac{A}{x-a} + \frac{B}{x-b} + \cdots",
        "explanation": "Partial fraction decomposition breaks a complex rational function into simpler fractions that we can integrate. The notation shows how we split a fraction into a sum of simpler terms. Each term $\\frac{A}{x-a}$ has an easy antiderivative: $A\\ln|x-a|$."
    }
}