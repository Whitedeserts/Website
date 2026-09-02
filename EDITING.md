# Editing the Website

This site is maintained from the Astro source files in `src`, `content`, and `public`. Do not edit generated files in `dist`; `dist` is rebuilt by `npm run build` and deployed by GitHub Actions.

Use the editable content files instead:

- Homepage content: `content/home.json`
- Other simple pages: `content/pages/*.md`
- Layout, navigation, metadata, structured data, and shared styles: `src/layouts/SiteLayout.astro`
- Arctic gallery page: `src/pages/arctic-fieldwork.astro`
- Arctic gallery metadata: `src/data/arcticFieldwork.ts`
- Static production assets: `public/`

## Change the Homepage

1. Open `content/home.json`.
2. Change the text, links, or photo values.
3. Run this from `D:\Website`:

```powershell
npm run build
```

4. Refresh the local site:

```text
http://localhost:4321/
```

For automatic updates while you edit, keep this command running in a terminal:

```powershell
npm run dev
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

Copy the image into the matching `public/photo/` path so Astro includes it in the generated site.

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
npm run build
```

The Markdown supports headings, paragraphs, bullet lists, and links like `[label](/url)`.

## Deployment Checks

Before pushing deployment changes, run:

```powershell
npm run check
npm run lint
npm run build
```

The custom domain is configured from `public/CNAME` and should build to `dist/CNAME` with exactly `mohamedahmed.ca`.
