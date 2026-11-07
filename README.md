# Afaf Loudini website

Static French website for https://afafloudini.com/, hosted from the repository with GitHub Pages. No JavaScript framework or build step is required to serve the committed HTML files.

## Editing

- Content, shared page structure and metadata: `scripts/build_site.py`.
- Responsive styles: `css/site.css`.
- Accessible mobile navigation: `js/site.js`.
- Content/image sources: `RESEARCH.md`.

After changing the page template, regenerate with Python 3.12+ and Pillow installed:

```sh
python3 scripts/build_site.py
```

The generated HTML is committed so hosting does not need Python. Existing page URLs, `CNAME`, `robots.txt`, and `sitemap.xml` are retained. Original image files and legacy styles/scripts remain available for old external links; the refreshed pages use only the new stylesheet and script.

## Local preview

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/. Mobile navigation, appointment links, FAQs and directions work without a frontend dependency. Without JavaScript, navigation stays visible and the FAQ uses native HTML disclosure elements.

## Validation

```sh
python3 scripts/check_site.py
node --check js/site.js
```
