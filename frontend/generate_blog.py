#!/usr/bin/env python3
"""
Static blog generator.

Reads Markdown posts from /posts and generates static HTML pages under /blog,
styled to match the main site (index.html) — same colors, fonts, nav, footer.

Usage:
    uv run python generate_blog.py
    (or: python generate_blog.py, if `markdown` is installed in your env)

To publish a new post:
    1. Create a new file in /posts, e.g. posts/my-new-post.md
    2. Add frontmatter at the top:

       ---
       title: My New Post
       date: 2026-08-21
       excerpt: One-line summary shown on the blog listing page.
       ---

       Then write the post body in Markdown below the second ---.

    3. Run this script again. It regenerates blog/index.html and
       blog/<slug>.html for every post in /posts — safe to re-run anytime.
"""

import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
BLOG_DIR = ROOT / "blog"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

MASCOT_HTML = """
  <button class="mascot" type="button" aria-label="Back to home" onclick="window.location.href='../index.html'">
    <svg viewBox="0 0 76 88" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">
      <g fill="var(--text)">
        <rect x="28" y="0" width="20" height="4"/>
        <rect x="48" y="4" width="8" height="4"/>
        <rect x="20" y="4" width="4" height="4"/>
        <rect x="12" y="8" width="4" height="4"/>
        <rect x="56" y="8" width="4" height="4"/>
        <rect x="8" y="12" width="4" height="4"/>
        <rect x="60" y="12" width="4" height="4"/>
        <rect x="4" y="16" width="4" height="4"/>
        <rect x="64" y="16" width="4" height="4"/>
        <rect x="4" y="20" width="4" height="4"/>
        <rect x="64" y="20" width="4" height="4"/>
        <rect x="0" y="24" width="4" height="4"/>
        <rect x="68" y="24" width="4" height="4"/>
        <rect x="0" y="28" width="4" height="4"/>
        <rect x="68" y="28" width="4" height="4"/>
        <rect x="0" y="32" width="4" height="4"/>
        <rect x="68" y="32" width="4" height="4"/>
        <rect x="0" y="36" width="4" height="4"/>
        <rect x="68" y="36" width="4" height="4"/>
        <rect x="0" y="40" width="4" height="4"/>
        <rect x="68" y="40" width="4" height="4"/>
        <rect x="0" y="44" width="4" height="4"/>
        <rect x="68" y="44" width="4" height="4"/>
        <rect x="4" y="48" width="4" height="4"/>
        <rect x="64" y="48" width="4" height="4"/>
        <rect x="4" y="52" width="4" height="4"/>
        <rect x="64" y="52" width="4" height="4"/>
        <rect x="8" y="56" width="4" height="4"/>
        <rect x="60" y="56" width="4" height="4"/>
        <rect x="8" y="60" width="4" height="4"/>
        <rect x="60" y="60" width="4" height="4"/>
        <rect x="12" y="64" width="4" height="4"/>
        <rect x="56" y="64" width="4" height="4"/>
        <rect x="16" y="68" width="4" height="4"/>
        <rect x="52" y="68" width="4" height="4"/>
        <rect x="20" y="72" width="4" height="4"/>
        <rect x="48" y="72" width="4" height="4"/>
        <rect x="24" y="76" width="4" height="4"/>
        <rect x="44" y="76" width="4" height="4"/>
        <rect x="28" y="80" width="4" height="4"/>
        <rect x="40" y="80" width="4" height="4"/>
        <rect x="32" y="84" width="8" height="4"/>
        <rect x="28" y="64" width="16" height="4"/>
      </g>
      <g fill="var(--accent)">
        <rect x="8" y="28" width="12" height="4"/>
        <rect x="8" y="32" width="4" height="4"/>
        <rect x="16" y="32" width="8" height="4"/>
        <rect x="8" y="36" width="20" height="4"/>
        <rect x="8" y="40" width="24" height="4"/>
        <rect x="12" y="44" width="20" height="4"/>
        <rect x="16" y="48" width="16" height="4"/>
        <rect x="20" y="52" width="12" height="4"/>
        <rect x="52" y="28" width="12" height="4"/>
        <rect x="48" y="32" width="8" height="4"/>
        <rect x="60" y="32" width="4" height="4"/>
        <rect x="44" y="36" width="20" height="4"/>
        <rect x="40" y="40" width="24" height="4"/>
        <rect x="40" y="44" width="20" height="4"/>
        <rect x="40" y="48" width="16" height="4"/>
        <rect x="40" y="52" width="12" height="4"/>
      </g>
    </svg>
  </button>
"""

