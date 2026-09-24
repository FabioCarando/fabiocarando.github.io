import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "FabioCarando"
OUTPUT = Path("assets/svg/fabio-os.svg")


def github_api(endpoint):
    request = urllib.request.Request(
        f"https://api.github.com{endpoint}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USERNAME,
        },
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def relative_time(date_string):
    date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    delta = now - date
    minutes = int(delta.total_seconds() / 60)
    hours = int(delta.total_seconds() / 3600)
    days = delta.days

    if minutes < 1:
        return "just now"
    if minutes < 60:
        return f"{minutes}m ago"
    if hours < 24:
        return f"{hours}h ago"
    if days == 1:
        return "yesterday"

    return f"{days}d ago"


repos = github_api(
    f"/users/{USERNAME}/repos?per_page=100&sort=updated"
)

public_repos = len(repos)

languages = []

for repo in repos:
    language = repo.get("language")

    if language and language not in languages:
        languages.append(language)

languages = languages[:4]

latest_repo = repos[0] if repos else None

if latest_repo:
    latest_project = latest_repo["name"]
    latest_update = relative_time(latest_repo["updated_at"])
else:
    latest_project = "—"
    latest_update = "—"

language_string = " · ".join(languages) if languages else "—"


svg = f"""
<svg width="1000" height="440"
     viewBox="0 0 1000 440"
     xmlns="http://www.w3.org/2000/svg">

<style>

.background {{
    fill: #0d1117;
}}

.border {{
    fill: none;
    stroke: #30363d;
    stroke-width: 1;
}}

.title {{
    font: 700 18px monospace;
    fill: #ffffff;
    letter-spacing: 3px;
}}

.online {{
    font: 13px monospace;
    fill: #3fb950;
}}

.section {{
    font: 700 12px monospace;
    fill: #8b949e;
    letter-spacing: 2px;
}}

.label {{
    font: 14px monospace;
    fill: #8b949e;
}}

.value {{
    font: 14px monospace;
    fill: #ffffff;
}}

.dim {{
    font: 12px monospace;
    fill: #484f58;
}}

.pulse {{
    fill: #3fb950;
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0%   {{ opacity: 1; }}
    50%  {{ opacity: .25; }}
    100% {{ opacity: 1; }}
}}

</style>

<rect width="100%" height="100%" rx="14" class="background"/>

<rect
    x="1"
    y="1"
    width="998"
    height="438"
    rx="14"
    class="border"
/>

<!-- HEADER -->

<text x="45" y="55" class="title">
FABIO OS
</text>

<circle cx="835" cy="49" r="5" class="pulse"/>

<text x="850" y="54" class="online">
ONLINE
</text>

<line
    x1="45"
    y1="80"
    x2="955"
    y2="80"
    stroke="#30363d"
/>

<!-- SYSTEM -->

<text x="45" y="120" class="section">
SYSTEM
</text>

<text x="45" y="155" class="label">
ROLE
</text>

<text x="220" y="155" class="value">
Data Scientist
</text>

<text x="45" y="185" class="label">
FOCUS
</text>

<text x="220" y="185" class="value">
AI · Automation · Data Products
</text>

<text x="45" y="215" class="label">
MODE
</text>

<text x="220" y="215" class="value">
BUILDING
</text>

<!-- GITHUB LIVE -->

<text x="530" y="120" class="section">
GITHUB / LIVE
</text>

<text x="530" y="155" class="label">
REPOSITORIES
</text>

<text x="720" y="155" class="value">
{public_repos}
</text>

<text x="530" y="185" class="label">
LATEST
</text>

<text x="720" y="185" class="value">
{latest_project}
</text>

<text x="530" y="215" class="label">
UPDATED
</text>

<text x="720" y="215" class="value">
{latest_update}
</text>

<!-- SIGNAL -->

<line
    x1="45"
    y1="255"
    x2="955"
    y2="255"
    stroke="#30363d"
/>

<text x="45" y="300" class="section">
CURRENT SIGNAL
</text>

<text x="45" y="340" class="value">
{language_string}
</text>

<text x="45" y="395" class="dim">
generated from github · automatic system
</text>

<text
    x="955"
    y="395"
    text-anchor="end"
    class="dim">
fabio@github:~$
</text>

</svg>
"""


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(svg, encoding="utf-8")

print(f"Generated {OUTPUT}")