"""Mompy backend package.

The frontend owns the CRT interface. This package owns the Python learning
logic that will be connected to the interface in the next phase.
"""

from .api import MompyAPI

__all__ = ["MompyAPI"]
