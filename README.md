# Árbol Trade & Marketing — sitio web

One-page marketing site for **Árbol Trade & Marketing** (client: Gustavo),
`www.arbolmarketing.com`. Spanish (es-AR).

This is a **separate, standalone project** — unrelated to the Oxígeno Marketing
site. Nothing is shared between them except the client.

Plain static HTML/CSS/JS. **No build step, no framework, no npm.** What you edit
is what ships.

```
index.html      the whole site (inline tree SVG + inline service icons)
styles.css      design system + layout
script.js       ~150 lines, no dependencies, pure progressive enhancement
404.html        branded not-found page
.htaccess       production Apache config (charset, caching, compression)
assets/
  logo/         the client's two JPG lockups, untouched
  tree/         generated line-art fragments + preview
  fonts/        self-hosted Bodoni Moda + Jost (latin subset, 71 KB total)
  favicon/      favicon.svg + apple-touch-icon.png
tools/          dev-only helpers, never uploaded to the server
CONTENIDO.md    all site copy in plain language, for the client to approve
PLAN.md         the full build plan this was made from
```

## Running it locally

```sh
cd ~/arbol-marketing
python3 -m http.server 8899
open http://localhost:8899/
```

It must be served over HTTP, not opened as a `file://` URL — the self-hosted
fonts will not load otherwise.

## The one thing to understand: the scroll runs upward

The client asked for a site that *"escrolee desde abajo hacia arriba: o sea
desde el piso (semilla, raíces) siguiendo por el tronco del árbol luego la copa
del árbol"*.

That is built literally. The mechanism is a single CSS property on `.scroll`:

```css
flex-direction: column-reverse;
```

This stacks the sections bottom-to-top **visually** while leaving them in
narrative order in the HTML. Consequences worth knowing before you edit
anything:

- The page **opens at the seed**, at the visual bottom, with no JavaScript. The
  browser parks the scroll position at the flow's start edge, which the reversed
  direction puts at the bottom.
- **Scrolling up moves the visitor forward**: semilla → raíces → tronco → copa.
- **HTML order = reading order = tab order = screen-reader order.** Nothing is
  visually reordered relative to what assistive tech announces, so there is no
  WCAG 1.3.2 / 2.4.3 failure. The whole page is flipped, not individual elements.
- **Chrome reports `scrollTop` as negative** in this container. `script.js`
  measures the convention at startup rather than assuming it, and normalises
  everything through `progress()` (0 = at the seed, 1 = at the canopy). If you
  touch the scroll code, keep that.
- Sections in `index.html` are in narrative order: §1 semilla is first in the
  HTML and last on screen. **Do not reorder them to "fix" the layout.**

Two accepted quirks, worth telling the client: **Ctrl+F / find-in-page scrolls
in the conventional direction**, and a visitor who has already inverted
scrolling at the OS level experiences the page conventionally.

## The árbol drawing is a PLACEHOLDER

**This is the most important open item in the project.**

The client supplied the logo only as **JPG**. A raster image has no strokes, so
it cannot draw itself in — and the entire concept depends on the tree drawing
itself as you climb it.

So `tools/gen_tree.py` generates a scribble tree in the same construction
language as the logo (continuous tangled loops, calm waves at the ground). It is
**not the client's logo** and must be replaced before launch:

1. **Ask Gustavo for the vector** (`.ai`, `.eps`, `.pdf`, `.svg`). Someone drew
   this in Illustrator; the file almost certainly exists. Then split it into
   named groups (`#semilla #raices #tronco #ramas #copa`) and swap it in.
2. **If no vector exists:** commission a designer redraw (~2–4 h). Spec:
   *strokes must remain strokes, not outlined paths* — outlined paths cannot be
   animated with `stroke-dashoffset`.

**Auto-tracing is not a route.** potrace converts strokes into filled outlines,
which kills the draw-on animation and produces a file larger than the JPG.

The real logo lockups ship untouched as JPG in the header, the contact card and
the 404 page. Only the animated tree is generated.

The **favicon is also a new mark** (a simplified single-loop tree — the full
scribble is an unreadable green smudge at 16px). Show it to Gustavo before launch.

## Regenerating the artwork

```sh
python3 tools/gen_tree.py     # redraw the tree fragments (deterministic seed)
python3 tools/inline_tree.py  # splice them into index.html
```

These are one-time generators, not a build step — the paths are written straight
into `index.html`, and the committed `index.html` is what ships.

> Do **not** put `vector-effect="non-scaling-stroke"` back on the tree paths.
> It renders the stroke in device space while `pathLength` normalisation stays
> in user space, so the dash never covers the whole path and the draw-on
> animation visibly stops partway up the trunk.

## Checking your work

```sh
python3 tools/verify_copy.py                 # client's Spanish still verbatim?
python3 tools/shoot.py --w 1440 --h 900 --at s3 --final --out shots/x.png
python3 tools/shoot.py --w 390 --h 844 --at s1 --final --frame --out shots/m.png
```

`verify_copy.py` diffs the page against the client's original `.docx` and fails
if any of his 41 sentences have been altered. **Run it after any copy edit.**

`shoot.py` needs the local server running. Use `--frame` for anything below
500px wide: **headless Chrome silently clamps its own window to a 500px
minimum**, so a `--window-size=390` shot is really a 500px page cropped to 390
and will show phantom clipping that does not exist in a real phone.

## Colour rules that must not be broken

`--leaf` (#7CC01F) is **2.23:1** on white and `--mid` (#689F1E) is **3.20:1**.
Both are **decorative strokes only** — never text, never a link, never a focus
ring. Mid-green is the instinctive choice for a button and it fails WCAG.
Buttons, links and focus rings use `--brand` (#00690C, 6.94:1) or darker.

## Deployment

Not deployed yet. `www.arbolmarketing.com` currently serves an "En construcción"
placeholder on Apache, and **we do not have FTP credentials for it.**

Two hazards specific to this host, both documented in `PLAN.md` §7:

- **MX records point at the same box**, so `gerencia@arbolmarketing.com` lives on
  the web server. The cutover is a file replacement. **Never touch DNS.**
- **curl FTPS uploads silently truncate files over 16 KB** to exactly 16384 bytes
  and report success. Use a Python `FTP_TLS` subclass with data-channel TLS
  session reuse, and verify every upload by size and SHA-256.
