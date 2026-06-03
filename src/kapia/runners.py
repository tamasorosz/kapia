from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunnerResult:
    """Result of an external simulation or script run."""

    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass
class ExternalRunner:
    """Minimal wrapper around an external command.

    This is intentionally simple. Later it can be specialised for FEMM, Agros,
    COMSOL, OpenFOAM, CalculiX, or custom scripts.
    """

    command: list[str]
    cwd: str | Path | None = None
    env: dict[str, str] = field(default_factory=dict)

    def run(self, timeout: float | None = None) -> RunnerResult:
        environment = os.environ.copy()
        environment.update(self.env)

        completed = subprocess.run(
            self.command,
            cwd=self.cwd,
            env=environment,
            timeout=timeout,
            capture_output=True,
            text=True,
        )

        return RunnerResult(
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
