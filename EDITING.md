# Editing the Website

This folder currently contains the built static website in `dist`. The original Astro source folder is missing, so direct edits in `dist` are possible but hard to maintain.

Use the editable content files instead:

- Homepage content: `content/home.json`
- Other simple pages: `content/pages/*.md`
- Homepage updater: `scripts/apply-content.py`
- Built pages that get updated: `dist/index.html` and matching `dist/<page>/index.html` files

## Change the Homepage

1. Open `content/home.json`.
2. Change the text, links, or photo values.
3. Run this from `D:\Website`:

```powershell
py scripts/apply-content.py
```

4. Refresh the local site:

```text
http://localhost:4321/
```

For automatic updates while you edit, keep this command running in a terminal:

```powershell
py scripts/apply-content.py --watch
```

Then save `content/home.json` and refresh the browser page.

## Change the Photo

Put the new image anywhere in the website folder, then update these values in `content/home.json`:

```json
"photo": {
  "source": "Photo/your-new-photo.png",
  "publicPath": "/photo/your-new-photo.png",
  "alt": "Portrait of Mohamed Ahmed",
  "caption": "Lead Data Scientist & GeoAI Lead - Esri Canada"
}
```

The script copies the source image into `dist/photo` for you.

## Change Simple Pages

Edit these Markdown files:

- `content/pages/about.md`
- `content/pages/research.md`
- `content/pages/cv.md`
- `content/pages/work.md`
- `content/pages/writing.md`
- `content/pages/speaking.md`

Then run:

```powershell
py scripts/apply-content.py --pages
```

To update both the homepage and Markdown pages at once, run:

```powershell
py scripts/apply-content.py
```

The Markdown supports headings, paragraphs, bullet lists, and links like `[label](/url)`.

## Advanced Direct Edits

For pages that do not have Markdown files yet, edit their built files directly under `dist`.

For the clean long-term setup, restore or recreate the missing Astro `src` folder and edit the source files instead of `dist`.