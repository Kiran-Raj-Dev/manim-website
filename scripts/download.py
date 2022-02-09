import base64
import cgi
import json
import os
import re
from pathlib import Path

import readme_renderer.markdown
import readme_renderer.rst
import readme_renderer.txt
import requests

CONTENT_FOLDER = Path(__file__).parent.parent / "content"
REGEX = re.compile(r"<(.*)>manim-(?P<name>.*)<(.*)>")
IDS = []

# shamelessly copied from
# https://github.com/pypa/warehouse/blob/7fc3ce5bd7ecc93ef54c1652787fb5e7757fe6f2/warehouse/utils/readme.py


def render_readme(
    value,
    content_type=None,
    use_fallback=True,
):
    _RENDERERS = {
        None: readme_renderer.rst,  # Default if description_content_type is None
        "": readme_renderer.rst,  # Default if description_content_type is None
        "text/plain": readme_renderer.txt,
        "text/x-rst": readme_renderer.rst,
        "text/markdown": readme_renderer.markdown,
    }
    if value is None:
        return value

    content_type, parameters = cgi.parse_header(content_type or "")
    renderer = _RENDERERS.get(content_type, readme_renderer.txt)
    rendered = renderer.render(value, **parameters)
    if use_fallback and rendered is None:
        rendered = readme_renderer.txt.render(value)

    return rendered


content = requests.get("https://pypi.org/simple")
content = content.text.split("\n")

with open(Path(__file__).parent / "default.json") as f:
    default = json.load(f)

for i in content:
    if "manim" in i:
        things = REGEX.search(i)
        if things:
            if (
                "manim-" + things.group("name")
                not in default["exclude"] + default["archive"]
            ):
                IDS.append("manim-" + things.group("name"))
IDS.extend(default["extras"])
if not (CONTENT_FOLDER).exists():
    CONTENT_FOLDER.mkdir()

for id in IDS:
    file = Path(CONTENT_FOLDER, f"{id}.json")
    if file.exists():
        continue
    c = requests.get(f"https://pypi.org/pypi/{id}/json").json()
    description = render_readme(
        c["info"]["description"],
        content_type=c["info"]["description_content_type"],
    )
    c["info"]["description"] = description  # convert md to html

    with open(file, "w", encoding="utf-8") as f:
        json.dump(c, f)

front_matter_md = """\
---
slug: "/governance"
title: "Manim governance"
date: {date}
description: "Manim's governance model"
---
"""

GITHUB_TOKEN = os.environ.get('TOKEN_FOR_API_GITHUB_PRIVATE')
if GITHUB_TOKEN:
    req = requests.get("https://api.github.com/repos/manimcommunity/official_documents/contents/steering_council.md",
                       headers={"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GITHUB_TOKEN}"})
    last_mod_req = requests.get("https://api.github.com/repos/manimcommunity/official_documents/commits?path=steering_council.md&page=1&per_page=1",
                                headers={"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GITHUB_TOKEN}"})
    date = last_mod_req.json()[0]['commit']['committer']['date']
    contents = base64.b64decode(req.json()['content'])

    with open(Path(CONTENT_FOLDER, f"steering_council.md"), 'w', encoding='utf-8') as f:
        f.write(front_matter_md.format(date=date))
        f.write('\n')
        f.write(contents.decode('utf-8'))
else:
    # Create a empty file so that the build doesn't error
    # out for people with no access to Steering Council repo
    with open(Path(CONTENT_FOLDER, f"steering_council.md"), 'w', encoding='utf-8') as f:
        f.write(front_matter_md.format(date='2021-12-05'))
        f.write('\n')
        f.write('# This is a stub file.')
