"""Data for practice problems across different math domains."""

class QuestionType:
    NUMERICAL = "numerical"  # Direct numerical answer
    MULTIPLE_CHOICE = "multiple_choice"  # Multiple choice selection
    VECTOR = "vector"  # Vector/matrix entry with multiple components

LINEAR_ALGEBRA_PROBLEMS = {
    "Determinant": [
        {
            "id": "la_001",
            "problem": "Given a 2×2 matrix $A = \\begin{bmatrix} 2 & 1 \\\\ 3 & 4 \\end{bmatrix}$, calculate the determinant. Show your final answer as a single number.",
            "type": QuestionType.NUMERICAL,
            "answer": "5",
            "explanation": "For a 2×2 matrix [[a, b], [c, d]], the determinant is calculated as ad - bc. Here, det(A) = (2×4) - (1×3) = 8 - 3 = 5",
            "difficulty": "beginner"
        },
        {
            "id": "la_001b",
            "problem": "What happens to the determinant of a matrix when you multiply every element by 2?",
            "type": QuestionType.MULTIPLE_CHOICE,
            "choices": [
                "The determinant doubles",
                "The determinant multiplies by 4",
                "The determinant stays the same",
                "The determinant squares"
            ],
            "answer": 1,  # Index of correct answer
            "explanation": "When you multiply every element in an n×n matrix by k, the determinant is multiplied by k^n. For a 2×2 matrix, multiplying by 2 means the determinant multiplies by 2^2 = 4.",
            "difficulty": "intermediate"
        },
        {
            "id": "la_001c",
            "problem": "A rectangular room is being transformed by a linear transformation represented by the matrix $\\begin{bmatrix} 3 & 1 \\\\ 2 & 2 \\end{bmatrix}$. If the original room had an area of 100 square meters, what is the new area?",
            "type": QuestionType.NUMERICAL,
            "answer": "400",
            "explanation": "The determinant of the transformation matrix is (3×2) - (1×2) = 4. The new area is the original area multiplied by the absolute value of the determinant: 100 × |4| = 400 square meters.",
            "difficulty": "advanced"
        }
    ],
    "Vector": [
        {
            "id": "la_002a",
            "problem": "Calculate the magnitude of the vector $\\vec{v} = \\begin{bmatrix} 3 \\\\ 4 \\end{bmatrix}$",
            "type": QuestionType.NUMERICAL,
            "answer": "5",
            "explanation": "The magnitude of a 2D vector $\\begin{bmatrix} x \\\\ y \\end{bmatrix}$ is calculated as $\\sqrt{x^2 + y^2}$. Here, $\\sqrt{3^2 + 4^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5$",
            "difficulty": "beginner"
        },
        {
            "id": "la_002b",
            "problem": "A ship is sailing with a velocity of 3 knots east and 4 knots north. Which of these best describes its actual speed and direction?",
            "type": QuestionType.MULTIPLE_CHOICE,
            "choices": [
                "5 knots at 37° north of east",
                "7 knots at 45° north of east",
                "5 knots at 53° north of east",
                "7 knots at 53° north of east"
            ],
            "answer": 0,
            "explanation": "The ship's velocity forms a 3-4-5 right triangle. The speed (magnitude) is 5 knots. The angle is arctan(4/3) ≈ 53°, but measured from the vertical, so the angle from east is 37°.",
            "difficulty": "intermediate"
        },
        {
            "id": "la_002c",
            "problem": "An airplane is flying through a wind field. Its airspeed is $\\begin{bmatrix} 100 \\\\ 0 \\end{bmatrix}$ km/h (east), and the wind velocity is $\\begin{bmatrix} 30 \\\\ 40 \\end{bmatrix}$ km/h. Find the ground velocity vector of the airplane.",
            "type": QuestionType.VECTOR,
            "answer": "[130, 40]",
            "explanation": "Ground velocity is the vector sum of air velocity and wind velocity. Adding the vectors: $\\begin{bmatrix} 100 \\\\ 0 \\end{bmatrix} + \\begin{bmatrix} 30 \\\\ 40 \\end{bmatrix} = \\begin{bmatrix} 130 \\\\ 40 \\end{bmatrix}$",
            "difficulty": "advanced"
        }
    ],
    "Matrix Multiplication": [
        {
            "id": "la_003a",
            "problem": "Multiply matrices $A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 3 \\end{bmatrix}$ and $B = \\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}$. What is the first element of the resulting matrix?",
            "type": QuestionType.NUMERICAL,
            "answer": "4",
            "explanation": "When multiplying a 2×2 matrix by a 2×1 matrix, we get a 2×1 matrix. The first element is calculated as (2×1) + (1×2) = 2 + 2 = 4",
            "difficulty": "intermediate"
        },
        {
            "id": "la_003b",
            "problem": "A graphics program uses matrices to transform images. Which sequence of transformations would rotate an image 90° clockwise around the origin and then double its size?",
            "type": QuestionType.MULTIPLE_CHOICE,
            "choices": [
                "First rotate: $\\begin{bmatrix} 0 & 1 \\\\ -1 & 0 \\end{bmatrix}$, then scale: $\\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}$",
                "First scale: $\\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}$, then rotate: $\\begin{bmatrix} 0 & 1 \\\\ -1 & 0 \\end{bmatrix}$",
                "Use combined matrix: $\\begin{bmatrix} 0 & 2 \\\\ -2 & 0 \\end{bmatrix}$",
                "All of the above"
            ],
            "answer": 3,
            "explanation": "All three methods are equivalent! The combined matrix $\\begin{bmatrix} 0 & 2 \\\\ -2 & 0 \\end{bmatrix}$ is the result of multiplying the rotation and scaling matrices in either order (they commute in this case).",
            "difficulty": "advanced"
        },
        {
            "id": "la_003c",
            "problem": "A 3D animation system uses transformation matrices. A character starts at position $\\begin{bmatrix} 1 \\\\ 2 \\\\ 1 \\end{bmatrix}$ and undergoes two transformations: first $A = \\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 2 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$ then $B = \\begin{bmatrix} 2 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 2 \\end{bmatrix}$. What is the final z-coordinate?",
            "type": QuestionType.NUMERICAL,
            "answer": "2",
            "explanation": "We need to multiply B × A × position. First A transforms the position to $\\begin{bmatrix} 2 \\\\ 4 \\\\ 1 \\end{bmatrix}$, then B transforms it to $\\begin{bmatrix} 4 \\\\ 4 \\\\ 2 \\end{bmatrix}$. The z-coordinate is 2.",
            "difficulty": "advanced"
        }
    ],
    "Dot Product": [
        {
            "id": "la_004a",
            "problem": "Calculate the dot product of vectors $\\vec{a} = \\begin{bmatrix} 2 \\\\ 3 \\end{bmatrix}$ and $\\vec{b} = \\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix}$",
            "type": QuestionType.NUMERICAL,
            "answer": "-1",
            "explanation": "The dot product is calculated as $a_1b_1 + a_2b_2$. Here, $(2)(1) + (3)(-1) = 2 - 3 = -1$",
            "difficulty": "beginner"
        },
        {
            "id": "la_004b",
            "problem": "A force of 5N is applied to a box at a 60° angle from the horizontal. How much of the force is effectively pushing the box horizontally?",
            "type": QuestionType.MULTIPLE_CHOICE,
            "choices": [
                "2.5N",
                "4.33N",
                "2.89N",
                "5N"
            ],
            "answer": 1,
            "explanation": "The horizontal component is the dot product of the force vector with the unit vector [1,0]. Force × cos(60°) = 5 × 0.866 = 4.33N",
            "difficulty": "intermediate"
        },
        {
            "id": "la_004c",
            "problem": "In a video game physics engine, a character with velocity vector $\\vec{v} = \\begin{bmatrix} 3 \\\\ 4 \\\\ 0 \\end{bmatrix}$ m/s moves against a headwind with vector $\\vec{w} = \\begin{bmatrix} -2 \\\\ -2 \\\\ 0 \\end{bmatrix}$ m/s. Calculate the rate at which the wind is slowing the character (the dot product of these vectors).",
            "type": QuestionType.NUMERICAL,
            "answer": "-14",
            "explanation": "The dot product $\\vec{v} \\cdot \\vec{w}$ gives the rate of work: $(3)(-2) + (4)(-2) + (0)(0) = -6 - 8 + 0 = -14$ (negative indicates opposing motion)",
            "difficulty": "advanced"
        }
    ],
    "Cross Product": [
        {
            "id": "la_005a",
            "problem": "Calculate the cross product of vectors $\\vec{a} = \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}$ and $\\vec{b} = \\begin{bmatrix} 0 \\\\ 1 \\\\ 0 \\end{bmatrix}$. What is the third component of the resulting vector?",
            "type": QuestionType.NUMERICAL,
            "answer": "1",
            "explanation": "The cross product of unit vectors $\\hat{i} \\times \\hat{j}$ gives $\\hat{k}$. So the result is $\\begin{bmatrix} 0 \\\\ 0 \\\\ 1 \\end{bmatrix}$, and the third component is 1",
            "difficulty": "intermediate"
        },
        {
            "id": "la_005b",
            "problem": "In a 3D video game, a character's forward direction is $\\vec{f} = \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}$ and up direction is $\\vec{u} = \\begin{bmatrix} 0 \\\\ 0 \\\\ 1 \\end{bmatrix}$. Which vector represents the character's 'right' direction?",
            "type": QuestionType.MULTIPLE_CHOICE,
            "choices": [
                "$\\begin{bmatrix} 0 \\\\ -1 \\\\ 0 \\end{bmatrix}$",
                "$\\begin{bmatrix} 0 \\\\ 1 \\\\ 0 \\end{bmatrix}$",
                "$\\begin{bmatrix} -1 \\\\ 0 \\\\ 0 \\end{bmatrix}$",
                "$\\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}$"
            ],
            "answer": 1,
            "explanation": "The right direction is found using the cross product $\\vec{f} \\times \\vec{u}$, which gives $\\begin{bmatrix} 0 \\\\ 1 \\\\ 0 \\end{bmatrix}$ (right-hand rule)",
            "difficulty": "intermediate"
        },
        {
            "id": "la_005c",
            "problem": "A force of 3N is applied at the end of a 2m lever arm. If the force vector is $\\vec{F} = \\begin{bmatrix} 3 \\\\ 0 \\\\ 0 \\end{bmatrix}$ and the lever arm vector is $\\vec{r} = \\begin{bmatrix} 0 \\\\ 2 \\\\ 0 \\end{bmatrix}$, calculate the magnitude of the resulting torque (magnitude of $\\vec{r} \\times \\vec{F}$).",
            "type": QuestionType.NUMERICAL,
            "answer": "6",
            "explanation": "Torque magnitude = |$\\vec{r} \\times \\vec{F}$| = |\\vec{r}||\\vec{F}|\\sin(90°) = (2)(3)(1) = 6 N⋅m. The vectors are perpendicular, so sin(90°) = 1.",
            "difficulty": "advanced"
        }
    ],
    "Identity Matrix": [
        {
            "id": "la_006",
            "type": QuestionType.NUMERICAL,
            "problem": "What is the sum of all elements in the 3×3 identity matrix?",
            "answer": "3",
            "explanation": "The 3×3 identity matrix has 1's on the diagonal and 0's elsewhere: $\\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}$. Sum = 1 + 1 + 1 = 3",
            "difficulty": "beginner"
        }
    ],
    "Transpose": [
        {
            "id": "la_007",
            "type": QuestionType.NUMERICAL,
            "problem": "Given matrix $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\\\ 5 & 6 \\end{bmatrix}$, what is the element at position (2,1) in $A^T$?",
            "answer": "2",
            "explanation": "$A^T$ swaps rows and columns. The element at (2,1) in $A^T$ is the element at (1,2) in $A$, which is 2",
            "difficulty": "beginner"
        }
    ],
    "Inverse": [
        {
            "id": "la_008",
            "type": QuestionType.NUMERICAL,
            "problem": "For matrix $A = \\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}$, what is the element at position (1,1) in $A^{-1}$?",
            "answer": "0.5",
            "explanation": "This is a scalar multiple of the identity matrix. Its inverse is $\\frac{1}{2}I$, so each diagonal element becomes $\\frac{1}{2} = 0.5$",
            "difficulty": "intermediate"
        }
    ],
    "System of Linear Equations": [
        {
            "id": "la_009",
            "type": QuestionType.NUMERICAL,
            "problem": "In the system $\\begin{bmatrix} 2 & 1 \\\\ 1 & 1 \\end{bmatrix}\\begin{bmatrix} x \\\\ y \\end{bmatrix} = \\begin{bmatrix} 4 \\\\ 3 \\end{bmatrix}$, what is the value of x?",
            "answer": "1",
            "explanation": "From the equations: 2x + y = 4 and x + y = 3, subtract the second from the first to get x = 1",
            "difficulty": "intermediate"
        }
    ],
    "Linear Transformation": [
        {
            "id": "la_010",
            "type": QuestionType.NUMERICAL,
            "problem": "A linear transformation rotates vectors by 90° counterclockwise. What will be the coordinates of the transformed vector $\\vec{v} = \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix}$? Enter the x-coordinate.",
            "answer": "0",
            "explanation": "A 90° counterclockwise rotation transforms $\\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix}$ to $\\begin{bmatrix} 0 \\\\ 1 \\end{bmatrix}$. The x-coordinate is 0",
            "difficulty": "intermediate"
        }
    ],
    "Rank": [
        {
            "id": "la_011",
            "type": QuestionType.NUMERICAL,
            "problem": "What is the rank of the matrix $\\begin{bmatrix} 1 & 2 \\\\ 2 & 4 \\end{bmatrix}$?",
            "answer": "1",
            "explanation": "The second row is a scalar multiple (2×) of the first row, so these rows are linearly dependent. Therefore, the rank is 1",
            "difficulty": "intermediate"
        }
    ]
}

# Add more problem sets for other branches here