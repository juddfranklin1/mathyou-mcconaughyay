from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Subject, Concept, Question, UserResponse
import uuid

app = create_app()

def seed_questions():
    with app.app_context():
        print("Starting question seeding...")
        
        # Dictionary of specific questions for known concepts
        # Key: (subject_slug, concept_slug)
        specific_questions = {
            # --- Differential Calculus ---
            ('calculus', 'derivative'): [
                {
                'problem_text': 'Find the derivative of $f(x) = 3x^2 - 4x + 5$.',
                'difficulty': 'Easy',
                'explanation': 'Using the Power Rule: $\\frac{d}{dx}(3x^2) = 6x$, $\\frac{d}{dx}(-4x) = -4$, $\\frac{d}{dx}(5) = 0$. So $f\'(x) = 6x - 4$.',
                'data': {'type': 'multiple_choice', 'choices': ['$6x - 4$', '$3x - 4$', '$6x$', '$6x^2 - 4$'], 'answer': 0}
                },
                {
                'problem_text': 'Find the derivative of $f(x) = \\sqrt{x} + \\frac{1}{x}$.',
                'difficulty': 'Medium',
                'explanation': 'Rewrite as $x^{1/2} + x^{-1}$. Apply power rule: $\\frac{1}{2}x^{-1/2} - 1x^{-2} = \\frac{1}{2\\sqrt{x}} - \\frac{1}{x^2}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{1}{2\\sqrt{x}} - \\frac{1}{x^2}$', '$\\frac{1}{2\\sqrt{x}} + \\frac{1}{x^2}$', '$\\sqrt{x} - x^2$', '$\\frac{1}{2}x - \\frac{1}{x}$'], 'answer': 0}
                },
                {
                'problem_text': 'Find the equation of the tangent line to $y = x^3 - 3x$ at $x=2$.',
                'difficulty': 'Hard',
                'explanation': '$y(2) = 8-6=2$. $y\' = 3x^2 - 3$. $y\'(2) = 12-3=9$. Line: $y - 2 = 9(x - 2) \\Rightarrow y = 9x - 16$.',
                'data': {'type': 'multiple_choice', 'choices': ['$y = 9x - 16$', '$y = 9x - 2$', '$y = 3x - 4$', '$y = 9x + 16$'], 'answer': 0}
                }
            ],
            ('calculus', 'power-rule'): [
                {
                'problem_text': 'Calculate $\\frac{d}{dx}(x^8)$.',
                'difficulty': 'Easy',
                'explanation': 'Apply the Power Rule $nx^{n-1}$. Here $n=8$, so we get $8x^{8-1} = 8x^7$.',
                'data': {'type': 'multiple_choice', 'choices': ['$8x^7$', '$7x^8$', '$8x^8$', '$x^7$'], 'answer': 0}
                },
                {
                'problem_text': 'Differentiate $y = 5x^{100} - 3x^{10}$.',
                'difficulty': 'Medium',
                'explanation': '$5(100x^{99}) - 3(10x^9) = 500x^{99} - 30x^9$.',
                'data': {'type': 'multiple_choice', 'choices': ['$500x^{99} - 30x^9$', '$100x^{99} - 10x^9$', '$500x^{100} - 30x^{10}$', '$5x^{99} - 3x^9$'], 'answer': 0}
                },
                {
                'problem_text': 'Find $\\frac{d}{dx}(\\frac{4}{\\sqrt[3]{x}})$.',
                'difficulty': 'Hard',
                'explanation': 'Rewrite as $4x^{-1/3}$. Derivative is $4(-\\frac{1}{3})x^{-4/3} = -\\frac{4}{3}x^{-4/3} = -\\frac{4}{3x^{4/3}}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$-\\frac{4}{3}x^{-4/3}$', '$\\frac{4}{3}x^{-2/3}$', '$4x^{2/3}$', '$-12x^{-4/3}$'], 'answer': 0}
                }
            ],
            ('calculus', 'product-rule'): [
                {
                'problem_text': 'Find the derivative of $y = x e^x$.',
                'difficulty': 'Easy',
                'explanation': '$u=x, v=e^x$. $u\'=1, v\'=e^x$. $y\' = 1\\cdot e^x + x\\cdot e^x = e^x(1+x)$.',
                'data': {'type': 'multiple_choice', 'choices': ['$e^x(1+x)$', '$e^x$', '$xe^x$', '$e^x + 1$'], 'answer': 0}
                },
                {
                'problem_text': 'Find the derivative of $y = x^2 \\sin(x)$.',
                'difficulty': 'Medium',
                'explanation': 'Product Rule: $u\'v + uv\'$. Let $u=x^2, v=\\sin(x)$. $u\'=2x, v\'=\\cos(x)$. Result: $2x\\sin(x) + x^2\\cos(x)$.',
                'data': {'type': 'multiple_choice', 'choices': ['$2x\\sin(x) + x^2\\cos(x)$', '$2x\\cos(x)$', '$x^2\\cos(x)$', '$2x\\sin(x)$'], 'answer': 0}
                },
                {
                'problem_text': 'Differentiate $f(x) = (3x+1)(2x-5)$ using the product rule.',
                'difficulty': 'Hard',
                'explanation': '$u=3x+1, v=2x-5$. $u\'=3, v\'=2$. $3(2x-5) + 2(3x+1) = 6x-15 + 6x+2 = 12x-13$.',
                'data': {'type': 'multiple_choice', 'choices': ['$12x-13$', '$6x-15$', '$12x+13$', '$6x^2-13x-5$'], 'answer': 0}
                }
            ],
            ('calculus', 'quotient-rule'): [
                {
                'problem_text': 'Find $y\'$ for $y = \\frac{1}{x}$.',
                'difficulty': 'Easy',
                'explanation': 'Using quotient rule with $u=1, v=x$ (or power rule $x^{-1}$). $\\frac{0\\cdot x - 1\\cdot 1}{x^2} = -\\frac{1}{x^2}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$-\\frac{1}{x^2}$', '$\\frac{1}{x^2}$', '$\\ln(x)$', '$0$'], 'answer': 0}
                },
                {
                'problem_text': 'Find $f\'(x)$ for $f(x) = \\frac{\\sin(x)}{x}$.',
                'difficulty': 'Medium',
                'explanation': 'Quotient Rule: $\\frac{u\'v - uv\'}{v^2}$. $u=\\sin(x), v=x$. $u\'=\\cos(x), v\'=1$. Result: $\\frac{x\\cos(x) - \\sin(x)}{x^2}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{x\\cos(x) - \\sin(x)}{x^2}$', '$\\frac{\\cos(x)}{1}$', '$\\frac{\\sin(x) - x\\cos(x)}{x^2}$', '$\\cos(x)$'], 'answer': 0}
                },
                {
                'problem_text': 'Differentiate $y = \\frac{x^2 + 1}{x^2 - 1}$.',
                'difficulty': 'Hard',
                'explanation': '$u=x^2+1, v=x^2-1$. $u\'=2x, v\'=2x$. $\\frac{2x(x^2-1) - 2x(x^2+1)}{(x^2-1)^2} = \\frac{2x^3-2x - 2x^3-2x}{(x^2-1)^2} = \\frac{-4x}{(x^2-1)^2}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{-4x}{(x^2-1)^2}$', '$\\frac{4x}{(x^2-1)^2}$', '$\\frac{2x}{x^2-1}$', '$0$'], 'answer': 0}
                }
            ],
            ('calculus', 'chain-rule'): [
                {
                'problem_text': 'Find the derivative of $y = (2x+1)^3$.',
                'difficulty': 'Easy',
                'explanation': '$3(2x+1)^2 \\cdot 2 = 6(2x+1)^2$.',
                'data': {'type': 'multiple_choice', 'choices': ['$6(2x+1)^2$', '$3(2x+1)^2$', '$6(2x+1)$', '$2(2x+1)^3$'], 'answer': 0}
                },
                {
                'problem_text': 'Find the derivative of f(x) = (3x² + 2)⁵ using the Chain Rule.',
                'difficulty': 'Medium',
                'explanation': 'Let u = 3x² + 2, then y = u⁵. dy/dx = dy/du * du/dx = 5u⁴ * 6x = 30x(3x² + 2)⁴.',
                'data': {'type': 'multiple_choice', 'choices': ['30x(3x² + 2)⁴', '5(3x² + 2)⁴', '15x(3x² + 2)⁴', '(3x² + 2)⁴'], 'answer': 0}
                },
                {
                'problem_text': 'Differentiate $y = \\sin(\\cos(x))$.',
                'difficulty': 'Hard',
                'explanation': 'Outer is $\\sin$, inner is $\\cos$. $\\cos(\\cos(x)) \\cdot (-\\sin(x)) = -\\sin(x)\\cos(\\cos(x))$.',
                'data': {'type': 'multiple_choice', 'choices': ['$-\\sin(x)\\cos(\\cos(x))$', '$\\cos(\\cos(x))$', '$\\cos(\\sin(x))$', '$\\sin(\\sin(x))$'], 'answer': 0}
                }
            ],

            # --- Integration ---
            ('integration', 'definite-integral'): [
                {
                'problem_text': 'Evaluate $\\int_0^1 2x dx$.',
                'difficulty': 'Easy',
                'explanation': 'Antiderivative is $x^2$. $1^2 - 0^2 = 1$.',
                'data': {'type': 'numerical', 'answer': 1}
                },
                {
                'problem_text': 'Evaluate $\\int_0^2 3x^2 dx$.',
                'difficulty': 'Medium',
                'explanation': 'Antiderivative of $3x^2$ is $x^3$. Evaluate at bounds: $2^3 - 0^3 = 8 - 0 = 8$.',
                'data': {'type': 'numerical', 'answer': 8}
                },
                {
                'problem_text': 'Evaluate $\\int_0^\\pi \\sin(x) dx$.',
                'difficulty': 'Hard',
                'explanation': 'Antiderivative is $-\\cos(x)$. $-\\cos(\\pi) - (-\\cos(0)) = -(-1) - (-1) = 1 + 1 = 2$.',
                'data': {'type': 'numerical', 'answer': 2}
                }
            ],
            ('integration', 'indefinite-integral'): [
                {
                'problem_text': 'Find $\\int 5 dx$.',
                'difficulty': 'Easy',
                'explanation': '$5x + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$5x + C$', '$5 + C$', '$0$', '$x + C$'], 'answer': 0}
                },
                {
                'problem_text': 'Find the indefinite integral of $f(x) = 4x^3$.',
                'difficulty': 'Medium',
                'explanation': 'Power rule for integration: add 1 to exponent, divide by new exponent. $\\frac{4x^4}{4} + C = x^4 + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$x^4 + C$', '$4x^4 + C$', '$12x^2 + C$', '$x^3 + C$'], 'answer': 0}
                },
                {
                'problem_text': 'Find $\\int \\frac{1}{x} dx$.',
                'difficulty': 'Hard',
                'explanation': 'The antiderivative of $1/x$ is $\\ln|x| + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\ln|x| + C$', '$-x^{-2} + C$', '$e^x + C$', '$1$'], 'answer': 0}
                }
            ],
            ('integration', 'integration-by-parts'): [
                {
                'problem_text': 'To integrate $\\int x \\cos(x) dx$, what should you choose for $u$?',
                'difficulty': 'Easy',
                'explanation': 'Choose $u=x$ so that $du=dx$ (simpler). If $u=\\cos(x)$, $du$ is more complex.',
                'data': {'type': 'multiple_choice', 'choices': ['$x$', '$\\cos(x)$', '$dx$', '$x\\cos(x)$'], 'answer': 0}
                },
                {
                'problem_text': 'Evaluate $\\int x e^x dx$.',
                'difficulty': 'Medium',
                'explanation': 'Use $\\int u dv = uv - \\int v du$. Let $u=x, dv=e^x dx$. Then $du=dx, v=e^x$. Result: $xe^x - \\int e^x dx = xe^x - e^x + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$xe^x - e^x + C$', '$xe^x + e^x + C$', '$e^x + C$', '$\\frac{x^2}{2}e^x + C$'], 'answer': 0}
                },
                {
                'problem_text': 'Evaluate $\\int \\ln(x) dx$.',
                'difficulty': 'Hard',
                'explanation': 'Use parts with $u=\\ln(x), dv=dx$. $du=1/x dx, v=x$. $x\\ln(x) - \\int x(1/x) dx = x\\ln(x) - x + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$x\\ln(x) - x + C$', '$\\frac{1}{x} + C$', '$\\ln(x) + C$', '$x\\ln(x) + C$'], 'answer': 0}
                }
            ],
            ('integration', 'u-substitution'): [
                {
                'problem_text': 'Evaluate $\\int (x+1)^5 dx$.',
                'difficulty': 'Easy',
                'explanation': 'Let $u=x+1, du=dx$. $\\int u^5 du = \\frac{1}{6}u^6 = \\frac{1}{6}(x+1)^6 + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{1}{6}(x+1)^6 + C$', '$5(x+1)^4 + C$', '$(x+1)^6 + C$', '$\\frac{1}{5}(x+1)^5 + C$'], 'answer': 0}
                },
                {
                'problem_text': 'Evaluate $\\int 2x \\cos(x^2) dx$.',
                'difficulty': 'Medium',
                'explanation': 'Let $u = x^2$, then $du = 2x dx$. Integral becomes $\\int \\cos(u) du = \\sin(u) + C = \\sin(x^2) + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\sin(x^2) + C$', '$\\cos(x^2) + C$', '$2\\sin(x^2) + C$', '$\\sin(2x) + C$'], 'answer': 0}
                },
                {
                'problem_text': 'Evaluate $\\int \\frac{e^{\\sqrt{x}}}{\\sqrt{x}} dx$.',
                'difficulty': 'Hard',
                'explanation': '$u=\\sqrt{x}, du = \\frac{1}{2\\sqrt{x}}dx \\Rightarrow 2du = \\frac{1}{\\sqrt{x}}dx$. $\\int 2e^u du = 2e^u = 2e^{\\sqrt{x}} + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$2e^{\\sqrt{x}} + C$', '$e^{\\sqrt{x}} + C$', '$\\frac{1}{2}e^{\\sqrt{x}} + C$', '$e^x + C$'], 'answer': 0}
                }
            ],
            ('integration', 'partial-fractions'): [
                {
                'problem_text': 'Decompose $\\frac{2}{x^2-1}$.',
                'difficulty': 'Easy',
                'explanation': '$\\frac{2}{(x-1)(x+1)} = \\frac{1}{x-1} - \\frac{1}{x+1}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{1}{x-1} - \\frac{1}{x+1}$', '$\\frac{1}{x-1} + \\frac{1}{x+1}$', '$\\frac{2}{x-1}$', '$\\frac{2}{x+1}$'], 'answer': 0}
                },
                {
                'problem_text': 'Which form is correct for the partial fraction decomposition of $\\frac{1}{x(x+1)}$?',
                'difficulty': 'Medium',
                'explanation': 'Since factors are linear distinct, form is $\\frac{A}{x} + \\frac{B}{x+1}$. Solving gives $A=1, B=-1$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{A}{x} + \\frac{B}{x+1}$', '$\\frac{A}{x} + \\frac{Bx+C}{x+1}$', '$\\frac{A}{x^2} + \\frac{B}{x+1}$', '$\\frac{A}{x(x+1)}$'], 'answer': 0}
                },
                {
                'problem_text': 'Integrate $\\int \\frac{1}{x^2+x} dx$.',
                'difficulty': 'Hard',
                'explanation': '$\\frac{1}{x(x+1)} = \\frac{1}{x} - \\frac{1}{x+1}$. Integral is $\\ln|x| - \\ln|x+1| + C = \\ln|\\frac{x}{x+1}| + C$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\ln|\\frac{x}{x+1}| + C$', '$\\ln|x(x+1)| + C$', '$\\ln|x| + \\ln|x+1| + C$', '$\\frac{1}{x} + C$'], 'answer': 0}
                }
            ],

            # --- Trigonometry ---
            ('trigonometry', 'basic-ratios'): [
                {
                'problem_text': 'In a right triangle, if the opposite side is 3 and the hypotenuse is 5, what is $\\sin(\\theta)$?',
                'difficulty': 'Easy',
                'explanation': '$\\sin(\\theta) = \\frac{\\text{opposite}}{\\text{hypotenuse}} = \\frac{3}{5} = 0.6$.',
                'data': {'type': 'numerical', 'answer': 0.6}
                },
                {
                'problem_text': 'If $\\cos(\\theta) = 0.8$, what is $\\sin(\\theta)$? (Assume first quadrant)',
                'difficulty': 'Medium',
                'explanation': '$0.6^2 + 0.8^2 = 0.36 + 0.64 = 1$. So $\\sin(\\theta) = 0.6$.',
                'data': {'type': 'numerical', 'answer': 0.6}
                },
                {
                'problem_text': 'If $\\tan(\\theta) = 1$, what is $\\theta$ in degrees?',
                'difficulty': 'Hard',
                'explanation': '$\\tan(45^\\circ) = 1$.',
                'data': {'type': 'numerical', 'answer': 45}
                }
            ],
            ('trigonometry', 'reciprocal-functions'): [
                {
                'problem_text': 'If $\\sin(\\theta) = \\frac{1}{2}$, what is $\\csc(\\theta)$?',
                'difficulty': 'Easy',
                'explanation': '$\\csc(\\theta) = \\frac{1}{\\sin(\\theta)}$. So $\\csc(\\theta) = \\frac{1}{1/2} = 2$.',
                'data': {'type': 'numerical', 'answer': 2}
                },
                {
                'problem_text': 'Simplify $\\tan(\\theta) \\cdot \\cot(\\theta)$.',
                'difficulty': 'Medium',
                'explanation': '$\\tan(\\theta) \\cdot \\frac{1}{\\tan(\\theta)} = 1$.',
                'data': {'type': 'numerical', 'answer': 1}
                },
                {
                'problem_text': 'Express $\\sec^2(\\theta)$ in terms of $\\tan(\\theta)$.',
                'difficulty': 'Hard',
                'explanation': 'Identity: $\\sec^2(\\theta) = 1 + \\tan^2(\\theta)$.',
                'data': {'type': 'multiple_choice', 'choices': ['$1 + \\tan^2(\\theta)$', '$1 - \\tan^2(\\theta)$', '$\\tan^2(\\theta) - 1$', '$1$'], 'answer': 0}
                }
            ],
            ('trigonometry', 'pythagorean-identities'): [
                {
                'problem_text': 'Simplify the expression $1 - \\sin^2(\\theta)$.',
                'difficulty': 'Easy',
                'explanation': 'From $\\sin^2(\\theta) + \\cos^2(\\theta) = 1$, we have $\\cos^2(\\theta) = 1 - \\sin^2(\\theta)$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\cos^2(\\theta)$', '$\\sin^2(\\theta)$', '$\\tan^2(\\theta)$', '$1$'], 'answer': 0}
                },
                {
                'problem_text': 'Simplify $\\frac{\\sin^2(\\theta) + \\cos^2(\\theta)}{\\cos(\\theta)}$.',
                'difficulty': 'Medium',
                'explanation': 'Numerator is 1. $\\frac{1}{\\cos(\\theta)} = \\sec(\\theta)$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\sec(\\theta)$', '$\\cos(\\theta)$', '$\\sin(\\theta)$', '$1$'], 'answer': 0}
                },
                {
                'problem_text': 'If $\\sin(\\theta) = 0.6$, find $\\cos(\\theta)$ (Quadrant I).',
                'difficulty': 'Hard',
                'explanation': '$\\cos(\\theta) = \\sqrt{1 - 0.6^2} = \\sqrt{1 - 0.36} = \\sqrt{0.64} = 0.8$.',
                'data': {'type': 'numerical', 'answer': 0.8}
                }
            ],
            ('trigonometry', 'double-angle-formulas'): [
                {
                'problem_text': 'Which of the following is equivalent to $\\sin(2\\theta)$?',
                'difficulty': 'Easy',
                'explanation': 'The double angle identity for sine is $\\sin(2\\theta) = 2\\sin(\\theta)\\cos(\\theta)$.',
                'data': {'type': 'multiple_choice', 'choices': ['$2\\sin(\\theta)\\cos(\\theta)$', '$\\cos^2(\\theta) - \\sin^2(\\theta)$', '$2\\sin(\\theta)$', '$\\sin(\\theta)\\cos(\\theta)$'], 'answer': 0}
                },
                {
                'problem_text': 'If $\\sin(\\theta) = 3/5$ and $\\cos(\\theta) = 4/5$, find $\\sin(2\\theta)$.',
                'difficulty': 'Medium',
                'explanation': '$2(3/5)(4/5) = 24/25 = 0.96$.',
                'data': {'type': 'numerical', 'answer': 0.96}
                },
                {
                'problem_text': 'Solve $\\cos(2\\theta) = \\cos^2(\\theta) - \\sin^2(\\theta)$ for $\\theta=0$.',
                'difficulty': 'Hard',
                'explanation': '$\\cos(0) = 1 - 0 = 1$. Correct.',
                'data': {'type': 'numerical', 'answer': 1}
                }
            ],
            ('trigonometry', 'addition-formulas'): [
                {
                'problem_text': 'Expand $\\sin(A+B)$.',
                'difficulty': 'Easy',
                'explanation': '$\\sin A \\cos B + \\cos A \\sin B$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\sin A \\cos B + \\cos A \\sin B$', '$\\sin A \\cos B - \\cos A \\sin B$', '$\\cos A \\cos B - \\sin A \\sin B$', '$\\sin A + \\sin B$'], 'answer': 0}
                },
                {
                'problem_text': 'Use the addition formula to find $\\cos(90^\\circ - \\theta)$.',
                'difficulty': 'Medium',
                'explanation': '$\\cos(A-B) = \\cos A \\cos B + \\sin A \\sin B$. $\\cos(90)\\cos(\\theta) + \\sin(90)\\sin(\\theta) = 0\\cdot\\cos(\\theta) + 1\\cdot\\sin(\\theta) = \\sin(\\theta)$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\sin(\\theta)$', '$\\cos(\\theta)$', '$-\\sin(\\theta)$', '$-\\cos(\\theta)$'], 'answer': 0}
                },
                {
                'problem_text': 'Find $\\sin(75^\\circ)$ using $30^\\circ + 45^\\circ$.',
                'difficulty': 'Hard',
                'explanation': '$\\sin(30)\\cos(45) + \\cos(30)\\sin(45) = \\frac{1}{2}\\frac{\\sqrt{2}}{2} + \\frac{\\sqrt{3}}{2}\\frac{\\sqrt{2}}{2} = \\frac{\\sqrt{2}+\\sqrt{6}}{4}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{\\sqrt{2}+\\sqrt{6}}{4}$', '$\\frac{\\sqrt{6}-\\sqrt{2}}{4}$', '$\\frac{1}{4}$', '$1$'], 'answer': 0}
                }
            ],
            ('trigonometry', 'law-of-sines'): [
                {
                'problem_text': 'State the Law of Sines.',
                'difficulty': 'Easy',
                'explanation': '$\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\frac{a}{\\sin A} = \\frac{b}{\\sin B}$', '$a^2 = b^2 + c^2$', '$\\frac{a}{\\cos A} = \\frac{b}{\\cos B}$', '$a \\sin A = b \\sin B$'], 'answer': 0}
                },
                {
                'problem_text': 'In triangle ABC, if $A=30^\\circ$, $a=10$, and $B=90^\\circ$, find side $b$.',
                'difficulty': 'Medium',
                'explanation': '$\\frac{a}{\\sin A} = \\frac{b}{\\sin B} \\Rightarrow \\frac{10}{\\sin 30} = \\frac{b}{\\sin 90} \\Rightarrow \\frac{10}{0.5} = \\frac{b}{1} \\Rightarrow b=20$.',
                'data': {'type': 'numerical', 'answer': 20}
                },
                {
                'problem_text': 'If $a=10, A=40^\\circ, B=60^\\circ$, find $b$.',
                'difficulty': 'Hard',
                'explanation': '$b = \\frac{a \\sin B}{\\sin A} = \\frac{10 \\sin 60}{\\sin 40} \\approx \\frac{10(0.866)}{0.643} \\approx 13.47$.',
                'data': {'type': 'numerical', 'answer': 13.47}
                }
            ],
            ('trigonometry', 'law-of-cosines'): [
                {
                'problem_text': 'In a triangle with sides $a=3, b=4$ and angle $C=90^\\circ$, find $c^2$ using Law of Cosines.',
                'difficulty': 'Easy',
                'explanation': '$c^2 = a^2 + b^2 - 2ab\\cos(C)$. Since $C=90^\\circ, \\cos(C)=0$. $c^2 = 3^2 + 4^2 = 9+16=25$.',
                'data': {'type': 'numerical', 'answer': 25}
                },
                {
                'problem_text': 'Find $c$ if $a=5, b=8, C=60^\\circ$.',
                'difficulty': 'Medium',
                'explanation': '$c^2 = 25 + 64 - 2(5)(8)(0.5) = 89 - 40 = 49$. $c=7$.',
                'data': {'type': 'numerical', 'answer': 7}
                },
                {
                'problem_text': 'Find angle $A$ if $a=5, b=5, c=5$.',
                'difficulty': 'Hard',
                'explanation': 'Equilateral triangle, so $60^\\circ$. Using formula: $25 = 25+25 - 50\\cos A \\Rightarrow -25 = -50\\cos A \\Rightarrow \\cos A = 0.5$.',
                'data': {'type': 'numerical', 'answer': 60}
                }
            ],
            ('trigonometry', 'period-and-amplitude'): [
                {
                'problem_text': 'What is the amplitude of $y = -5\\sin(3x)$?',
                'difficulty': 'Easy',
                'explanation': 'Amplitude is $|A|$. Here $A=-5$, so amplitude is $|-5| = 5$.',
                'data': {'type': 'numerical', 'answer': 5}
                },
                {
                'problem_text': 'What is the period of $y = \\sin(2x)$?',
                'difficulty': 'Medium',
                'explanation': 'Period is $2\\pi / B$. Here $B=2$, so $2\\pi/2 = \\pi$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\pi$', '$2\\pi$', '$\\pi/2$', '$4\\pi$'], 'answer': 0}
                },
                {
                'problem_text': 'Find the period of $y = 3\\tan(4x)$.',
                'difficulty': 'Hard',
                'explanation': 'Period of tan is $\\pi/B$. Here $\\pi/4$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\pi/4$', '$\\pi$', '$4\\pi$', '$\\pi/2$'], 'answer': 0}
                }
            ],

            # --- Linear Algebra (Missing from practice_problems.py) ---
            ('linear-algebra', 'eigenvalue'): [
                {
                'problem_text': 'Find the eigenvalues of the diagonal matrix $A = \\begin{bmatrix} 4 & 0 \\\\ 0 & 7 \\end{bmatrix}$.',
                'difficulty': 'Easy',
                'explanation': 'For a diagonal matrix, the eigenvalues are simply the diagonal entries. Here, $\\lambda_1 = 4, \\lambda_2 = 7$.',
                'data': {'type': 'multiple_choice', 'choices': ['4 and 7', '0 and 0', '11 and 0', '28 and 0'], 'answer': 0}
                },
                {
                'problem_text': 'If $\\lambda$ is an eigenvalue of $A$, what is an eigenvalue of $A^2$?',
                'difficulty': 'Medium',
                'explanation': '$A\\vec{x} = \\lambda\\vec{x} \\Rightarrow A^2\\vec{x} = A(\\lambda\\vec{x}) = \\lambda(A\\vec{x}) = \\lambda^2\\vec{x}$.',
                'data': {'type': 'multiple_choice', 'choices': ['$\\lambda^2$', '$\\lambda$', '$2\\lambda$', '$\\sqrt{\\lambda}$'], 'answer': 0}
                },
                {
                'problem_text': 'Find the eigenvalues of $\\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}$.',
                'difficulty': 'Hard',
                'explanation': 'Triangular matrix, eigenvalues are on diagonal. $\\lambda = 1$ (repeated).',
                'data': {'type': 'multiple_choice', 'choices': ['1', '0', '1 and 0', 'None'], 'answer': 0}
                }
            ]
        }
        
        concepts = Concept.query.all()
        count = 0
        
        for concept in concepts:
            subject = concept.subject
            key = (subject.slug, concept.slug)
            
            q_list = specific_questions.get(key)
            
            if q_list:
                # Remove existing questions for this concept to ensure we replace generic ones
                existing_questions = Question.query.filter_by(concept_id=concept.id).all()
                for q in existing_questions:
                    # Delete associated responses first to avoid IntegrityError
                    for response in q.responses:
                        db.session.delete(response)
                    db.session.delete(q)
            
                for q_data in q_list:
                    legacy_id = f"{concept.slug}_q_{uuid.uuid4().hex[:6]}"
                    question = Question(
                        legacy_id=legacy_id,
                        concept_id=concept.id,
                        problem_text=q_data['problem_text'],
                        difficulty=q_data['difficulty'],
                        explanation=q_data['explanation'],
                        data=q_data['data']
                    )
                    
                    db.session.add(question)
                    count += 1
                print(f"Added {len(q_list)} specific questions for {concept.name} ({subject.name})")
            
        db.session.commit()
        print(f"Successfully added {count} questions.")

if __name__ == '__main__':
    seed_questions()