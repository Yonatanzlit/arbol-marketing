#!/usr/bin/env python3
"""
Checks that every sentence of the client's supplied copy appears on the page
exactly as he wrote it. The client's Spanish is final — this is the guard that
stops a well-meaning edit from paraphrasing it.

Source of truth: tools/Base Web Arbol.docx  →  compared against index.html

  python3 tools/verify_copy.py
"""
import html as htmllib
import os
import re
import sys
import zipfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
DOCX = os.path.join(ROOT, "tools", "Base Web Arbol.docx")
HTML = os.path.join(ROOT, "index.html")


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    out = []
    for p in paras:
        t = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
        out.append(htmllib.unescape(t))
    return out


def page_text(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<svg.*?</svg>", " ", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", htmllib.unescape(s)).strip()


def norm(s):
    # collapse whitespace only — accents, punctuation and wording must match
    return re.sub(r"\s+", " ", s).strip()


# The exact client strings that must survive to the page, verbatim.
REQUIRED = [
    "¡Conocé a Arbol Trade & Marketing!",
    "¡Hola! Somos Arbol Trade & Marketing, una empresa líder en el mercado de Servicios Corporativos y Trade Marketing.",
    "Con una amplia experiencia, ayudamos a nuestros clientes a mejorar sus ventas y aumentar su presencia en el mercado.",
    "¡Nos encantaría hacer lo mismo con tu Compañía!",
    "Brindamos un servicio personalizado, de calidad y con calidez.",
    "¡Te esperamos!",
    "Nuestra historia de crecimiento",
    "Como un árbol, crecemos y evolucionamos a lo largo de los años.",
    "Desde nuestros inicios, hemos acompañado a nuestros clientes en su camino hacia el éxito.",
    "Logramos echar raíces, prosperar, dar cobertura y frutos con nuestras acciones.",
    "Hoy seguimos creciendo junto a ellos.",
    "Conocé más sobre nuestra historia y cómo podemos ayudar a tu negocio a crecer y prosperar.",
    "¿Qué ofrecemos?",
    "Servicios de Marketing, Trade, BTL, campañas y eventos.",
    "Equipos de atención permanente para el PdeV",
    "¡Siempre estamos disponibles para ayudar a nuestros clientes a mejorar su servicio al canal!",
    "Brigadas para acciones puntuales",
    "¡Ayudamos a nuestros clientes a destacar en campañas específicas, rápidas y de gran alcance!",
    "Servicios de auditoría",
    "¡Brindamos una visión detallada del mercado para ayudar a tomar decisiones basadas en información!",
    "Mystery Shoppers",
    "¡Ayudamos a nuestros clientes a mejorar su servicio al cliente, evaluar sus KPI y validar la calidad de sus dinámicas!",
    "Servicio de Merchandising",
    "¡Gestión de Trade, Información, Activación, Seguimiento y presentación de productos en tiendas!",
    "Marketing visual",
    "¡Ayudamos a nuestros clientes a llamar la atención con activaciones impactantes!",
    "Logística",
    "¡Aseguramos que los Materiales Promocionales lleguen a tiempo y se instalen en perfectas condiciones!",
    "¿Por qué trabajar con nosotros?",
    "Ofrecemos una combinación única de tecnología avanzada, potencial de crecimiento y recursos humanos altamente capacitados.",
    "Además, nuestra experiencia en el mercado en varias categorías nos permite brindar un servicio de calidad a nuestros clientes.",
    "¡Nos encantaría ayudarte a alcanzar tus objetivos!",
    "¡Contactá con nosotros!",
    "¡Estamos ansiosos de conectarnos con vos!",
    "Nos encontrás en Ciudad de la Paz 2941 Piso 9° B, CABA, Argentina",
    "www.arbolmarketing.com",
    "gerencia@arbolmarketing.com",
    "¡No dudes en ponerte en contacto con nosotros para analizar juntos cómo podemos ayudar a crecer tu negocio!",
    # the three buttons, exact labels
    "Trabajá con Nosotros",
    "Acceso Clientes",
    "Quiero crecer con Arbol",
]

page = norm(page_text(HTML))
missing = [s for s in REQUIRED if norm(s) not in page]

# Cross-check: is every REQUIRED string actually traceable to the docx?
doc = norm(" ".join(docx_text(DOCX))) if os.path.exists(DOCX) else ""
unsourced = []
if doc:
    for s in REQUIRED:
        if norm(s) not in doc:
            unsourced.append(s)

print("client strings checked : %d" % len(REQUIRED))
print("missing from page      : %d" % len(missing))
for s in missing:
    print("   MISSING  %s" % s)
if doc:
    print("not found in docx      : %d  (expected: button labels, which the brief lists separately)" % len(unsourced))
    for s in unsourced:
        print("   UNSOURCED  %s" % s)

sys.exit(1 if missing else 0)
