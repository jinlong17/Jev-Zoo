"""Bind an offline static payload to a reviewed source release; never deploys."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIAGNOSTIC_FILES = {"build-report.json", "audit-report.json"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_hash(files):
    canonical = json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def payload_files(output):
    files = {}
    for path in sorted(output.rglob("*")):
        if path.is_symlink():
            raise ValueError("Static payload cannot contain symlinks")
        if not path.is_file():
            continue
        relative = str(path.relative_to(output))
        if relative in DIAGNOSTIC_FILES:
            continue
        if (
            not relative.endswith((".html", ".json", ".js", ".css", ".svg"))
            and relative != ".nojekyll"
        ):
            raise ValueError("Unexpected static payload file: " + relative)
        files[relative] = digest(path)
    return files


def freeze(output, manifest):
    # GitHub Pages branch publishing must preserve directories without Jekyll processing.
    (output / ".nojekyll").write_text("")
    files = payload_files(output)
    data = json.loads((output / "assets/catalog.json").read_text())
    contract = {
        "schema_version": "1.0",
        "static_content_hash": content_hash(files),
        "registry_sha256": data["registry_sha256"],
        "locales": data["locales"],
        "html_pages": sum(path.endswith(".html") for path in files),
        "files": files,
        "target": {
            "provider": "GitHub Pages",
            "url": "https://jinlong17.github.io/Jev-Zoo/",
            "branch": "gh-pages",
            "directory": "/",
            "status": "proposed; publication and deployment require exact-release approval",
        },
        "build": "python site/build.py --output /absolute/path/outside/git/jevzoo-site",
        "diagnostics_excluded": sorted(DIAGNOSTIC_FILES),
        "no_model_or_api_execution": True,
    }
    manifest.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n")
    return contract


def verify(output, manifest):
    contract = json.loads(manifest.read_text())
    actual = payload_files(output)
    if actual != contract["files"]:
        missing = sorted(set(contract["files"]) - set(actual))
        extra = sorted(set(actual) - set(contract["files"]))
        changed = sorted(
            path
            for path in set(actual) & set(contract["files"])
            if actual[path] != contract["files"][path]
        )
        raise ValueError(
            f"Static payload drift: missing={missing[:4]}, extra={extra[:4]}, changed={changed[:4]}"
        )
    if content_hash(actual) != contract["static_content_hash"]:
        raise ValueError("Static manifest content hash changed")
    return contract


def archive(output, manifest, destination):
    contract = verify(output, manifest)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for relative in sorted(contract["files"]):
            # Stable zip headers make independently regenerated archives byte-identical.
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, (output / relative).read_bytes())
    return {
        "files": len(contract["files"]),
        "static_content_hash": contract["static_content_hash"],
        "archive_sha256": digest(destination),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["freeze", "verify", "archive"])
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument(
        "--manifest", type=pathlib.Path, default=ROOT / "site/deployment-manifest.json"
    )
    parser.add_argument("--archive", type=pathlib.Path)
    args = parser.parse_args()
    if args.action == "freeze":
        result = freeze(args.output, args.manifest)
    elif args.action == "verify":
        result = verify(args.output, args.manifest)
    else:
        if args.archive is None:
            parser.error("archive requires --archive")
        result = archive(args.output, args.manifest, args.archive)
    print(
        json.dumps(
            {key: value for key, value in result.items() if key != "files"}
            | {
                "file_count": len(result["files"])
                if isinstance(result.get("files"), dict)
                else result.get("files")
            },
            ensure_ascii=False,
            indent=2,
        )
    )
