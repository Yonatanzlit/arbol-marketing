# Arbol Trade & Marketing - Website Build Plan

## 1. What Gustavo asked for

Gustavo is launching a **new, standalone company**: Arbol Trade & Marketing, at **www.arbolmarketing.com**. This is not related to his other company or its site in any way — different brand, different domain, different audience. Nothing from that project is reused or referenced here.

**The brand.** The name comes from the word *árbol* (tree). The brand colours are **white and green**, and he told us exactly what each one means:

> "El color blanco simboliza la limpieza, lo que se alinea con nuestra misión de promover el crecimiento y la salud de las empresas. El color verde representa la naturaleza, recordándonos la importancia de la sostenibilidad y el crecimiento en todos los aspectos de la vida."

> "El blanco proporciona un borrón y cuenta nueva para el negocio, mientras que el verde simboliza el crecimiento y la prosperidad."

That is a design instruction, not decoration: **white dominates the page**, green is the ink and the line work.

**The life-cycle story.** He wrote: *"En Arbol, hablamos del ciclo de vida: desde la semilla, las raíces fuertes, el crecimiento, los frutos, la cobertura (sombra), la longevidad, el futuro, la reproducción (frutos, semillas, y más árboles)."*

**The scroll idea — his differentiator.** This is the single most specific thing in the brief:

> "Es por esto que nos imaginamos un sitio que (a diferencia de otros) escrolee desde abajo hacia arriba: o sea desde el piso (semilla, raíces) siguiendo por el tronco del árbol luego la copa del árbol, todo parte del logo de la agencia."

Two things follow. First, **"a diferencia de otros"** — being mechanically unlike other sites *is* the requirement. Second, **"todo parte del logo de la agencia"** — the tree you climb is his actual logo, not an illustration we invent.

**The logo.** *"El logo es dinámico y descontracturado, con líneas claras."* We have two lockups (horizontal and vertical), both as JPGs on white.

**The copy.** He supplied finished Spanish copy for five blocks: intro, historia, 8 services, why-us, and contact. That copy is final and ships as written.

**The three buttons.** *"Quisiera agregar 3 botones de contacto: 'Trabaja con Nosotros', 'Acceso Clientes' y 'Quiero crecer con Arbol'."* He calls all three **botones de contacto** — contact buttons. All three ship, all three at equal weight.

---

## 2. The core concept

### The decision

**We build the bottom-to-top scroll he asked for. Literally.** The page opens at ground level and the visitor travels upward through the tree to the canopy.

This was the one place the four expert reviews disagreed most — three of them recommended a conventional downward scroll with a "camera that pans up," on accessibility grounds. I am overruling that. The accessibility objections are real but they are **engineering constraints to solve, not grounds to delete the client's only stated design differentiator**. And there is a technique that satisfies both.

### How it works mechanically

The page uses a single scroll container with `flex-direction: column-reverse`.

That one property does something valuable: it **stacks the content bottom-to-top visually while leaving the HTML in narrative order**. So:

- **Semilla** is the first element in the HTML — and renders at the visual *bottom* of the page.
- The browser natively parks the scroll position at the flow's start edge, which is the visual bottom. **The page loads underground, at the seed. No JavaScript required.**
- The visitor scrolls **upward** to move forward through the story: semilla → raíces → tronco → copa.
- **HTML order = narrative order = keyboard tab order = screen-reader reading order.** No WCAG 1.3.2 or 2.4.3 failure, because nothing is visually reordered relative to what a screen reader announces — the whole *page* is flipped, not individual elements within a stable frame.
- Wheel, trackpad and keyboard all act on the same geometry, so they agree with each other. There is no inverted-input hack anywhere; we never touch `wheel` events, never use `transform: scaleY(-1)`, and never scroll-jack.

Three residual behaviours we handle explicitly: `history.scrollRestoration = 'manual'` plus a re-anchor on `pageshow` (including the bfcache `persisted` case) so reload and back-button land correctly; `overscroll-behavior-y: contain` so iOS rubber-banding doesn't fight the origin; and `100svh` (never `100vh`) on every pinned element so the iOS toolbar collapse doesn't shift the composition mid-scroll.

Two behaviours we accept and will tell Gustavo about in writing: **Ctrl+F / find-in-page scrolls in the conventional direction**, and a visitor who has already inverted scrolling at the OS level experiences the page conventionally. Neither breaks the site; both are cosmetic oddities on a one-page brochure.

### What the visitor experiences, start to finish

**Load.** White screen. The viewport sits at ground level. A wavy multi-stroke line — lifted directly from the logo — runs across the lower third of the screen; below it, a single seed and the first hairline root, drawn in green on white. The H1 and the intro paragraph sit above the ground line. A slim rail on the right edge is empty at the bottom. There is one filled green button: **"Quiero crecer con Arbol"**.

**They scroll up.** The world sinks past them. The root system draws itself outward and downward as it exits the bottom of the screen — SVG strokes animating `stroke-dashoffset` from 1 to 0 — while "Nuestra historia de crecimiento" and its paragraph rise into place. The rail on the right fills a little further from the bottom.

**They keep going.** The **double-line trunk** from the logo enters from the top of the viewport and runs floor-to-ceiling, drawing itself as it comes. This is the longest passage. Eight service cards hang off the trunk as branches, alternating left and right; each branch draws out from the trunk and its card fades and slides 16px into place. The trunk is continuous — it is one SVG, one shape, the whole way up.

**The canopy.** The tangled scribble crown of the logo enters from the top and **draws itself in**, ten to fourteen overlapping strokes in the logo's three greens, sequenced across roughly 60vh of travel. This is the visual climax and it sits behind "¿Por qué trabajar con nosotros?". Once complete, a very soft shadow settles beneath it — the *cobertura* the brief names.

