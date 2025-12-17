"""Data for trigonometry concepts."""

TRIGONOMETRY_CONCEPTS = {
    "Basic Ratios": {
        "formula": r"\sin \theta = \frac{\text{opposite}}{\text{hypotenuse}}, \cos \theta = \frac{\text{adjacent}}{\text{hypotenuse}}, \tan \theta = \frac{\text{opposite}}{\text{adjacent}}",
        "explanation": "The fundamental ratios in trigonometry relate the sides of a right triangle. Here, $\\sin \\theta$ (sine), $\\cos \\theta$ (cosine), and $\\tan \\theta$ (tangent) are the building blocks of trigonometry. Notice how tangent is just $\\frac{\\sin \\theta}{\\cos \\theta}$ - it's like these ratios are one big happy family!"
    },
    "Reciprocal Functions": {
        "formula": r"\csc \theta = \frac{1}{\sin \theta}, \sec \theta = \frac{1}{\cos \theta}, \cot \theta = \frac{1}{\tan \theta}",
        "explanation": "Meet the reciprocal functions! $\\csc \\theta$ (cosecant), $\\sec \\theta$ (secant), and $\\cot \\theta$ (cotangent) are just flipped versions of our basic ratios. They're like the evil twins, but they're actually quite useful when we need to simplify complex expressions."
    },
    "Pythagorean Identities": {
        "formula": r"\sin^2 \theta + \cos^2 \theta = 1, \tan^2 \theta + 1 = \sec^2 \theta, \cot^2 \theta + 1 = \csc^2 \theta",
        "core_idea": "The Pythagorean Identity, $\\sin^2\\theta + \cos^2\\theta = 1$, is the most important equation in all of trigonometry. It comes directly from the unit circle and the Pythagorean Theorem ($a^2+b^2=c^2$). On the unit circle, the coordinates are $(\\cos\\theta, \\sin\\theta)$ and the radius (hypotenuse) is 1. So, $x^2+y^2=r^2$ becomes $\\cos^2\\theta + \\sin^2\\theta = 1^2$. It means that for *any* angle, if you know its sine, you can find its cosine, and vice-versa.",
        "real_world_application": "In robotics, if a robotic arm of length 1 is controlled by an angle $\\theta$, its endpoint has coordinates $(\\cos\\theta, \\sin\\theta)$. This identity provides a constant check on the validity of the arm's position. It's also fundamental in computer graphics for creating realistic lighting and reflection models, ensuring that calculations involving angles and distances remain consistent.",
        "mathematical_demonstration": "Suppose you know that for a certain angle $\theta$ in the first quadrant, $\\sin\\theta = \\frac{3}{5}$. What is $\\cos\\theta$?<ol><li>Start with the identity: $\\sin^2\\theta + \\cos^2\\theta = 1$.</li><li>Plug in the known value: $(\\frac{3}{5})^2 + \\cos^2\\theta = 1$.</li><li>Simplify: $\\frac{9}{25} + \\cos^2\\theta = 1$.</li><li>Solve for $\\cos^2\\theta$: $\\cos^2\\theta = 1 - \\frac{9}{25} = \\frac{16}{25}$.</li><li>Take the square root: $\\cos\\theta = \\pm\\sqrt{\\frac{16}{25}} = \\pm\\frac{4}{5}$.<br>Since we are in the first quadrant, cosine is positive, so $\\cos\\theta = \\frac{4}{5}$.</li></ol> You found one trig value from another without even knowing the angle!",
        "explanation": "The Pythagorean Identity is a fundamental relation in trigonometry that states that for any angle, the square of the sine plus the square of the cosine is 1."
    },
    "Double Angle Formulas": {
        "formula": r"\sin(2\theta) = 2\sin \theta \cos \theta, \cos(2\theta) = \cos^2 \theta - \sin^2 \theta = 2\cos^2 \theta - 1",
        "explanation": "Want to know what happens when you double an angle? These formulas tell you! $\\sin(2\\theta)$ is like a dance between sine and cosine, while $\\cos(2\\theta)$ can be written two ways (neat, right?). These formulas are super helpful when you need to convert powers to multiple angles or vice versa."
    },
    "Addition Formulas": {
        "formula": r"\sin(A + B) = \sin A \cos B + \cos A \sin B, \cos(A + B) = \cos A \cos B - \sin A \sin B",
        "explanation": "These are the Swiss Army knives of trigonometry! $\\sin(A + B)$ and $\\cos(A + B)$ show us how trig functions combine. It's like a mathematical recipe: mix some sines and cosines, and voilà! You can find the trig values of combined angles without measuring them directly."
    },
    "Law of Sines": {
        "formula": r"\frac{\sin A}{a} = \frac{\sin B}{b} = \frac{\sin C}{c} = \frac{1}{2R}",
        "core_idea": "The Law of Sines is a powerful tool for solving triangles that are *not* right-angled. It creates a beautiful ratio between the sides of a triangle and the sines of their opposite angles: $\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}$. If you know two angles and one side (AAS or ASA), or two sides and a non-included angle (SSA), you can use this law to find all the missing parts of the triangle.",
        "real_world_application": "Surveyors use this all the time! Imagine you need to find the distance to a faraway mountain peak. You can't measure it directly. So, you create a baseline between two points (A and B) and measure the distance. From each point, you measure the angle to the peak (C). Now you have a triangle where you know one side (the baseline) and two angles. The Law of Sines lets you calculate the other two sides—the distances to the peak!",
        "mathematical_demonstration": "Consider a triangle with angle $A=30^\circ$, angle $B=70^\circ$, and side $a=8$. Let's find the length of side $b$.<br>1. First, find angle C: $C = 180^\circ - 30^\circ - 70^\circ = 80^\circ$.<br>2. Set up the Law of Sines: $\frac{a}{\sin A} = \frac{b}{\sin B}$.<br>3. Plug in the known values: $\frac{8}{\sin 30^\circ} = \frac{b}{\sin 70^\circ}$.<br>4. Solve for b: $b = \frac{8 \cdot \sin 70^\circ}{\sin 30^\circ}$.<br>5. Calculate: $\sin 70^\circ \approx 0.940$ and $\sin 30^\circ = 0.5$. So, $b \approx \frac{8 \cdot 0.940}{0.5} = 15.04$. You've just found the length of a side without ever measuring it directly!",
        "explanation": "The Law of Sines relates the lengths of the sides of a triangle to the sines of its angles. The Law of Sines is like the scales of justice for triangles! Here, $a$, $b$, and $c$ are side lengths, $A$, $B$, and $C$ are angles, and $R$ is the radius of the circumscribed circle. This law works for ANY triangle, not just right ones. It's telling us there's a beautiful proportion between sides and sines."
    },
    "Law of Cosines": {
        "formula": r"c^2 = a^2 + b^2 - 2ab\cos C",
        "explanation": "This is the Pythagorean theorem's cooler cousin! When your triangle isn't right, this law saves the day. It relates the length of a side ($c$) to the other two sides ($a$ and $b$) and the angle between them ($C$). When $C = 90°$, $\\cos C = 0$, and boom - you're back to $a^2 + b^2 = c^2$!"
    },
    "Period and Amplitude": {
        "formula": r"y = A\sin(Bx + C) + D",
        "explanation": "The anatomy of a sine wave! Here, $A$ controls the amplitude (half the height from peak to trough), $B$ affects the period ($\\frac{2\\pi}{B}$ gives the period), $C$ shifts the wave horizontally (phase shift), and $D$ moves the whole wave up or down. It's like having a control panel for your wave function!"
    }
}