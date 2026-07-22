#!/usr/bin/env python3
"""
Visual QA harness. Renders index.html in headless Chrome at a given viewport,
optionally scrolled to a section, and saves a screenshot.

It builds a throwaway _shot.html next to index.html (so relative paths still
resolve), injects a scroll+error-capture shim, screenshots, then deletes it.
Nothing it injects ever touches the shipped index.html.

  python3 tools/shoot.py --w 1440 --h 900 --at s3 --out shots/desktop-s3.png
  python3 tools/shoot.py --w 390 --h 844 --at s1 --out shots/mobile-s1.png
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 8899

# Installed in <head> so it catches errors thrown by script.js itself.
HEAD_SHIM = """
<script>
window.__errs = [];
window.addEventListener('error', function(e){ window.__errs.push('ERR ' + e.message + ' @' + (e.filename||'').split('/').pop() + ':' + e.lineno); });
window.addEventListener('unhandledrejection', function(e){ window.__errs.push('REJ ' + e.reason); });
</script>
"""

SHIM = """
<script>
(function(){
  var errs = window.__errs || [];
  var ce = console.error; console.error = function(){ errs.push('CONSOLE ' + [].join.call(arguments,' ')); ce.apply(console, arguments); };
  function report(){
    var d = document.createElement('pre');
    d.id = '__diag';
    d.style.display = 'none';
    var s = document.getElementById('scroller');
    d.textContent = JSON.stringify({
      errors: errs,
      scrollTop: s ? Math.round(s.scrollTop) : null,
      max: s ? Math.round(s.scrollHeight - s.clientHeight) : null,
      railH: (document.getElementById('railFill')||{style:{}}).style.height || '',
      revealed: document.querySelectorAll('[data-reveal].in').length,
      total: document.querySelectorAll('[data-reveal]').length,
      hOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      boxes: ['#ftr','#s5','#s1','.waves','.trunk-art','.canopy-art'].reduce(function(o,sel){
        var e = document.querySelector(sel);
        if (e) { var r = e.getBoundingClientRect();
          o[sel] = [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; }
        return o;
      }, {})
    });
    document.body.appendChild(d);
    if (window.parent !== window) window.parent.postMessage({__diag: d.textContent}, '*');
  }
  window.addEventListener('load', function(){
    var target = '__TARGET__';
    var s = document.getElementById('scroller');
    if (s) { s.style.scrollBehavior = 'auto'; }
    if (__FINAL__) {
      // Jump straight to the settled end state so QA shots are deterministic
      // instead of catching the draw-on animation mid-stroke.
      var st = document.createElement('style');
      st.textContent = '*{transition:none !important;animation:none !important}';
      document.head.appendChild(st);
      var all = document.querySelectorAll('[data-reveal], .art');
      for (var i = 0; i < all.length; i++) all[i].classList.add('in');
    }
    if (target === 'top' && s) {
      // extreme end of the reversed scroller — clamps whichever sign it uses
      s.scrollTop = -1e7; if (s.scrollTop === 0) s.scrollTop = 1e7;
    } else if (target && target !== 's1' && s) {
      var el = document.getElementById(target);
      if (el) el.scrollIntoView({block: '__BLOCK__'});
    }
    setTimeout(report, 1600);
  });
})();
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--w", type=int, default=1440)
    ap.add_argument("--h", type=int, default=900)
    ap.add_argument("--at", default="s1")
    ap.add_argument("--block", default="center")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dsf", default="1")
    ap.add_argument("--final", action="store_true", help="force settled end state")
    ap.add_argument("--frame", action="store_true",
                    help="render inside an iframe — headless Chrome clamps its own window to a 500px minimum, "
                         "so this is the only way to get a genuine narrow mobile viewport")
    a = ap.parse_args()

    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    shim = (SHIM.replace("__TARGET__", a.at).replace("__BLOCK__", a.block)
            .replace("__FINAL__", "true" if a.final else "false"))
    html = html.replace("<head>", "<head>" + HEAD_SHIM, 1)
    html = html.replace("</body>", shim + "</body>")
    shot_path = os.path.join(ROOT, "_shot.html")
    open(shot_path, "w", encoding="utf-8").write(html)

    out = os.path.join(ROOT, a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    url = "http://localhost:%d/_shot.html" % PORT
    win_w, win_h = a.w, a.h
    if a.frame:
        url = ("http://localhost:%d/tools/_frame.html?src=../_shot.html&w=%d&h=%d"
               % (PORT, a.w, a.h))
        win_w, win_h = max(a.w + 20, 520), a.h + 20

    try:
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=" + a.dsf,
            "--window-size=%d,%d" % (win_w, win_h),
            "--screenshot=" + out, "--virtual-time-budget=4000", url,
        ], capture_output=True, timeout=90)

        dom = subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--window-size=%d,%d" % (win_w, win_h),
            "--dump-dom", "--virtual-time-budget=4000", url,
        ], capture_output=True, timeout=90, text=True).stdout

        m = re.search(r'<pre id="__diag"[^>]*>(.*?)</pre>', dom, re.S)
        diag = m.group(1) if m else "(no diagnostics)"
        print("%-26s %s" % (os.path.basename(out), diag.strip()[:400]))
    finally:
        if os.path.exists(shot_path):
            os.remove(shot_path)

    if not os.path.exists(out):
        print("FAILED to write", out)
        sys.exit(1)


if __name__ == "__main__":
    main()