**The top.** The camera stops. The canopy breathes almost imperceptibly (±0.4° over 9 seconds — the only ambient motion on the page, off under reduced-motion). The contact block sits under the canopy: the closing copy, the address, the email, and the three buttons.

**The payoff.** As the visitor reaches the top, the tree they just climbed settles and resolves into **the actual vertical logo lockup** — canopy, ground waves, then the wordmark. They realise they have just walked up through the logo. This is the sentence for Gustavo's email: *"todo parte del logo de la agencia" — literalmente.*

### What degrades, and to what

`column-reverse` is one CSS property. With CSS disabled, JavaScript off, or `prefers-reduced-motion: reduce` active, the page is a **plain, complete, conventional top-to-bottom document** in the client's copy order, with the tree drawn complete and static. Nothing is hidden by default; the animated state is the override. That is the baseline, not a fallback.

---

## 3. Design system

### Colours

Sampled from the logo files by decoding pixel values — not estimated.

| Token | Hex | Role |
|---|---|---|
| `--white` | `#FFFFFF` | Page background. The default everywhere. |
| `--mist` | `#F2F7EF` | Occasional section band. Max 3 on the page, never adjacent. |
| `--border` | `#DCE7D8` | Hairline rules, card outlines |
| `--ink` | `#14201A` | Body and heading text. A near-black darkened green, not a neutral grey — keeps the page white-and-green as instructed. 16.8:1 on white. |
| `--ink-2` | `#4A5A45` | Card body, secondary text. 7.4:1 |
| `--root` | `#0B4A12` | Deepest green. Footer band. 10.5:1 |
| `--brand` | `#00690C` | Primary green: buttons, links, wordmark. **6.94:1 on white** |
| `--brand-hov` | `#00520A` | Button hover |
| `--canopy` | `#375B29` | Olive. Eyebrows, dark scribble strokes. 7.8:1 |
| `--mid` | `#689F1E` | Mid wave strokes. **Decorative only** |
| `--leaf` | `#7CC01F` | Bright accent, underlines, icon highlights. **Decorative only** |

