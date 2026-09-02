from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME_CONTENT = ROOT / "content" / "home.json"
HOME_HTML = ROOT / "dist" / "index.html"
PAGES_CONTENT = ROOT / "content" / "pages"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Could not update {label}. Pattern matched {count} times.")
    return updated


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def inline_markdown(text: str) -> str:
    escaped = esc(text)
    return re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: f'<a href="{esc(match.group(2))}" class="text-shoal hover:text-nir underline underline-offset-2 transition-colors">{match.group(1)}</a>',
        escaped,
    )


def markdown_to_html(markdown: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(
                '<p class="text-iron/85 dark:text-salt/85 mt-5 max-w-prose text-base leading-relaxed">'
                + inline_markdown(" ".join(paragraph))
                + "</p>"
            )
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            blocks.append(
                '<ul class="text-iron/85 dark:text-salt/85 mt-5 list-disc space-y-2 pl-5 text-base leading-relaxed">'
                + "".join(f"<li>{inline_markdown(item)}</li>" for item in list_items)
                + "</ul>"
            )
            list_items.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            flush_list()
            continue
        if line.startswith("# "):
            flush_paragraph()
            flush_list()
            blocks.append(
                '<h1 class="font-display mt-4 text-4xl leading-[1.05] tracking-tight md:text-5xl">'
                + inline_markdown(line[2:].strip())
                + "</h1>"
            )
        elif line.startswith("## "):
            flush_paragraph()
            flush_list()
            blocks.append(
                '<h2 class="text-iron/70 dark:text-salt/60 mt-16 mb-4 font-mono text-xs tracking-widest uppercase">'
                + inline_markdown(line[3:].strip())
                + "</h2>"
            )
        elif line.startswith("### "):
            flush_paragraph()
            flush_list()
            blocks.append(
                '<h3 class="font-display mt-8 text-xl leading-tight tracking-tight">'
                + inline_markdown(line[4:].strip())
                + "</h3>"
            )
        elif line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
        else:
            flush_list()
            paragraph.append(line)

    flush_paragraph()
    flush_list()
    return " ".join(blocks)


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def first_paragraph(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            if lines:
                break
            continue
        lines.append(stripped)
    return " ".join(lines)[:220] or "Personal website page."


def copy_photo(content: dict) -> None:
    photo = content.get("photo", {})
    source = ROOT / photo.get("source", "")
    public_path = photo.get("publicPath", "")
    if not source.exists() or not public_path.startswith("/"):
        return

    destination = ROOT / "dist" / public_path.lstrip("/")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_resume() -> None:
    source = ROOT / "Resume" / "Mohamed_Ahmed_Resume.pdf"
    if not source.exists():
        return
    destination = ROOT / "dist" / "Resume" / "Mohamed_Ahmed_Resume.pdf"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def render_links(links: list[dict]) -> str:
    items = []
    for link in links:
        items.append(f'<a href="{esc(link["url"])}">{esc(link["label"])}</a>')
    return '<div class="profile-links">' + "".join(items) + "</div>"


def render_featured_work(items: list[dict]) -> str:
    articles = []
    for item in items:
        tags = "".join(
            f'<li class="bg-shoal/10 text-shoal rounded-sm px-1.5 py-0.5">{esc(tag)}</li>'
            for tag in item.get("tags", [])
        )
        articles.append(
            '<article class="group border-iron/10 dark:border-salt/10 border-t pt-8">'
            f'<div class="text-iron/70 dark:text-salt/60 mb-2 font-mono text-xs">{esc(item.get("meta", ""))}</div>'
            f'<h3 class="font-display text-xl leading-tight tracking-tight md:text-2xl"><a href="{esc(item["url"])}" class="hover:text-nir transition-colors">{esc(item["title"])}</a></h3>'
            f'<p class="text-iron/80 dark:text-salt/80 mt-2 max-w-prose text-sm md:text-base">{esc(item["summary"])}</p>'
            f'<ul class="mt-4 flex flex-wrap gap-1.5 font-mono text-[0.6875rem]">{tags}</ul>'
            '</article>'
        )
    return "".join(articles)


def render_recent_writing(items: list[dict]) -> str:
    rows = []
    for item in items:
        rows.append(
            '<li>'
            f'<a href="{esc(item["url"])}" class="group flex flex-col gap-1 py-4 md:flex-row md:items-baseline md:gap-8">'
            f'<time class="text-iron/70 dark:text-salt/60 font-mono text-xs md:w-32" datetime="{esc(item["date"])}">{esc(item["date"])}</time>'
            f'<span class="group-hover:text-nir text-base transition-colors">{esc(item["label"])}</span>'
            '</a></li>'
        )
    return "".join(rows)


def render_footer_links(items: list[dict]) -> str:
    return "".join(
        f'<li> <a href="{esc(item["url"])}" class="hover:text-nir"> {esc(item["label"])} </a> </li>'
        for item in items
    )


def update_footer_links(content: dict) -> None:
    links = content.get("footerLinks", [])
    if not links:
        return
    rendered_links = render_footer_links(links)
    for html_path in sorted((ROOT / "dist").glob("**/index.html")):
        html_text = html_path.read_text(encoding="utf-8")
        updated, count = re.subn(
            r'(<footer class="border-iron/10 dark:border-salt/10 mt-16 border-t">.*?<ul class="flex gap-4">).*?(</ul> </div> </footer>)',
            rf'\1{rendered_links}\2',
            html_text,
            count=1,
            flags=re.S,
        )
        if count == 1:
            html_path.write_text(updated, encoding="utf-8")


def update_home(content: dict) -> None:
    html_text = HOME_HTML.read_text(encoding="utf-8")
    photo = content.get("photo", {})
    details = content.get("details", {})

    html_text = replace_once(
        html_text,
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{esc(content["metaDescription"])}">',
        "home meta description",
    )
    html_text = replace_once(
        html_text,
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{esc(content["socialTitle"])}">',
        "home Open Graph title",
    )
    html_text = replace_once(
        html_text,
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{esc(content["socialDescription"])}">',
        "home Open Graph description",
    )
    html_text = replace_once(
        html_text,
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="https://mohamedahmed.example{esc(photo["publicPath"])}">',
        "home Open Graph image",
    )
    html_text = replace_once(
        html_text,
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{esc(content["socialTitle"])}">',
        "home Twitter title",
    )
    html_text = replace_once(
        html_text,
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{esc(content["socialDescription"])}">',
        "home Twitter description",
    )
    html_text = replace_once(
        html_text,
        r'<meta name="twitter:image" content="[^"]*">',
        f'<meta name="twitter:image" content="https://mohamedahmed.example{esc(photo["publicPath"])}">',
        "home Twitter image",
    )
    html_text = replace_once(
        html_text,
        r'<title>.*?</title>',
        f'<title>{esc(content["pageTitle"])}</title>',
        "home title",
    )
    html_text = replace_once(
        html_text,
        r'"description":"[^"]*"}</script>',
        f'"description":"{esc(content["metaDescription"])}"}}</script>',
        "home structured data description",
    )
    html_text = replace_once(
        html_text,
        r'"sameAs":\[.*?\],',
        '"sameAs":[],',
        "home structured data social links",
    )
    html_text = replace_once(
        html_text,
        r'(<div> <p class="text-iron/70 dark:text-salt/60 font-mono text-xs">).*?(</p> <h1)',
        rf'\1{esc(content["eyebrow"])}\2',
        "home eyebrow",
    )
    html_text = replace_once(
        html_text,
        r'(<h1 class="font-display[^>]*>).*?(</h1>)',
        rf'\1 {esc(content["name"])} \2',
        "home heading",
    )
    html_text = replace_once(
        html_text,
        r'(<p class="text-iron/80 dark:text-salt/80 mt-6 max-w-md text-base md:text-lg">).*?(</p> <dl)',
        rf'\1\n{esc(content["intro"])}\n\2',
        "home intro",
    )
    for key in ("role", "also", "now"):
        html_text = replace_once(
            html_text,
            rf'(<dt class="text-iron/70 dark:text-salt/60 w-16 shrink-0">{key}</dt> <dd>).*?(</dd>)',
            rf'\1{esc(details[key])}\2',
            f"home detail {key}",
        )
    html_text = replace_once(
        html_text,
        r'<div class="profile-links">.*?</div>',
        render_links(content.get("links", [])),
        "home profile links",
    )
    html_text = replace_once(
        html_text,
        r'(<figure class="swipe" role="group" aria-label=")[^"]*(" data-swipe)',
        rf'\1{esc(photo["alt"])}\2',
        "home figure label",
    )
    html_text = re.sub(
        r'src="/photo/[^"]*"',
        f'src="{esc(photo["publicPath"])}"',
        html_text,
    )
    html_text = replace_once(
        html_text,
        r'(<img class="swipe__base" src="[^"]*" alt=")[^"]*(")',
        rf'\1{esc(photo["alt"])}\2',
        "home photo alt text",
    )
    html_text = replace_once(
        html_text,
        r'(<figcaption class="swipe__caption"[^>]*>).*?(</figcaption>)',
        rf'\1{esc(photo["caption"])}\2',
        "home photo caption",
    )
    html_text = replace_once(
        html_text,
        r'(<section class="mx-auto max-w-6xl px-6 py-16"> <header class="mb-10 flex items-end justify-between gap-4"> <h2 class="text-iron/70 dark:text-salt/60 font-mono text-xs tracking-widest uppercase">\s*Selected work\s*</h2>.*?<div class="flex flex-col gap-10">).*?(</div>\s*(?:<p class="border-iron/10.*?</p>\s*)?</section> <section class="mx-auto max-w-6xl px-6 pt-4 pb-24">)',
        rf'\1{render_featured_work(content.get("featuredWork", []))}\2',
        "home featured work",
    )
    html_text = re.sub(r'<p class="border-iron/10 text-iron/50.*?\{\{TODO.*?</p>\s*', "", html_text, count=1, flags=re.S)
    html_text = replace_once(
        html_text,
        r'(<section class="mx-auto max-w-6xl px-6 pt-4 pb-24"> <header class="mb-8 flex items-end justify-between gap-4"> <h2 class="text-iron/70 dark:text-salt/60 font-mono text-xs tracking-widest uppercase">\s*Recent writing\s*</h2>.*?<ul class="divide-iron/10 dark:divide-salt/10 divide-y">).*?(</ul>\s*</section>)',
        rf'\1{render_recent_writing(content.get("recentWriting", []))}\2',
        "home recent writing",
    )

    HOME_HTML.write_text(html_text, encoding="utf-8")


def update_page(markdown_path: Path) -> None:
    slug = markdown_path.stem
    target = ROOT / "dist" / slug / "index.html"
    if not target.exists():
        raise RuntimeError(f"No built page exists for {slug}: {target}")

    markdown = markdown_path.read_text(encoding="utf-8")
    title = first_heading(markdown, slug.title())
    description = first_paragraph(markdown)
    page_html = markdown_to_html(markdown)

    html_text = target.read_text(encoding="utf-8")
    html_text = replace_once(
        html_text,
        r'<title>.*?</title>',
        f'<title>{esc(title)} - Mohamed Ahmed</title>',
        f"{slug} title",
    )
    html_text = replace_once(
        html_text,
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{esc(description)}">',
        f"{slug} meta description",
    )
    html_text = replace_once(
        html_text,
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{esc(title)} - Mohamed Ahmed">',
        f"{slug} Open Graph title",
    )
    html_text = replace_once(
        html_text,
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{esc(description)}">',
        f"{slug} Open Graph description",
    )
    html_text = replace_once(
        html_text,
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{esc(title)} - Mohamed Ahmed">',
        f"{slug} Twitter title",
    )
    html_text = replace_once(
        html_text,
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{esc(description)}">',
        f"{slug} Twitter description",
    )
    html_text = replace_once(
        html_text,
        r'<main id="main" class="flex-1">.*?</main>',
        '<main id="main" class="flex-1"> <section class="mx-auto max-w-3xl px-6 pt-12 pb-24 md:pt-20">'
        + page_html
        + "</section> </main>",
        f"{slug} page content",
    )
    target.write_text(html_text, encoding="utf-8")


def update_pages() -> None:
    if not PAGES_CONTENT.exists():
        return
    for markdown_path in sorted(PAGES_CONTENT.glob("*.md")):
        update_page(markdown_path)
        print(f"Updated dist\\{markdown_path.stem}\\index.html from {markdown_path.relative_to(ROOT)}")


def update_home_from_file() -> None:
    content = load_json(HOME_CONTENT)
    copy_photo(content)
    copy_resume()
    update_home(content)
    update_footer_links(content)
    print(f"Updated {HOME_HTML.relative_to(ROOT)} from {HOME_CONTENT.relative_to(ROOT)}")


def apply_all(include_pages: bool = True) -> None:
    if include_pages:
        update_pages()
    update_home_from_file()


def watched_files() -> list[Path]:
    files = [HOME_CONTENT]
    if PAGES_CONTENT.exists():
        files.extend(sorted(PAGES_CONTENT.glob("*.md")))
    return files


def snapshot_mtimes(files: list[Path]) -> dict[Path, float]:
    return {path: path.stat().st_mtime for path in files if path.exists()}


def watch() -> None:
    apply_all()
    files = watched_files()
    mtimes = snapshot_mtimes(files)
    print("Watching content files. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
            current_files = watched_files()
            current_mtimes = snapshot_mtimes(current_files)
            if current_mtimes != mtimes:
                try:
                    apply_all()
                    mtimes = current_mtimes
                except Exception as error:
                    print(f"Could not apply content: {error}")
    except KeyboardInterrupt:
        print("Stopped watching content files.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply editable content files to the built static website.")
    parser.add_argument("--home", action="store_true", help="Update only the homepage.")
    parser.add_argument("--pages", action="store_true", help="Update only Markdown pages in content/pages.")
    parser.add_argument("--watch", action="store_true", help="Keep running and update the built site whenever content files change.")
    args = parser.parse_args()

    if args.watch:
        watch()
        return

    if args.pages:
        update_pages()
        return

    apply_all(include_pages=not args.home)


if __name__ == "__main__":
    main()