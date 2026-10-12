from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def main(argv=None):
    # A process-level lock makes every GPU evaluate/train command serial on its assigned device.
    import fcntl
    import sys

    from .storage import workspace

    args = argv if argv is not None else sys.argv[1:]
    if "evaluate" in args or "train" in args:
        root = workspace()
        lock_path = (
            root
            / "tracking"
            / ("gpu-" + os.environ.get("CUDA_VISIBLE_DEVICES", "0").replace(",", "-") + ".lock")
        )
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            return _main(args)
    return _main(args)


def _main(argv=None):
    parser = argparse.ArgumentParser(prog="jevzoo")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("--manifest", type=Path, required=True)
    fetch.add_argument("--only", nargs="+")
    fetch.add_argument("--workers", type=int, default=4)
    freeze = sub.add_parser("freeze")
    catalog = sub.add_parser("catalog")
    catalog.add_argument("action", choices=["refresh", "render"])
    catalog.add_argument("--seed", type=Path, default=Path("planning/catalog_seed.json"))
    catalog.add_argument("--verify-links", action="store_true")
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--suite", required=True)
    evaluate.add_argument("--deployment", default="qwen35-4b")
    evaluate.add_argument(
        "--profile", choices=["smoke", "full", "diagnostic", "synthetic"], default="smoke"
    )
    evaluate.add_argument("--resume", type=Path)
    evaluate.add_argument("--calibration-data", type=Path)
    evaluate.add_argument("--calibration", type=Path)
    evaluate.add_argument("--rotations", type=int, default=1)
    evaluate.add_argument("--max-samples", type=int)
    evaluate.add_argument("--max-tokens", type=int, default=32768)
    report = sub.add_parser("report")
    report.add_argument("--run", type=Path, required=True)
    import importlib.util

    if importlib.util.find_spec("jev_zoo.release") is not None:
        release = sub.add_parser("release")
        release.add_argument("action", choices=["prepare", "publish"])
        release.add_argument("--public-repo", type=Path)
        release.add_argument("--candidate", type=Path)
        release.add_argument("--approval", type=Path)
    if importlib.util.find_spec("jev_zoo.training") is not None:
        train = sub.add_parser("train")
        train.add_argument("--config", type=Path, required=True)
        train.add_argument("--resume", type=Path)
    calibrate = sub.add_parser("calibrate")
    calibrate.add_argument("--run", type=Path, required=True)
    calibrate.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    if args.command == "fetch":
        from .fetch import fetch_manifest, fetch_workers

        locked = json.loads(args.manifest.read_text())
        statuses = (
            fetch_workers(args.manifest)
            if "workers" in locked
            else fetch_manifest(args.manifest, only=args.only, workers=args.workers)
        )
        print(json.dumps(statuses, indent=2))
        return 1 if any(s != "downloaded" for s in statuses.values()) else 0
    if args.command == "freeze":
        from .fetch import freeze

        print(freeze(repo))
    elif args.command == "catalog":
        from .catalog import refresh, render

        if args.action == "refresh":
            refresh(repo, args.seed, verify_links=args.verify_links)
        render(repo)
    elif args.command == "evaluate":
        from .runner import run
        from .tasks import SUITES

        suites = SUITES if args.suite == "jevzoo-eval-v0.1" else [args.suite]
        if args.resume and len(suites) > 1:
            parser.error("Resume specifies one benchmark, not the entire suite")
        failed = False
        for suite in suites:
            directory = run(
                repo,
                args.deployment,
                suite,
                profile=args.profile,
                resume=args.resume,
                max_samples=args.max_samples,
                max_tokens=args.max_tokens,
                calibration_data=args.calibration_data,
                rotations=args.rotations,
                calibration=args.calibration,
            )
            print(directory)
            metrics = json.loads((directory / "metrics.json").read_text())
            failed |= bool(metrics["errors"]) or metrics["attempted"] != metrics["eligible"]
        return 1 if failed else 0
    elif args.command == "report":
        from .runner import report

        print(json.dumps(report(args.run), indent=2))
    elif args.command == "release":
        from .release import prepare, publish

        if args.action == "prepare":
            print(prepare(repo, args.public_repo))
        else:
            if not (args.public_repo and args.candidate and args.approval):
                parser.error("Publish requires public repo, exact candidate and approval receipt")
            print(publish(repo, args.public_repo, args.candidate, args.approval))
    elif args.command == "train":
        from .training import train

        print(train(repo, args.config, resume=args.resume))
    elif args.command == "calibrate":
        from .calibration import fit_from_run

        print(fit_from_run(args.run, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
