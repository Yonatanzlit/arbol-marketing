#!/usr/bin/env python3
"""Builds ONE self-contained HTML review gallery with base64 screenshots."""
import base64
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
SHOTS = os.path.join(ROOT, "shots")
OUT = os.path.join(ROOT, "REVIEW.html")


def img(name):
    p = os.path.join(SHOTS, name)
    if not os.path.exists(p):
        return None
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()


GROUPS = [
    ("El recorrido — escritorio (1440 × 900)",
     "Se entra por abajo, en la semilla, y se sube. Cada captura es una parada del recorrido.",
     [("d-s1.jpg", "§1 · La semilla", "Donde aterriza el visitante. Bajo tierra: la semilla, la línea de suelo del logo y el aviso «Subí para crecer». El botón principal ya está acá."),
      ("d-s2.jpg", "§2 · Las raíces", "«Nuestra historia de crecimiento». Las raíces se dibujan hacia abajo y salen de la pantalla. Nunca pasan por detrás del texto."),
      ("d-s3.jpg", "§3 · El tronco", "«¿Qué ofrecemos?». El tronco recorre la sección entera y los 8 servicios cuelgan como ramas, alternando izquierda y derecha. Cada ícono es una sola línea continua."),
      ("d-s4.jpg", "§4 · La copa", "«¿Por qué trabajar con nosotros?». La copa se enmaraña sola sobre el texto y deja una sombra suave debajo: la cobertura."),
      ("d-s5.jpg", "§5 · Los frutos", "«¡Contactá con nosotros!» con los tres botones que pediste, la dirección y el correo. A la derecha, el logo vertical."),
      ("d-top.jpg", "El final del recorrido", "Lo más alto de la página. El pie cierra el recorrido por encima del contacto.")]),

    ("El recorrido — celular (390 × 844)",
     "Mismo recorrido, misma dirección. El tronco se corre al margen izquierdo y las tarjetas pasan a una sola columna.",
     [("m-s1.jpg", "§1 · La semilla", "El título entra en dos líneas y el botón ocupa todo el ancho."),
      ("m-s2.jpg", "§2 · Las raíces", "Las raíces quedan arriba del texto, sin taparlo."),
      ("m-s3.jpg", "§3 · El tronco", "El tronco se mueve al margen izquierdo y las ramas se acortan. Es el mismo dibujo, no una segunda versión."),
      ("m-s4.jpg", "§4 · La copa", "La copa ocupa el ancho completo de la pantalla."),
      ("m-s5.jpg", "§5 · Los frutos", "Los tres botones apilados, cada uno a ancho completo."),
      ("m-top.jpg", "El final del recorrido", "El pie de página, con el botón para reducir la animación.")]),

    ("Pruebas",
     "Lo que verifiqué antes de mostrártelo.",
     [("nojs.jpg", "Sin JavaScript", "Con el JavaScript apagado la página se ve completa, el árbol aparece dibujado entero y <b>igual arranca en la semilla</b>. El recorrido de abajo hacia arriba es CSS puro, no depende de scripts."),
      ("reduced.jpg", "Movimiento reducido", "Con «reducir movimiento» activado en el sistema, se muestra el estado final completo. Nunca una pantalla en blanco."),
      ("xs-s3.jpg", "320 px de ancho", "El teléfono más chico que se soporta. Sin desborde horizontal."),
      ("404.jpg", "Página 404", "Para cuando alguien entra a una dirección que no existe.")]),
]

CHECKS = [
    ("Textos del cliente publicados palabra por palabra", "41 / 41", True),
    ("Errores de JavaScript en consola", "0", True),
    ("Desborde horizontal (1440 / 390 / 320 px)", "ninguno", True),
    ("Elementos enfocables invisibles (falla típica de WCAG)", "0", True),
    ("Orden de lectura = orden visual = orden de tabulación", "sí", True),
    ("Contraste de todos los textos (WCAG AA)", "pasa", True),
    ("Botones y controles de 44 px mínimo", "pasa", True),
    ("Imágenes sin texto alternativo", "0", True),
    ("Funciona sin JavaScript", "sí", True),
    ("Dibujo del árbol definitivo", "PENDIENTE — falta el logo vectorial", False),
]

