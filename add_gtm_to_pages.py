#!/usr/bin/env python3
"""
Utility to inject the Google Tag Manager snippet into all HTML pages.
- Adds the script block near the top of <head>
- Adds the noscript iframe immediately after <body>
- Skips files that already contain the GTM container ID
"""

from pathlib import Path
import re
from typing import Tuple

ROOT = Path(__file__).parent
GTM_ID = "GTM-WJKXQG3K"

HEAD_SNIPPET = """    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-WJKXQG3K');</script>
    <!-- End Google Tag Manager -->"""

BODY_SNIPPET = """    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WJKXQG3K"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->"""


def inject_gtm(html: str) -> Tuple[str, bool]:
    if GTM_ID in html:
        return html, False

    head_match = re.search(r"<head[^>]*>", html, re.IGNORECASE)
    body_match = re.search(r"<body[^>]*>", html, re.IGNORECASE)

    if not head_match or not body_match:
        return html, False

    with_head = html[: head_match.end()] + "\n" + HEAD_SNIPPET + html[head_match.end() :]

    # Re-search for body after head injection to keep offsets accurate
    body_match = re.search(r"<body[^>]*>", with_head, re.IGNORECASE)
    if not body_match:
        return html, False

    with_body = (
        with_head[: body_match.end()] + "\n" + BODY_SNIPPET + with_head[body_match.end() :]
    )
    return with_body, True


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
