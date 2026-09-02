# Phase 1 — Design plan

The site's visual language comes from remote sensing itself: a false-color-composite palette, a working EO swipe as the homepage hero (not a background image), and small monospace coordinate strings as a persistent map-like motif. Boldness spends in the swipe hero; everything else stays quiet.

## Signature

**A live Earth observation swipe as the homepage hero.** Two aligned Sentinel-2 tiles of the same AOI under two renderings (true color vs a model output, or before/after a wildfire), with a draggable divider. It sits in its own column adjacent to the positioning line — not behind it — so it is a working artifact, not decoration. The site opens by demonstrating.

Carried across every page as the site's quiet secondary motif: a small IBM Plex Mono coordinate string near the header. Homepage shows a personal centroid, project pages show the AOI centroid, writing pages omit it (absence signals category). Makes the whole site read like a chart without ever looking like a map skin.

## Palette

Rooted in a Sentinel-2 NIR-R-G false-color composite plus SAR grayscale — the actual visual output of the work.

- `#0A1520` **Abyss** — dark base; deep-water tone in false color
- `#F1EDE4` **Salt** — light base; warm off-white shifted deliberately off "cream" to avoid the editorial-serif cliché
- `#D63384` **NIR Magenta** — the accent and the site's shout. Vegetation signal in NIR-R-G composites. Used for the swipe divider, hover on the featured artifact, and one word in the positioning line — nowhere else
- `#1E7B7B` **Shoal Teal** — shallow-water tone. Tag chips, link underlines, minimap fills
- `#2A2F3A` **Iron** — mid-tone text on light, subtle divider on dark; references SAR grayscale

Dark mode inverts base/text; the two accents hold their values on both grounds.

## Type

- **Display: Bricolage Grotesque (variable)** — quirky terminals and a grade axis give the site character at hero scale, then tightens down cleanly for section labels. Not Inter, not Space Grotesk, not a serif.
- **Body: Inter Tight** — quiet, gets out of the way while Bricolage carries the character.
- **Mono: IBM Plex Mono** — coordinates, publication metadata, tag chips, DOI/arXiv IDs, dates, figure captions. The site's "chart caption" voice, not a code-block-only utility.

Restraint rule: Bricolage only above 32px. Below that, body face.

## Layout — homepage

Two-column hero (left: mono coordinate, positioning line, current-focus line; right: the live swipe). Below: three horizontal project cards with thumbnail + AOI minimap chip + artifact icons + one-sentence summary. Then a compact recent-writing list. Then a quiet footer strip.

```
┌───────────────────────────────────────────────────────────────┐
│ MOHAMED AHMED        work · writing · research · about · cv   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  49.28° N, 123.12° W                    ┌───────────────────┐ │
│                                         │  ▓▓▓▓▒▒░│░░▒▒▓▓  │ │
│  Lead Data Scientist working on         │  ▓▓▒▒░░ │  ░▒▒▓  │ │
│  agentic systems for Earth              │  ▒▒░░   ◀▶  ░▒▓  │ │
│  observation. GeoAI models              │  ░░       │    ▒  │ │
│  that ship, not slides.                 │  before  drag after│
│                                         └───────────────────┘ │
│  Currently: {{TODO focus line}}          Sentinel-2 · YYYY-MM │
├───────────────────────────────────────────────────────────────┤
│  SELECTED WORK                                                │
│  ┌─────────────┐  Project 1 title                             │
│  │ [thumbnail] │  One-sentence what it does.                  │
│  │  [minimap]  │  paper · repo · demo · storymap              │
│  └─────────────┘  geoai · foundation-models                   │
│                                                               │
│  ┌─────────────┐  Project 2 title …                           │
├───────────────────────────────────────────────────────────────┤
│  RECENT WRITING                                               │
│  YYYY-MM-DD  Post title one …                                 │
│  YYYY-MM-DD  Post title two …                                 │
├───────────────────────────────────────────────────────────────┤
│  Contact · GitHub · Scholar · ORCID · RSS                     │
└───────────────────────────────────────────────────────────────┘
```

## Layout — project detail

Two-column with a sticky right rail. Left: title, one-sentence summary, artifact hero (StoryMap click-to-load / demo island / SpaceEmbed depending on primary artifact), long-form MDX writeup with embedded islands. Right rail: status, date, AOI minimap, artifact links, tags. Rail collapses above content on mobile.

```
┌───────────────────────────────────────────────────────────────┐
│ ← work                                                        │
├───────────────────────────────────────────────────────────────┤
│  Project title                          ┌────────────────┐    │
│  One-sentence summary.                  │  status: live  │    │
│                                         │  YYYY-MM       │    │
│  ┌───────────────────────────────────┐  │                │    │
│  │      Artifact hero                │  │  AOI minimap   │    │
│  │      (StoryMap thumbnail w/ play, │  │  ┌──────────┐  │    │
│  │       or demo island, or          │  │  │ ▓▒░ vec  │  │    │
│  │       SpaceEmbed w/ preload)      │  │  └──────────┘  │    │
│  └───────────────────────────────────┘  │                │    │
│                                         │  ARTIFACTS     │    │
│  ## What it does                        │  → paper       │    │
│  MDX prose …                            │  → repo        │    │
│                                         │  → storymap    │    │
│  ## Approach                            │  → demo        │    │
│  MDX prose, embedded charts …           │                │    │
│                                         │  TAGS          │    │
│  ## What I'd do differently             │  geoai · …     │    │
├───────────────────────────────────────────────────────────────┤
│  Related work → next project card                             │
└───────────────────────────────────────────────────────────────┘
```

## Cliché checklist (explicitly avoided)

- Not cream + high-contrast serif + terracotta (Salt is cooler than cream, display is a sans, no terracotta).
- Not near-black + acid-green (Abyss with NIR Magenta / Shoal Teal instead).
- Not broadsheet hairline rules + zero radius (soft 6–8px on cards; dividers reserved for the swipe handle).
- No `01 / 02 / 03` markers.
- No washed-out satellite image behind hero text. Satellite imagery appears only as working content: the swipe, project thumbnails, AOI minimaps.

## Judgement calls I'd flag

1. **The swipe hero is a client-side island** (~5–8KB gzipped vanilla JS, `client:visible`). Comfortably under the 50KB homepage budget, but it's the single largest JS line item on `/`.
2. **Bricolage Grotesque** is gaining popularity fast. Alternates if you'd rather something quieter: **General Sans** or **Uncut Sans**. Bricolage's grade axis is the reason I picked it.
3. **NIR Magenta as the shout color** is deliberately unusual — signals remote-sensing literacy to the field, reads as distinctive to outsiders. If it's too loud, alternates are **SWIR amber `#E58A2E`** or **Aurora green `#7BE0A6`**.