NAV_HTML = """
  <nav id="nav">
  <div class="nav-inner">
    <div class="nav-links">
      <a href="{home}">Home</a>
      <a href="{home}#expertise">Expertise</a>
      <a href="{home}#work">Work</a>
      <a href="{home}#experience">Experience</a>
      <a href="{blog_home}">Blog</a>
      <a href="{home}#contact">Contact</a>
    </div>
  </div>
</nav>
"""

FOOTER_HTML = """
  <footer>
    <p>&copy; 2026 Uli Rotela. All rights reserved.</p>
  </footer>
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Text:ital@0;1&family=Doto:wght@400..900&family=Inter:wght@400;500;600;700&family=Pixelify+Sans:wght@400..700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body class="blog-page">
{mascot}
{nav}
{body}
{footer}
</body>
</html>
"""


def parse_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Post is missing a frontmatter block (--- ... ---) at the top of the file.")
    raw_meta, body = match.groups()
    meta = {}
    for line in raw_meta.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body


def slugify(name: str) -> str:
    return name


def load_posts() -> list[dict]:
    posts = []
    for md_file in sorted(POSTS_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        html_body = markdown.markdown(body.strip(), extensions=["fenced_code", "tables"])
        posts.append({
            "slug": slugify(md_file.stem),
            "title": meta.get("title", md_file.stem),
            "date": meta.get("date", ""),
            "excerpt": meta.get("excerpt", ""),
            "html": html_body,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def render_listing(posts: list[dict]) -> str:
    if not posts:
        cards = '<p class="empty-state">// no posts yet</p>'
    else:
        cards = '<div class="blog-list">\n'
        for p in posts:
            cards += f"""    <a class="blog-card" href="{p['slug']}.html">
      <div class="post-date">{p['date']}</div>
      <h3>{p['title']}</h3>
      <p>{p['excerpt']}</p>
    </a>
"""
        cards += "  </div>"

    body = f"""  <section class="blog-header">
    <h1>Blog</h1>
    <p class="tagline">Notes on AI engineering, systems, and building in production</p>
    {cards}
  </section>"""

    return PAGE_TEMPLATE.format(
        title="Blog — Uli Rotela",
        mascot=MASCOT_HTML,
        nav=NAV_HTML.format(home="../index.html", blog_home="index.html"),
        body=body,
        footer=FOOTER_HTML,
    )


def render_post(post: dict) -> str:
    body = f"""  <section>
    <a class="back-link" href="index.html">&larr; back to blog</a>
    <div class="post-header">
      <div class="post-meta">{post['date']}</div>
      <h1>{post['title']}</h1>
    </div>
    <div class="post-content">
      {post['html']}
    </div>
  </section>"""

    return PAGE_TEMPLATE.format(
        title=f"{post['title']} — Uli Rotela",
        mascot=MASCOT_HTML,
        nav=NAV_HTML.format(home="../index.html", blog_home="index.html"),
        body=body,
        footer=FOOTER_HTML,
    )


def main():
    if BLOG_DIR.exists():
        shutil.rmtree(BLOG_DIR)
    BLOG_DIR.mkdir(parents=True)

    posts = load_posts()

    (BLOG_DIR / "index.html").write_text(render_listing(posts), encoding="utf-8")
    for post in posts:
        (BLOG_DIR / f"{post['slug']}.html").write_text(render_post(post), encoding="utf-8")

    print(f"Generated {len(posts)} post(s) into /blog")


if __name__ == "__main__":
    main()
