#!/usr/bin/env python3
"""
Utility to inject the provided Google tag (gtag.js) snippet into all HTML pages.
- Inserts the snippet immediately after <head>
- Removes the old GTM-WJKXQG3K snippet to keep only one Google code per page
- Skips files that already contain the new measurement ID
"""

from pathlib import Path
import re
from typing import Tuple

ROOT = Path(__file__).parent
MEASUREMENT_ID = "G-X1H7E6RXSX"
OLD_GTM_ID = "GTM-WJKXQG3K"

HEAD_SNIPPET = f"""    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', '{MEASUREMENT_ID}');
    </script>"""


def strip_old_gtm(html: str) -> str:
    """Remove the previous GTM snippet if present so only one Google code remains."""
    patterns = [
        r"\s*<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\s*",
        r"\s*<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->\s*",
    ]
    cleaned = html
    for pattern in patterns:
        cleaned = re.sub(pattern, "\n", cleaned, flags=re.DOTALL | re.IGNORECASE)
    return cleaned


def inject_gtm(html: str) -> Tuple[str, bool]:
    if MEASUREMENT_ID in html:
        return html, False

    html = strip_old_gtm(html)

    head_match = re.search(r"<head[^>]*>", html, re.IGNORECASE)
    if not head_match:
        return html, False

    with_head = html[: head_match.end()] + "\n" + HEAD_SNIPPET + html[head_match.end() :]
    return with_head, True


def main() -> None:
    html_files = sorted(ROOT.rglob("*.html"))
    updated = []
    skipped = []

    for path in html_files:
        original = path.read_text(encoding="utf-8")
        new_content, changed = inject_gtm(original)
        if changed:
            path.write_text(new_content, encoding="utf-8")
            updated.append(path)
        else:
            skipped.append(path)

    print(f"Updated {len(updated)} file(s).")
    for path in updated:
        print(f"  + {path.relative_to(ROOT)}")

    if skipped:
        print(f"Skipped {len(skipped)} already tagged file(s).")


if __name__ == "__main__":
    main()
