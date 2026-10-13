"""Audit generated pages, registry parity and public metadata without network calls."""

import argparse
import hashlib
import json
import pathlib
import re
import urllib.parse
from html.parser import HTMLParser


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        for key in ["href", "src"]:
            if key in attributes:
                self.links.append(attributes[key])


def audit(output):
    data = json.loads((output / "assets/catalog.json").read_text())
    failures = []
    pages = list(output.rglob("*.html"))
    for page in pages:
        parser = Links()
        source = page.read_text()
        parser.feed(source)
        if re.search(r"/(?:nfs[.]auto|home)/", source):
            failures.append({"page": str(page.relative_to(output)), "error": "private path"})
        for link in parser.links:
            parsed = urllib.parse.urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (page.parent / urllib.parse.unquote(parsed.path)).resolve()
            if not target.is_relative_to(output.resolve()) or not target.exists():
                failures.append(
                    {
                        "page": str(page.relative_to(output)),
                        "link": link,
                        "error": "missing/escaping internal target",
                    }
                )
    for locale in ["en", "zh"]:
        for record in data["resources"]:
            if not (output / locale / "resources" / record["slug"] / "index.html").exists():
                failures.append(
                    {"resource_id": record["id"], "locale": locale, "error": "missing locale page"}
                )
    # Data projection must still correspond to the current registry.
    repo = pathlib.Path(__file__).resolve().parents[1]
    registry_hash = hashlib.sha256((repo / "catalog/catalog.json").read_bytes()).hexdigest()
    if registry_hash != data["registry_sha256"]:
        failures.append({"error": "stale registry projection"})
    if re.search(r"/(?:nfs[.]auto|home)/", (output / "assets/catalog.json").read_text()):
        failures.append({"error": "private path in metadata"})
    report = {
        "html_pages_checked": len(pages),
        "locale_resources_each": len(data["resources"]),
        "registry_sha256": registry_hash,
        "failures": failures,
        "passed": not failures,
        "network_calls": 0,
        "external_link_scope": "Inherited discovery checks and primary-source audit; this offline pass checks internal paths only.",
    }
    (output / "audit-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    audit(parser.parse_args().output.resolve())
