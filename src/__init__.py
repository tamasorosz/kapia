"""
Kapia: a lightweight glue library for FEM-based robust optimisation workflows.
"""

from kapia.archive import RunArchive
from kapia.runners import ExternalRunner, RunnerResult

__version__ = "0.0.1"

__all__ = [
    "__version__",
    "RunArchive",
    "ExternalRunner",
    "RunnerResult",
]