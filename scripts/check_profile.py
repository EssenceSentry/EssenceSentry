"""Check the profile's local links and accessible image descriptions."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
readme = (root / "README.md").read_text(encoding="utf-8")
links = re.findall(r"(!?)\[([^\]]*)\]\(([^\s)]+)\)", readme)
if not links:
    raise SystemExit("The profile has no links or images to check.")

errors = []
for image, label, target in links:
    url = urlsplit(target)
    if image and not label.strip():
        errors.append(f"Image needs a description: {target}")
    if url.scheme:
        if url.scheme not in {"https", "mailto"}:
            errors.append(f"Unsupported link scheme: {target}")
        continue
    if url.netloc:
        errors.append(f"Use an explicit HTTPS URL: {target}")
        continue
    if url.path:
        path = (root / unquote(url.path)).resolve()
        if not path.is_relative_to(root) or not path.exists():
            errors.append(f"Missing local link target: {target}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(links)} profile links and image descriptions.")
