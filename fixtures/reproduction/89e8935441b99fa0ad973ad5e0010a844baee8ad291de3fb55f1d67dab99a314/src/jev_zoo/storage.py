from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def workspace(value: str | Path | None = None) -> Path:
    configured = value or os.environ.get("JEVZOO_WORKSPACE")
    if not configured:
        raise ValueError("Set JEVZOO_WORKSPACE to a directory outside all Git worktrees")
    root = Path(configured).expanduser().resolve()
    for parent in (root, *root.parents):
        marker = parent / ".git"
        # An aggregation directory may contain only .git/info/exclude. It is not a
        # Git repository; real repositories and gitdir worktree pointers are rejected.
        if marker.is_file() or (marker.is_dir() and (marker / "HEAD").is_file()):
            raise ValueError("JEVZOO_WORKSPACE must not be inside a Git worktree")
    return root


def safe_child(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts or "\\" in relative:
        raise ValueError("Unsafe relative path")
    cursor = root
    for part in candidate.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("Symbolic links are not authorized asset/publication paths")
    target = (root / candidate).resolve()
    if target == root.resolve() or not target.is_relative_to(root.resolve()):
        raise ValueError("Path escapes its authorized root")
    return target


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    descriptor, temporary = tempfile.mkstemp(prefix=".jevzoo-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + "\n")
        handle.flush()


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