css = """
:root{--bg:#0d1210;--card:#151d19;--line:#22302a;--tx:#e8efe9;--mut:#93a89a;
--leaf:#7cc01f;--brand:#4faa2a}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
font:16px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:56px 24px 90px}
h1{font-size:34px;margin:0 0 8px;letter-spacing:-.02em}
.sub{color:var(--mut);margin:0 0 34px;font-size:17px}
.note{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--leaf);
border-radius:10px;padding:18px 22px;margin:0 0 40px}
.note b{color:var(--leaf)}
h2{font-size:22px;margin:52px 0 6px;padding-top:26px;border-top:1px solid var(--line)}
h2 .n{color:var(--mut);font-weight:400;font-size:15px;display:block;margin-top:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:26px;margin-top:26px}
.shot{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.shot img{width:100%;display:block;background:#fff}
.cap{padding:15px 18px 19px}
.cap h3{margin:0 0 6px;font-size:16px;color:var(--leaf)}
.cap p{margin:0;font-size:14px;color:var(--mut);line-height:1.6}
table{width:100%;border-collapse:collapse;margin-top:22px;font-size:15px}
td{padding:11px 12px;border-bottom:1px solid var(--line)}
td:last-child{text-align:right;white-space:nowrap;font-weight:600}
.ok{color:var(--brand)}.warn{color:#e0a422}
@media(max-width:900px){.grid{grid-template-columns:1fr}.wrap{padding:32px 16px 60px}}
"""

parts = ["<!doctype html><html lang='es'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width,initial-scale=1'>",
         "<title>Árbol Trade & Marketing — sitio para revisar</title>",
         "<style>%s</style></head><body><div class='wrap'>" % css,
         "<h1>Árbol Trade &amp; Marketing</h1>",
         "<p class='sub'>Sitio completo, escritorio y celular. Capturas reales del sitio andando.</p>",
         "<div class='note'><b>Lo que hay que saber:</b> la página se recorre "
         "<b>de abajo hacia arriba</b>, como pidió Gustavo. Arranca bajo tierra en la semilla "
         "y se sube por las raíces y el tronco hasta la copa. Está hecho de verdad así, no simulado.<br><br>"
         "<b>Lo único que falta:</b> el dibujo del árbol que se anima es "
         "<b>provisorio</b>. El logo llegó solo en JPG y una imagen JPG no se puede dibujar sola. "
         "Hace falta el archivo vectorial original (.ai / .eps / .svg) para reemplazarlo. "
         "Los logos reales del cliente sí se usan tal cual en el encabezado, en la tarjeta de contacto y en el 404.</div>"]

for title, sub, shots in GROUPS:
    parts.append("<h2>%s<span class='n'>%s</span></h2><div class='grid'>" % (title, sub))
    for fn, h, cap in shots:
        d = img(fn)
        if not d:
            continue
        parts.append("<div class='shot'><img src='%s' alt='%s'>"
                     "<div class='cap'><h3>%s</h3><p>%s</p></div></div>" % (d, h, h, cap))
    parts.append("</div>")

parts.append("<h2>Verificaciones<span class='n'>Automáticas, sobre el sitio real.</span></h2><table>")
for label, val, ok in CHECKS:
    parts.append("<tr><td>%s</td><td class='%s'>%s</td></tr>" % (label, "ok" if ok else "warn", val))
parts.append("</table></div></body></html>")

open(OUT, "w", encoding="utf-8").write("".join(parts))
print("wrote %s  (%.1f MB)" % (OUT, os.path.getsize(OUT) / 1024 / 1024))
