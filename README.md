# Mohamed Ahmed - personal site

Astro 5 + Tailwind 4 static personal website for Mohamed Ahmed, PhD. The site
is built for GitHub Pages and the production custom domain
`https://mohamedahmed.ca`.

## Dev

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # static output to ./dist
npm run preview      # serve ./dist locally
npm run check        # astro + type check
npm run lint         # eslint
npm run format       # prettier --write
```

## Content

- Homepage content lives in `content/home.json` and renders through
  `src/pages/index.astro`.
- Main text pages live in `content/pages/*.md` and render through
  `src/pages/[slug].astro`.
- Writing has a dedicated page at `src/pages/writing.astro`.
- Arctic gallery metadata lives in `src/data/arcticFieldwork.ts`; image files
  are served from `public/arctic/`.
- Global layout, navigation, metadata, structured data, and shared CSS live in
  `src/layouts/SiteLayout.astro`.

## Deploy

Deployment is handled by GitHub Actions in `.github/workflows/deploy.yml`.

- Build command: `npm run build`
- Output directory: `dist`
- Node version: `22`
- GitHub Pages source: GitHub Actions
- Custom domain: `mohamedahmed.ca`

Set `SITE_URL` to the production origin before deploy. The sitemap and
canonical URLs read from it. For this site, the production origin is
`https://mohamedahmed.ca`. The deploy workflow already sets this value.

The custom domain file is `public/CNAME`, which is copied to `dist/CNAME` at
build time. `public/robots.txt` points crawlers to
`https://mohamedahmed.ca/sitemap.xml`.
