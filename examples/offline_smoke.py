"""Core-only public example: a synthetic fixture, never a real-model score."""

from pathlib import Path

from jev_zoo.runner import run

print(run(Path.cwd(), "mock", "synthetic-smoke", profile="synthetic", max_samples=8))
