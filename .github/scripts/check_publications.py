"""
Monthly publication check against Semantic Scholar.

Finds papers not yet in content/publication/ or publications.bib,
fetches their bibtex from doi.org, and appends them to publications.bib.
Writes a human-readable summary to $GITHUB_OUTPUT for the PR body.
"""

import os
import re
import sys
import time
import json
import textwrap
import requests
from pathlib import Path

AUTHOR_ID = "47680095"  # Aneesh C. Subramanian on Semantic Scholar
SS_PAPERS = (
    f"https://api.semanticscholar.org/graph/v1/author/{AUTHOR_ID}/papers"
)
FIELDS = "title,year,venue,externalIds,authors"
PUB_BIB = Path("publications.bib")


def _get_with_retry(url: str, params: dict, max_retries: int = 5) -> requests.Response:
    """GET with exponential backoff on 429 rate-limit responses."""
    delay = 10
    for attempt in range(max_retries):
        r = requests.get(url, params=params, timeout=20)
        if r.status_code != 429:
            r.raise_for_status()
            return r
        retry_after = int(r.headers.get("Retry-After", delay))
        wait = max(retry_after, delay)
        print(f"  Rate limited (429); waiting {wait}s before retry {attempt + 1}/{max_retries} ...")
        time.sleep(wait)
        delay = min(delay * 2, 120)
    r.raise_for_status()
    return r


def get_all_papers() -> list[dict]:
    papers: list[dict] = []
    offset = 0
    while True:
        r = _get_with_retry(
            SS_PAPERS,
            params={"fields": FIELDS, "limit": 100, "offset": offset},
        )
        data = r.json()
        papers.extend(data["data"])
        if "next" not in data:
            break
        offset = data["next"]
        time.sleep(2)  # be polite to the API between pages
    return papers


def get_known_dois() -> set[str]:
    """Collect DOIs already present in content/publication/ and publications.bib."""
    dois: set[str] = set()
    pattern = re.compile(r"doi\s*=\s*\{([^}]+)\}", re.IGNORECASE)

    for bib in Path("content/publication").rglob("cite.bib"):
        for m in pattern.finditer(bib.read_text(errors="ignore")):
            dois.add(m.group(1).strip().lower())

    if PUB_BIB.exists():
        for m in pattern.finditer(PUB_BIB.read_text(errors="ignore")):
            dois.add(m.group(1).strip().lower())

    return dois


def fetch_bibtex(doi: str) -> str | None:
    """Fetch bibtex from doi.org content negotiation."""
    try:
        r = requests.get(
            f"https://doi.org/{doi}",
            headers={"Accept": "application/x-bibtex"},
            allow_redirects=True,
            timeout=20,
        )
        text = r.text.strip()
        if r.status_code == 200 and text.startswith("@"):
            return text
    except requests.RequestException:
        pass
    return None


def main() -> int:
    print("Fetching all papers from Semantic Scholar ...")
    papers = get_all_papers()
    print(f"  Total papers on Semantic Scholar: {len(papers)}")

    known_dois = get_known_dois()
    print(f"  DOIs already in repo: {len(known_dois)}")

    new_papers = [
        p for p in papers
        if (doi := (p.get("externalIds") or {}).get("DOI"))
        and doi.lower() not in known_dois
    ]

    if not new_papers:
        print("No new papers found — nothing to do.")
        _set_output("new_count", "0")
        _set_output("summary", "No new papers found.")
        return 0

    print(f"\nNew papers found: {len(new_papers)}")

    bibtex_blocks: list[str] = []
    summary_rows: list[str] = []

    for p in new_papers:
        doi = (p.get("externalIds") or {}).get("DOI", "")
        title = p.get("title", "Unknown title")
        year = p.get("year") or "?"
        venue = p.get("venue") or "Unknown venue"
        authors = ", ".join(
            a.get("name", "") for a in (p.get("authors") or [])
        )

        print(f"  · {title} ({year})")
        bib = fetch_bibtex(doi)
        if bib:
            bibtex_blocks.append(bib)
            status = "bibtex fetched"
        else:
            # Fallback: minimal stub the user can fix
            bibtex_blocks.append(
                f"@article{{stub_{doi.replace('/', '_')},\n"
                f"  title = {{{title}}},\n"
                f"  author = {{{authors}}},\n"
                f"  year = {{{year}}},\n"
                f"  doi = {{{doi}}},\n"
                f"}}"
            )
            status = "⚠️ bibtex fetch failed — stub added"

        summary_rows.append(
            f"| {title} | {authors[:60]}... | {year} | {venue} | `{doi}` | {status} |"
        )
        time.sleep(0.3)

    # Append new entries to publications.bib
    with PUB_BIB.open("a") as f:
        f.write("\n\n" + "\n\n".join(bibtex_blocks) + "\n")

    summary = textwrap.dedent(f"""\
        ## {len(new_papers)} new paper(s) found on Semantic Scholar

        | Title | Authors | Year | Venue | DOI | Status |
        |-------|---------|------|-------|-----|--------|
        {chr(10).join(summary_rows)}

        ---
        **Review this PR:**
        - ✅ Merge to add these publications to your site
        - ✏️ Edit `publications.bib` in this PR to correct any entries
        - 🗑️ Delete entries from `publications.bib` you don't want to add
        - ❌ Close without merging to skip all of them
    """)

    _set_output("new_count", str(len(new_papers)))
    _set_output("summary", summary)

    print(f"\nDone. Appended {len(bibtex_blocks)} entries to {PUB_BIB}.")
    return 0


def _set_output(key: str, value: str) -> None:
    """Write to $GITHUB_OUTPUT (multiline-safe)."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        delimiter = "EOF_DELIM"
        with open(output_file, "a") as f:
            f.write(f"{key}<<{delimiter}\n{value}\n{delimiter}\n")
    else:
        print(f"[output] {key}={value[:120]}")


if __name__ == "__main__":
    sys.exit(main())
