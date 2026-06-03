from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _json_default(value: Any) -> str:
    """Fallback JSON serializer for simple archive logging."""
    return str(value)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _try_command(command: list[str], cwd: Path | None = None) -> str | None:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


@dataclass
class RunArchive:
    """Minimal archive for reproducible optimisation or simulation runs.

    The archive stores metadata, configs, evaluation logs, and arbitrary JSON
    files in a single run directory.
    """

    path: str | Path
    create: bool = True

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        if self.create:
            self.path.mkdir(parents=True, exist_ok=True)

    @property
    def evaluations_path(self) -> Path:
        return self.path / "evaluations.jsonl"

    def save_metadata(self, extra: dict[str, Any] | None = None) -> Path:
        """Write basic reproducibility metadata."""
        metadata: dict[str, Any] = {
            "created_at_utc": _utc_now(),
            "python": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "git_commit": _try_command(["git", "rev-parse", "HEAD"]),
            "git_branch": _try_command(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
            "git_dirty": self._git_dirty(),
        }

        if extra:
            metadata.update(extra)

        return self.save_json("metadata.json", metadata)

    def _git_dirty(self) -> bool | None:
        status = _try_command(["git", "status", "--porcelain"])
        if status is None:
            return None
        return bool(status)

    def save_config(self, source: str | Path, name: str | None = None) -> Path:
        """Copy a configuration file into the archive."""
        source_path = Path(source)
        if not source_path.exists():
            raise FileNotFoundError(f"Config file not found: {source_path}")

        destination = self.path / (name or source_path.name)
        shutil.copy2(source_path, destination)
        return destination

    def save_json(self, name: str, data: dict[str, Any] | list[Any]) -> Path:
        """Save a JSON file inside the archive."""
        destination = self.path / name
        destination.parent.mkdir(parents=True, exist_ok=True)

        with destination.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False, default=_json_default)

        return destination

    def log_evaluation(
        self,
        design: dict[str, Any],
        objectives: dict[str, float],
        constraints: dict[str, float] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Append one design evaluation to evaluations.jsonl."""
        record = {
            "timestamp_utc": _utc_now(),
            "design": design,
            "objectives": objectives,
            "constraints": constraints or {},
            "metadata": metadata or {},
        }

        with self.evaluations_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False, default=_json_default))
            file.write("\n")

        return self.evaluations_path
