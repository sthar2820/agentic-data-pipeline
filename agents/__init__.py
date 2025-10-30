"""
Agents Package

Three specialized AI agents for data analytics:
- InspectorAgent: Data profiling and validation
- RefinerAgent: Data cleaning and transformation
- InsightAgent: Analysis and insights generation
"""

from .inspector import InspectorAgent
from .refiner import RefinerAgent
from .insight import InsightAgent

__all__ = ['InspectorAgent', 'RefinerAgent', 'InsightAgent']
