"""Centralized data structure for all mathematical disciplines."""

from . import (
    LINEAR_ALGEBRA_CONCEPTS,
    DIFFERENTIAL_CALCULUS_CONCEPTS,
    INTEGRATION_CONCEPTS,
    TRIGONOMETRY_CONCEPTS
)
from .practice_problems import LINEAR_ALGEBRA_PROBLEMS

# Centralized data structure for all disciplines
DISCIPLINES = {
    'linear-algebra': {
        'name': 'Linear Algebra',
        'template': 'linear_algebra.html',
        'concepts': LINEAR_ALGEBRA_CONCEPTS,
        'problems': LINEAR_ALGEBRA_PROBLEMS
    },
    'calculus': {
        'name': 'Differential Calculus',
        'template': 'calculus.html',
        'concepts': DIFFERENTIAL_CALCULUS_CONCEPTS,
        'problems': None
    },
    'integration': {
        'name': 'Integration',
        'template': 'integration.html',
        'concepts': INTEGRATION_CONCEPTS,
        'problems': None
    },
    'trigonometry': {
        'name': 'Trigonometry',
        'template': 'trigonometry.html',
        'concepts': TRIGONOMETRY_CONCEPTS,
        'problems': None
    }
}
