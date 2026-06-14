"""Safe local JSON storage helpers."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
PROGRESS_PATH = DATA_DIR / "progress.json"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def write_json(path: Path, data: Any) -> None:
    ensure_parent(path)
    payload = json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True)

    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp",
    ) as handle:
        handle.write(payload)
        temp_name = handle.name

    Path(temp_name).replace(path)


def resolve_data_path(filename: str) -> Path:
    safe_name = Path(filename).name
    return DATA_DIR / safe_name