**Three hard rules, written as a comment in the CSS so they survive future edits:**
1. `--leaf` (#7CC01F) is **2.23:1** on white. Never text, never a link, never a focus ring.
2. `--mid` (#689F1E) is **3.20:1** on white. Decorative only, at any size.
3. **Focus rings and CTA button fills use `--brand` or darker.** Mid-green is the instinctive choice for a button and it fails.

**Whiteness budget:** ≥80% of any viewport is white or mist. Green is ink, line and one button — never a full-bleed wash except the footer band. Tree line art never sits behind running text; it lives in the margins and gutters, or it steps aside.

### Typography

**Display — Bodoni Moda.** The wordmark is a genuine Didone: extreme thick/thin contrast, unbracketed hairline serifs, vertical stress. Bodoni Moda is the closest free match. **Display sizes only** — its hairlines break down below ~34px.

**Text and UI — Jost.** "TRADE & MARKETING" is a light, monoline, wide-tracked geometric — Futura. Jost is a direct Futura interpretation and reproduces the tracked-caps treatment almost exactly at weight 300.

Two families. **Self-hosted as subsetted WOFF2**, not loaded from Google Fonts — a round trip to `fonts.gstatic.com` from Buenos Aires costs 300–500ms before a glyph renders, and the origin is in Argentina. Subset to Latin plus `áéíóúüñÁÉÍÓÚÜÑ¡¿`. The `¡` and `¿` are easy to forget and their absence is instantly visible in "¿Qué ofrecemos?".

| Token | Family | Desktop | Mobile | Use |
|---|---|---|---|---|
| eyebrow | Jost 500 | 13px, 0.18em, uppercase | 12px, 0.14em | Above every h2 — the direct logo echo |
| h1 | Bodoni Moda 600 | 64px / 1.08 | 38px / 1.15 | The intro heading |
| h2 | Bodoni Moda 600 | 44px / 1.15 | 30px / 1.2 | Section headings |
| h3 | Jost 500 | 22px / 1.3 | 20px | Service card titles (sans on purpose — keeps the serif rare) |
| body-lg | Jost 300 | 20px / 1.65 | 18px / 1.6 | Intro paragraphs |
| body | Jost 400 | 17px / 1.7 | 17px | Default. Spanish runs long; the 1.7 is not optional. |
| button | Jost 500 | 15px, 0.08em, uppercase | 15px | All three CTAs |

Max measure 68ch. Spacing on an 8px scale: `4 8 12 16 24 32 48 64 80 96 128`. Radii: 6/10/16px, buttons fully pill — echoing the logo's round line-caps and its complete absence of hard corners.

### The scribble / line language

The logo is one continuous line that tangles at the top and calms into waves at the bottom. We reuse the **construction logic**, not just the picture.

- **Wave dividers.** Every section boundary is a three-stroke wave echoing the logo's ground line, in `--leaf` / `--mid` / `--canopy` at 2.5 / 2 / 1.5px, inline SVG, full-bleed, `preserveAspectRatio="none"`. Control points shift ±8px per section so no two are identical — that is what makes them read as hand-drawn rather than a repeated asset.
- **Draw-on.** Every path carries `pathLength="1"` and animates `stroke-dasharray:1; stroke-dashoffset:1 → 0`. `pathLength` normalisation is the trick that makes this work regardless of a path's real length.
- **Service icons.** All eight drawn as **single continuous unbroken paths** — one line, never lifted — 40×40 viewBox, 1.75px stroke, round caps and joins, deliberate hand-wobble, no perfect circles. That construction rule is what ties them to the logo and is the cheapest way to look bespoke.

### Logo usage

| Placement | Lockup |
|---|---|
| Header | Horizontal, 168px wide |
| The page spine | The traced tree at **full strength** — roots, trunk, canopy — as the structural element the visitor climbs. Not a watermark. |
| Top of page | Vertical lockup, as the resolution payoff |
| Footer | Vertical, knocked out to white on `--root` |
| Favicon | Simplified single-loop tree (one canopy loop, one trunk stroke, one ground wave) — the full scribble is a green smudge at 16px. **New mark; show Gustavo before it goes live.** |
| OG image | 1200×630, vertical lockup centred on white, logo at 380px |

Clear space = the cap-height of the "A" on all four sides. Minimum 120px wide horizontal, 96px vertical. Never on a green fill without knocking out to solid white. Never re-tinted, rotated, or reproportioned.

**The JPG problem — this is the critical path.** Both lockups are JPGs on white. That fails even on a white page: JPEG ringing puts visible grey mosquito noise around every scribble line at header size, on a site whose entire premise is *limpieza*; there is no favicon path, no retina, no white knockout, and — decisively — **no draw-on animation**, because a raster has no strokes.

Route, in order:
- **A. Get the vector from Gustavo** (`.ai`, `.eps`, `.pdf`, `.svg`). Someone drew this in Illustrator; the file almost certainly exists. Then 1–2 hours in Inkscape splitting it into named `#semilla / #raices / #tronco / #ramas / #copa / #frutos` groups. **This is the highest-leverage request in the project.**
- **B. If no vector: commission a designer redraw** (~$100–250, 2–4 hours). Spec: *"Redraw as clean SVG. Strokes must remain strokes, not outlined. Group into these six named layers. Single colour, `currentColor`-friendly."*

**Auto-tracing with potrace is not a route.** It converts strokes into filled outlines, which makes `stroke-dashoffset` animation impossible, and produces a multi-hundred-KB SVG that is slower than the JPG. And **we do not substitute a tree of our own invention** — the brief says the journey is *"todo parte del logo de la agencia"*, so the tree must be his.

### Looking good with zero photography

There is no photography, no team imagery, no client logos and no case studies, and we invent none. The brand's asset is a line system, so this is survivable. What carries it, in order: **scale contrast in type** (64px Bodoni against 17px Jost is itself the visual — most photo-free sites fail because everything is one size); the **full-strength traced tree** as the page spine; the **eight single-line icons**; the **wave dividers**; and **density discipline** — never centre long paragraphs, cap every measure at 68ch, use asymmetric 5/7 splits so white space reads as composed rather than left over, and keep vertical rhythm strictly on the 8px scale.

Borders, not shadows. Cards at rest carry a 1px `--border` and no shadow; on hover they gain a soft shadow and lift 2px. Nothing else on the page casts a shadow.

---

## 4. Page structure

Sections are listed in **narrative order** — which is HTML order. Visually, §1 sits at the bottom of the page and §5 at the top.

**Copy rule for the whole build:** the client's copy ships **complete and unedited**. The source document had every accent and tilde stripped by the export (`anos`, `campanas`, `atencion`, `logistica`), so we restore diacritics on ordinary Spanish words and add the opening `¿` and `¡` that Spanish orthography requires. **We do not re-conjugate his verbs** — "Conoce", "Contacta" and "Trabaja" ship as he wrote them — and **we do not accent the brand name**: it ships as **Arbol**, matching his logo (which typesets ARBOL) and his domain. Both of those are questions for him, in §8, not decisions for us. The accent restoration goes to him as a one-page diff for approval, and we build in parallel — it does not block anything.

---

### §1 — Semilla · the ground *(visual bottom of the page; where the visitor lands)*

**Heading:** `¡Conoce a Arbol Trade & Marketing!`

**Copy, complete:**
> `¡Hola! Somos Arbol Trade & Marketing, una empresa líder en el mercado de Servicios Corporativos y Trade Marketing. Con una amplia experiencia, ayudamos a nuestros clientes a mejorar sus ventas y aumentar su presencia en el mercado. ¡Nos encantaría hacer lo mismo con tu Compañía! Brindamos un servicio personalizado, de calidad y con calidez. ¡Te esperamos!`

All five sentences ship. If it doesn't fit one viewport, it splits across scroll beats — no word is dropped.

**Life-cycle stage:** semilla.

**Looks like:** white. The logo's wavy ground line across the lower third. Below it, a seed and one hairline root in `--brand`. H1 in Bodoni, paragraph at body-lg, `--ink`. One filled button: **"Quiero crecer con Arbol"**.

**Animates:** on load, the ground wave draws left to right; the seed fades in. Scrolling up, the seed cracks and the root system draws downward as it exits the bottom of the viewport.

---

### §2 — Raíces fuertes

**Heading:** `Nuestra historia de crecimiento`

**Copy, complete:**
> `Como un árbol, crecemos y evolucionamos a lo largo de los años. Desde nuestros inicios, hemos acompañado a nuestros clientes en su camino hacia el éxito. Logramos echar raíces, prosperar, dar cobertura y frutos con nuestras acciones. Hoy seguimos creciendo junto a ellos. Conoce más sobre nuestra historia y cómo podemos ayudar a tu negocio a crecer y prosperar.`

All five sentences. Staging them across scroll beats is fine; deleting any is not. The closing sentence reads as a CTA — at launch it renders as prose with no link, because there is no history page and we will not fabricate one. Question 5 in §8 asks him where he wants it to go.

**Stage:** raíces fuertes.

**Looks like:** root scribbles spreading laterally into the left and right gutters, never behind the text.

**Animates:** roots draw outward, staggered, as the section enters.

---

### §3 — Tronco / crecimiento · the services

**Heading:** `¿Qué ofrecemos?`

**Stage:** crecimiento (the client's word).

**Looks like:** the trunk runs floor-to-ceiling, centred on desktop. Eight cards alternate left and right as branches. **On mobile the trunk moves to `left: 24px`**, branches become 24px stubs and cards go full-width to its right — same SVG, different viewBox via media query, no second asset.

**Animates:** the trunk draws upward continuously; each branch draws out from it, and its card fades and translates 16px into place. **The cards are real, focusable, selectable HTML in order 1→8** — animation only touches `opacity` and `transform`. Someone scrolling fast sees eight cards in a normal stack, never an empty screen.

The eight, verbatim:

1. **`Servicios de Marketing, Trade, BTL, campañas y eventos.`** — *Icon: the whole canopy.* A dense scribble of overlapping loose loops with four short rays leaving it, each ending in a leaf-tick. **Note:** this item alone has no descriptor line and ends in a period rather than an exclamation. It renders as a **name-only card**, the title vertically centred against the icon, same height as its neighbours. We invent nothing. Question 3 asks him for a line.
2. **`Equipos de atención permanente para el PdeV: ¡Siempre estamos disponibles para ayudar a nuestros clientes a mejorar su servicio al canal!`** — *Two continuous-line figures at a wavy shelf, one dark green, one bright.*
3. **`Brigadas para acciones puntuales: ¡Ayudamos a nuestros clientes a destacar en campañas específicas, rápidas y de gran alcance!`** — *One unbroken zigzag, loose at the left and tightening into an arrowhead at the right, with two speed lines beneath.*
4. **`Servicios de auditoría: ¡Brindamos una visión detallada del mercado para ayudar a tomar decisiones basadas en información!`** — *A magnifier drawn as two-and-a-half loose loops that never close cleanly, plus a 45° handle in the same stroke; inside, three ascending bar-ticks traced by a small wave.*
5. **`Mystery Shoppers: ¡Ayudamos a nuestros clientes a mejorar su servicio al cliente, evaluar sus KPI y validar la calidad de sus dinámicas!`** — *A shopping bag in one continuous line whose handle arc closes into an almond eye with a scribbled iris.*
6. **`Servicio de Merchandising: ¡Gestión de Trade, Información, Activación, Seguimiento y presentación de productos en tiendas!`** — *Three stacked wavy shelf lines (direct lifts of the logo's ground waves); on the top wave, three box outlines, the centre one bright green and tilted 8°.*
7. **`Marketing visual: ¡Ayudamos a nuestros clientes a llamar la atención con activaciones impactantes!`** — *One continuous line starting as a tight spiral and unwinding into six uneven rays, over a thin panel outline rotated 30°.*
8. **`Logística: ¡Aseguramos que los Materiales Promocionales lleguen a tiempo y se instalen en perfectas condiciones!`** — *A side-view truck in one path, wheels as doubled scribble loops, sitting on the logo's ground wave which extends past the icon on both sides.*

Cap this stage at ~400vh desktop and validate on a real phone before sign-off — eight services is a lot of scroll and an over-long trunk kills the conversion at the top.

---

### §4 — Copa / frutos / cobertura

**Heading:** `¿Por qué trabajar con nosotros?`

**Copy, complete:**
> `Ofrecemos una combinación única de tecnología avanzada, potencial de crecimiento y recursos humanos altamente capacitados. Además, nuestra experiencia en el mercado en varias categorías nos permite brindar un servicio de calidad a nuestros clientes. ¡Nos encantaría ayudarte a alcanzar tus objetivos!`

It stays as one paragraph. We do **not** break it into four labelled differentiators — the client wrote prose, not a list.

**Stage:** frutos + cobertura (sombra).

**Looks like:** the canopy fills the upper viewport in the logo's three greens. Once complete, a soft radial shadow at ~8% settles beneath it, and the paragraph sits in that shade.

**Animates:** the canopy draws itself in — 10–14 overlapping strokes sequenced across ~60vh (35vh on mobile). This is the climax of the page.

---

### §5 — Longevidad / futuro / reproducción · Contacto *(visual top)*

**Heading:** `¡Contacta con nosotros!`

**Copy, complete, line breaks as he wrote them:**
> `¡Estamos ansiosos de conectarnos con vos!`
> `Nos encontrás en Ciudad de la Paz 2941 Piso 9 B, CABA, Argentina`
> `www.arbolmarketing.com o envianos un correo electrónico a gerencia@arbolmarketing.com .`
> `¡No dudes en ponerte en contacto con nosotros para analizar juntos cómo podemos ayudar a crecer tu negocio!`

The address ships with **his exact punctuation** — no comma inserted after 2941. It sits inside `<address>` with `font-style: normal`. The email is a `mailto:` link **and** visible selectable text, because a meaningful share of B2B desktop users have no mail handler configured. `www.arbolmarketing.com` renders as styled green text, not a link — linking a page to itself is a dead end.

**No contact form at launch.** He asked to be emailed at a stated address; that is what ships. A PHP form on this host carries real deliverability risk (SPF/DKIM, spam folders, silent failures on a lead-gen site). If he wants one, it is a scoped phase two with him specifying the fields.

**Stage:** longevidad / futuro / reproducción.

**Animates:** the canopy breathes (±0.4°, 9s, off under reduced-motion). Three seeds detach and drift down past the viewport — each one is a CTA arriving. Then the tree settles into the **vertical logo lockup** and the visitor sees the whole mark.

**The three CTAs.** All three appear here together, at full size, all three functioning as **contact buttons** exactly as he described them. None is greyed out, none is disabled, none is removed.

| Label (exact) | Weight | Action |
|---|---|---|
| `Quiero crecer con Arbol` | Primary — `--brand` fill, white text, pill. Also in the header, and as a sticky bottom bar on mobile after §1. | `mailto:gerencia@arbolmarketing.com?subject=Quiero%20crecer%20con%20Arbol` |
| `Trabaja con Nosotros` | Secondary — transparent, 1.5px `--brand` border, `--brand` text | `mailto:gerencia@arbolmarketing.com?subject=Trabaja%20con%20Nosotros` |
| `Acceso Clientes` | Tertiary — outline, same size | `mailto:gerencia@arbolmarketing.com?subject=Acceso%20Clientes` |

Subject lines only, **no prefilled body text** — we would be writing Spanish he hasn't approved, and "Trabaja con Nosotros" is genuinely ambiguous between recruitment and new business. Questions 6 and 7 resolve both; the `href` is a one-line change when they do.

All three are real `<a>` elements, minimum 44×44px, focus ring `3px solid var(--brand)` at 2px offset.

**Header:** logo left, one button right (`Quiero crecer con Arbol`). **No section nav** — his headings are questions, too long for a nav bar, and inventing five short labels means putting Spanish on his site that he never wrote. A slim right-edge progress rail that fills from the bottom gives orientation with zero copy; it is `aria-hidden` and hidden below 1100px.

**Footer:** vertical logo knocked out white on `--root`, address, email, and a **"Reducir animación"** toggle (see §5).

---

## 5. Technical approach

**Stack: plain static HTML/CSS/JS. No framework, no build step, no bundler, no npm dependency in the shipped site.**

Stripped of poetry, the animation is one number between 0 and 1 fanned out to CSS custom properties driving `transform`, `opacity` and `stroke-dashoffset` on an inline SVG. That is 60–100 lines of JavaScript. React solves problems this page does not have. **GSAP is also declined** — ~28KB for behaviour we write in under 3KB, and it is an opaque box to a non-developer maintainer: when Gustavo asks "make the tree appear a bit later," the answer should be editing a named CSS variable, not a ScrollTrigger config. If Phase 3 proves the hand-rolled version janky on a real mid-range Android after honest optimisation, GSAP becomes a deliberate scoped decision then.

**File structure** (`/Users/yonatanzlit/arbol-marketing`) — what you edit is what ships, no `src/` vs `dist/`:

```
index.html          # the site. Inline critical CSS + inline tree SVG + inline icons
404.html            # branded, minimal
styles.css          # ≤12KB. Loaded with ?v=N cache-bust
script.js           # ~100 lines, zero dependencies
.htaccess           # production Apache config (§7)
robots.txt  sitemap.xml  site.webmanifest  .nojekyll
assets/logo/  assets/tree/  assets/icons/  assets/fonts/  assets/og/  assets/favicon/
tools/              # dev only, never uploaded — deploy, backup, asset generation, screenshot sheet
server-backup-2026-07-XX/   # the live server as we found it. Committed. Sacred.
DEPLOY.md  CONTENIDO.md  README.md
```

`CONTENIDO.md` holds all site copy as plain Markdown so Gustavo can propose edits without touching HTML.

**Path discipline:** staging serves at a GitHub Pages subpath, production at the domain root. **Every internal path is relative** (`assets/logo/...`), never root-absolute. The deploy script greps for `src="/` and `href="/` and refuses to upload if it finds any. The only absolutes are `og:image` and `canonical`.

**Three-tier progressive enhancement.** Tier 0 (no JS, no modern CSS): a complete, readable, correctly-styled Spanish page with every word present — this is the baseline, not a fallback. Tier 1 (JS): one `IntersectionObserver` for reveals plus one `rAF`-throttled passive scroll listener writing `--progress` to `:root`. Tier 2, gated behind `@supports (animation-timeline: scroll())`: the same visual result running off the main thread on the compositor. Tiers 1 and 2 produce the same end state, so dropping from 2 to 1 looks less smooth, never broken.

**Performance.** Origin is in Argentina (Dattatec) with no CDN, so TTFB is the weak link and **request count matters more than usual** — we inline aggressively. Budget: index.html ≤30KB, styles.css ≤12KB, script.js ≤8KB, fonts ≤30KB, **total ≤400KB and ≤15 requests**. Targets on throttled Slow 4G + 4× CPU: LCP ≤2.0s, CLS <0.02, INP <150ms. Lighthouse ≥95 performance, **100 accessibility (non-negotiable)**, 100 best-practices, 100 SEO.

Animate `transform` and `opacity` only — never `top`, `height`, `width` or SVG geometry attributes. `content-visibility: auto` on off-screen sections. `will-change` on at most two elements, removed when out of view. No `backdrop-filter`, no SVG filters on anything that moves.

**Accessibility.**
- HTML order = visual order = focus order = reading order, guaranteed by the `column-reverse` approach.
- **The invisible-focus bug** is the #1 real defect in scroll-reveal sites: an element at `opacity: 0` is still focusable, so a keyboard user tabs into a link they cannot see. **We never hide interactive content** — text and links are always present and visible; motion applies to illustration and to subtle translates that never drop below `opacity: 0.15`.
- Reveal CSS defaults to **visible**; the animation is the override. Authored the other way round, reduced-motion and no-JS users get a blank page.
- `prefers-reduced-motion: reduce` ships in the same commit as the animation, showing the **complete** final state. Plus a visible **"Reducir animación"** toggle in the footer writing a `localStorage` flag — many users have never opened OS accessibility settings.
- Skip link `Saltar al contenido principal` as the first focusable element, landing on `<main id="contenido" tabindex="-1">`.
- Decorative tree: `aria-hidden="true" focusable="false"`. Logo SVG: `role="img"` with a `<title>`. Exactly one `<h1>`, `<h2>` per section, no skips. Services as a real `<ul>`. `<html lang="es-AR">`. All `alt` text in Spanish.
- Usable at 320px and 400% zoom with no horizontal scroll — scroll effects routinely break here.

*(Both the skip-link text and "Reducir animación" are Spanish we authored. They go in `CONTENIDO.md` for his approval alongside the 404 page and meta description.)*

**Browser support.** P0: Chrome Android, Safari iOS (current + 16/17), **Samsung Internet**. P1: Chrome/Safari desktop, Firefox. **The Samsung Internet trap:** its "Dark mode for websites" force-inverts pages and is on by default for many users, turning a white-and-green brand site into a black page with a magenta tree — invisible in all other testing. Mitigated with `<meta name="color-scheme" content="only light">` and verified by enabling the setting on a real device.

---

## 6. Build phases

Effort is focused working time; calendar time is longer because of review loops.

| # | Phase | Gustavo sees | Effort | Risk |
|---|---|---|---|---|
| **0** | **Access & assets.** Send the credentials/assets email (§8). Take the HTTP snapshot of the current placeholder. Create the repo and the GitHub Pages staging URL. | The email; a working staging URL with a skeleton | **2–3 h** | **Blocking but out of our control.** The vector logo may not exist. **We never wait on it — Phase 1 starts the same day.** |
| **1** | **Content & structure.** Full site, all copy in correct es-AR, semantic HTML, responsive, keyboard- and screen-reader-clean. **No animation.** Plus `CONTENIDO.md`. | Live staging URL he can read end to end | **1 day** | **Routine.** The only judgement call is the accent restoration — sent as a diff, not applied silently. |
| **2** | **Visual design.** Palette with the contrast rules, type scale, logo lockups, wave dividers, the eight icons, the three CTAs, contact block. | Same URL, now designed | **1–1.5 days** | **Low.** Risk is taste, not code. **Show two hero variants only** — an open-ended choice invites an unbounded revision loop. |
| **3** | **The bottom-to-top scroll.** Day 1 of this phase: a 20-second working prototype of ground→trunk on the real inverted mechanism, sent to him for a yes before we build the rest. Then the full journey, with reduced-motion and keyboard correctness built in from the start. Delivered as a URL **plus a screen recording** — he will watch it on his phone. | The site, working | **2–3 days** | **⚠️ THE RISKY PHASE.** Three risks: **(a)** the inverted mechanism failing real-device testing on iOS — mitigated by the day-1 prototype tested on an actual iPhone, not a simulator; **(b)** asset quality, entirely dependent on Phase 0's vector outcome; **(c)** performance on mid-range Android — profile from the first commit, not the end. If (a) genuinely fails on device, we report the failed test with the recording and agree a change with him — we do not pre-argue him out of it. |
| **4** | **Assets, performance, SEO.** Favicons, WhatsApp preview card, JSON-LD, Lighthouse scores in the README. | Correct preview when he shares the link | **0.5–1 day** | **Routine.** Only recurring surprise is WhatsApp's preview cache. |
| **5** | **Cutover prep.** `DEPLOY.md` written for a non-developer. **Read-only** full mirror of the live server the moment credentials arrive. Client signs off on staging. | The sign-off request | **0.5 day** | **Routine, but do not compress it.** Doing the read-only backup as a separate, earlier step than the deploy is what makes the deploy safe. |
| **6** | **Production cutover.** | www.arbolmarketing.com live | **0.5 day** | **Moderate, well-mitigated.** Three real hazards — redirect loop, 16KB truncation, charset mojibake — each with a specific countermeasure and a <60s rollback. |
| **7** | **Post-launch buffer.** | Fixes from real use | **0.5 day** | Budget it explicitly or it eats Phase 6. |

**Total: ~7–9 working days of effort. Calendar realistically 3–4 weeks**, dominated by credential turnaround and review cycles.

**Genuinely risky:** the inverted scroll on real iOS devices; whether the logo vector exists; the `.htaccess` HTTPS redirect; the silent FTPS truncation; animation performance on mid-range Android.

**Routine, should surprise nobody:** HTML/CSS/JS authoring, responsive layout, favicon generation, Lighthouse, the file upload itself, GitHub Pages staging.

---

## 7. Deployment

### What we verified about the server

`www.arbolmarketing.com` → `200.58.112.96`, reverse DNS `c240.dattaweb.com` — a Dattatec/Ferozo shared host in Argentina. Port 21 open (FTPS explicit), 22 filtered — **FTPS is the only upload channel**. Currently serving a 670-byte hand-written placeholder over HTTP/2 with valid TLS.

**Two findings that shape everything:**

1. **MX records for arbolmarketing.com point to the same box.** `gerencia@arbolmarketing.com` — the target of every button on the site — is a live mailbox there. **We do not touch DNS or nameservers under any circumstances.** The cutover is a file replacement over FTP, full stop. This also rules out any "just move it to Netlify/Cloudflare" shortcut.
2. **Apache on this host defaults to `charset=iso-8859-1`.** Without forcing UTF-8, every Spanish accent on the live site renders as garbage (`Conocé` → `ConocÃ©`) — an instant credibility failure with an Argentine audience, and one that will not appear in local testing.

### Staging

**GitHub Pages, public repo, `Yonatanzlit/arbol-marketing`** → `https://yonatanzlit.github.io/arbol-marketing/`. Chosen because Gustavo has already reviewed a GH Pages URL from Argentina before (zero new tooling to explain), `gh` is already authenticated, and it is **architecturally identical to production** — static files on a plain web server. What he approves is what ships.

Each section gets a stable anchor (`#s1`…`#s5`), listed in the review email, so he can say "en la sección 3, cambiar X". Ask him to open it **on his phone in Buenos Aires** — that single act is a free real-device, real-network, real-geography performance test.

Staging carries `<meta name="robots" content="noindex, nofollow">` with a loud comment, plus a canonical tag as a second layer. **The deploy script greps for `noindex` and aborts** if it is still present — with no build step there is no environment switching, so this guard is the only thing preventing a de-indexed launch.

### Production cutover

**Step 1 — Back up, three layers, in order.**
- **Layer 1, now, no credentials needed:** `curl` the live index.html, its headers and `web-en-construccion.jpg` into `server-backup-2026-07-21/`.
- **Layer 2, when credentials arrive:** a recursive read-only FTP mirror of the entire web root **before a single byte is written**. Use `LIST -a` — ProFTPD hides dotfiles from a plain `LIST`, and `.htaccess` is the single most important file to back up. Recurse into every directory: this client's other server on the same host family turned out to hold a full compromised WordPress behind an apparently simple front page. **Assume the directory contains more than the one file we can see.** Log every filename and byte count to a manifest.
- **Layer 3:** before overwriting, copy the originals into `_backup_20260721/` **on the remote host**. Layer 2 lives on a laptop; if someone is rolling back at 11pm, the recovery files must already be next to the live ones.

**And we never delete anything.** Add files, replace `index.html` and `.htaccess`, leave everything else exactly where it is.

**Step 2 — `.htaccess`.** Sets `AddDefaultCharset UTF-8` and `AddType "text/html; charset=UTF-8" .html` (the mojibake fix), `DirectoryIndex index.html index.htm index.php`, `Options -Indexes`, `RedirectMatch 404 ^/_backup_`, `ErrorDocument 404 /404.html`, `mod_deflate` for text types, one-year immutable caching for `/assets/` with `no-cache` on HTML, plus `X-Content-Type-Options` and `Referrer-Policy`.

**The HTTPS/www redirect ships as a separate, later upload.** On many Argentine shared hosts TLS terminates at a front-end proxy, so Apache sees `%{HTTPS}` as `off` even on HTTPS requests, producing an **infinite 301 loop** — and 301s are aggressively cached by browsers, so a loop that reaches real users is unusually painful to undo. Procedure: deploy with **no redirect block at all**, confirm the site works on both schemes, then add the block guarded by `RewriteCond %{HTTP:X-Forwarded-Proto} !https` and immediately verify with `curl -I` that `https://www.` returns 200 and not 301. This is the highest-risk single line in the whole deployment.

**Step 3 — Upload with Python `FTP_TLS`, never `curl`.** On this host class, curl FTPS uploads **silently truncate every file over 16KB to exactly 16384 bytes or to zero, and report success** — because curl does not reuse the control channel's TLS session on the data channel. `styles.css` and `index.html` will both exceed 16KB. The fix is an `FTP_TLS` subclass that passes `session=self.sock.session` when wrapping the data socket.

**Because the failure is silent, verification is mandatory, not optional.** After every file: compare `ftp.size(remote)` to the local size, then re-download and compare SHA-256. Print a final table of every file with local size, remote size and pass/fail. Any failure exits non-zero and **does not proceed to swap `.htaccess`**.

**Upload order:** all assets, CSS, JS and 404 **first**, verified — then `index.html` and `.htaccess` last. There is never a moment where a new index points at assets that haven't landed.

**Step 4 — Timing.** A weekday morning, **09:00–11:00 ART**. A full Argentine business day to catch problems, with Gustavo awake and reachable. Never Friday afternoon.

**Step 5 — Smoke test, 15 minutes, every item.** 200 with no redirect loop; `charset=utf-8` in the response; accented strings present in the HTML; CSS served compressed at full length; OG image reachable; a bad URL returns our 404; **zero occurrences of `noindex`**; `dig MX arbolmarketing.com` **unchanged**. Then manually: load on a real phone, click all three CTAs and confirm the mail client opens with the right recipient, share the URL to yourself on **WhatsApp** and check the preview card (WhatsApp is the dominant sharing channel in Argentina and far pickier than Facebook), and re-run Lighthouse against production.

**Rollback.** Trigger decided in advance: site broken, mojibake, redirect loop or 500 — and not fixed within **10 minutes**. Then roll back and debug on staging. No troubleshooting on production past the 10-minute mark.

| Level | Action | Time |
|---|---|---|
| 0 | Re-upload `_backup_20260721/index.html` and `.htaccess` over the root. Because nothing was deleted, the placeholder returns immediately. | **<60s** |
| 1 | `deploy_to_arbol.py --rollback` — push the whole Layer-2 mirror back. | ~3 min |
| 2 | Restore from the host's own panel backup (retention confirmed before cutover). | 15–30 min |
| 3 | Rebuild from git. Nothing is unrecoverable. | ~10 min |

---

## 8. Open questions for Gustavo

Ready to send. Items 1, 2 and 8 are the ones that unblock the most work.

1. **¿Tenés el logo en vectorial (.ai, .eps, .pdf o .svg)?** Es el pedido más importante de todos. Con los JPG no podemos animar el árbol, ni hacer el favicon, ni que se vea nítido en pantallas retina. Si no existe el archivo original, ¿hay presupuesto para que un diseñador lo redibuje? Son unas 2 a 4 horas de trabajo.
2. **El documento nos llegó sin acentos ni eñes** (dice "campanas", "atencion", "anos", "logistica"). Vamos a escribirlo con la ortografía correcta y te mandamos el texto final para que lo apruebes de una sola vez. **¿La marca lleva tilde — "Árbol" o "Arbol"?** Por ahora la escribimos **sin** tilde, igual que tu logo y que el dominio.
3. **El primer servicio no tiene descripción como los otros siete.** ¿Nos mandás una frase, o lo dejamos solo con el nombre? Hoy lo dejamos solo con el nombre — no inventamos texto.
4. **¿Tus títulos van en voseo o en tuteo?** Tu texto mezcla los dos: el cuerpo usa voseo ("conectarnos con vos", "Nos encontrás") pero los títulos usan tuteo ("Conoce", "Contacta", "Trabaja"). Por ahora respetamos exactamente lo que escribiste. Si querés unificar todo en voseo ("Conocé", "Contactá", "Trabajá con Nosotros"), decinos y lo cambiamos.
5. **"Conoce más sobre nuestra historia": ¿a dónde debería llevar?** Hoy no hay página de historia, así que lo dejamos como texto.
6. **¿"Trabaja con Nosotros" es para postulaciones de empleo o para clientes nuevos?** Y si es para empleo, ¿los CV van a `gerencia@` o hay otra casilla?
7. **¿"Acceso Clientes" tiene que llevar a algún sistema que ya exista** (un reporte, un Power BI, un Drive)? Si existe, lo enlazamos ya. Por ahora los tres botones abren un correo a `gerencia@arbolmarketing.com` con un asunto distinto cada uno.
8. **Datos de acceso al hosting de arbolmarketing.com:** usuario y contraseña del panel (Ferozo / DonWeb), o los datos de FTP (servidor, usuario, contraseña — puerto 21, FTPS explícito). Y confirmarnos cuál es la carpeta raíz del sitio.
9. **¿El hosting tiene backups automáticos? ¿De cuántos días?** Lo necesitamos saber antes de tocar nada.
10. **Confirmanos que `gerencia@arbolmarketing.com` funciona y que alguien lo revisa.** Importante: el correo de `@arbolmarketing.com` está en el **mismo servidor** que la web, así que **no vamos a tocar los DNS bajo ningún concepto** — solo reemplazamos los archivos del sitio.
11. **¿Tenemos fotos del equipo, de acciones en punto de venta, o logos de clientes que podamos mostrar?** Hoy no hay ninguna imagen más allá del logo. Se puede lanzar igual y el diseño está pensado para eso, pero conseguir material lleva semanas — por eso preguntamos ahora.
12. **¿Hay teléfono, WhatsApp o redes sociales (LinkedIn, Instagram)** que quieras sumar? Tu texto solo menciona la dirección y el correo.
13. **¿Confirmás la dirección tal cual va a figurar?** La ponemos exactamente como la escribiste: `Ciudad de la Paz 2941 Piso 9 B, CABA, Argentina`. ¿Querés que sumemos un enlace a Google Maps?
14. **¿Querés formulario de contacto, o alcanza con el correo?** Arrancamos solo con el correo; un formulario en este servidor tiene riesgo de caer en spam.
15. **¿El sitio va solo en español, o vas a necesitar versión en inglés?**
16. **¿Hay fecha objetivo de lanzamiento?** Preferimos hacer el cambio a producción un día hábil entre las 9 y las 11 de la mañana.

---

## 9. Risks and how we handle them

**The logo is only available as JPG. This is the critical path.** Nothing visual is final until the tree exists as named, stroke-based SVG layers. Auto-tracing does not solve it — it converts strokes to filled outlines, which kills the draw-on animation entirely, and produces a file larger than the source. *Handling:* Route A (ask for the vector) goes out in the first email; Route B (a $100–250 designer redraw) is the fallback and we decide between them before Phase 3 starts, not during it. We do **not** substitute a tree of our own invention — the brief says the journey is *"todo parte del logo de la agencia"*.

**The inverted scroll may misbehave on real iOS.** We are building what he asked for, which means we own the hardest part of it. *Handling:* the mechanism is prototyped and tested on a physical iPhone on **day 1 of Phase 3**, before the rest is built on top of it — not simulator-tested, because the toolbar-collapse behaviour that breaks these effects does not reproduce in a simulator. If it genuinely fails, we send him the recording of the failed test and agree a change together. We do not argue him out of his idea in advance.

**Spanish accents render as garbage on the live server.** Confirmed: this Apache defaults to ISO-8859-1. *Handling:* UTF-8 forced twice — `.htaccess` and meta tag — and verified with a `curl | grep` against the production URL in the smoke test.

**FTPS uploads truncate silently at 16KB.** The upload reports success and the site is broken. *Handling:* Python `FTP_TLS` with data-channel session reuse, plus mandatory size and SHA-256 verification on every file, with a hard abort before `.htaccess` is swapped.

**The HTTPS redirect can cause an infinite, browser-cached 301 loop.** *Handling:* deploy with no redirect at all, verify, then add it as its own upload guarded by `X-Forwarded-Proto` and immediately test with curl. Rollback in under 60 seconds if it loops.

**Touching DNS would silently kill the client's corporate email.** *Handling:* the cutover is file-only. This is stated explicitly in the email to Gustavo so nobody else changes it either.

**Bright brand greens fail contrast.** `#7CC01F` is 2.23:1 on white and `#689F1E` is 3.20:1 — and mid-green is the instinctive choice for a CTA button. *Handling:* the two rules are written as a comment in the CSS, and axe DevTools runs in Phase 4.

**Scroll-reveal creates invisible keyboard focus targets** — a WCAG failure Lighthouse does not detect. *Handling:* we never hide interactive content, and a full tab-through of the page is recorded as a screen capture in testing.

**Samsung Internet force-inverts the page** for many Argentine Android users by default, turning a white-and-green site black with a magenta tree — invisible in all other testing. *Handling:* `color-scheme: only light`, verified by enabling the setting on a real device.

**Eight services is a lot of scroll.** An over-long trunk makes the middle of the page tedious and drops conversion at exactly the point the CTAs live. *Handling:* the stage is capped at ~400vh desktop and validated on a real phone before sign-off.

**The server may contain more than the placeholder we can see.** This client's other server on the same host family held a compromised WordPress behind a simple front page. *Handling:* full recursive mirror including dotfiles before any write, and we delete nothing, ever.

**There is no photography, no client logos, no case studies and no statistics** — and a services company with no evidence of its work is a conversion weakness. *Handling:* we invent none of it. The design carries the whole load on type scale, the tree and the line system, and it is complete as-is. The ask goes to Gustavo in Phase 0 because sourcing takes him weeks, and photo slots drop in later with fixed `aspect-ratio` so nothing reflows.

**Staging `noindex` leaking to production** would de-index the live site, and with no build step there is no environment switching to prevent it. *Handling:* a grep-and-abort guard in the deploy script, plus a canonical tag as a second layer.

**Scope creep on copy we author.** Skip link, motion toggle, 404 page, meta description and OG text are all Spanish we write, not Spanish he wrote. *Handling:* all of it goes into `CONTENIDO.md` for his approval before launch. Nothing client-facing ships in Spanish without him seeing it.