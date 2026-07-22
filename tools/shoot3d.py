#!/usr/bin/env python3
"""
Screenshot harness for the 3D version. Same idea as shoot.py, but it drives
the scroller to a given progress (0 = seed, 1 = canopy) and waits for the
WebGL scene to settle before capturing.

  python3 tools/shoot3d.py --p 0 --out shots/3d-p00.png
  python3 tools/shoot3d.py --p 0.55 --w 390 --h 844 --frame --out shots/3d-m.png
"""
import argparse
import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 8899

SHIM = """
<script>
window.__errs = [];
window.addEventListener('error', function(e){ window.__errs.push('ERR ' + e.message + ' @' + (e.filename||'').split('/').pop() + ':' + e.lineno); });
window.addEventListener('load', function(){
  var s = document.getElementById('scroller');
  s.style.scrollBehavior = 'auto';
  var st = document.createElement('style');
  st.textContent = '*{transition:none !important}';
  document.head.appendChild(st);
  var all = document.querySelectorAll('[data-reveal], .art');
  for (var i = 0; i < all.length; i++) all[i].classList.add('in');
  // Drive the reversed scroller to the requested progress AFTER the page's
  // own anchor() has run on load, otherwise it resets us back to the seed.
  setTimeout(function(){
    var m = s.scrollHeight - s.clientHeight;
    s.scrollTop = -m * __P__;
    if (s.scrollTop === 0 && __P__ > 0) s.scrollTop = m * __P__;
  }, 700);
  setTimeout(function(){
    var d = document.createElement('pre');
    d.id = '__diag'; d.style.display = 'none';
    d.textContent = JSON.stringify({
      errors: window.__errs,
      webgl: !document.documentElement.classList.contains('no-webgl'),
      ready: document.documentElement.classList.contains('scene-ready'),
      scrollTop: Math.round(s.scrollTop),
      max: Math.round(s.scrollHeight - s.clientHeight)
    });
    document.body.appendChild(d);
    if (window.parent !== window) window.parent.postMessage({__diag: d.textContent}, '*');
  }, 4200);
});
</script>
"""

GL = ["--enable-unsafe-swiftshader", "--use-gl=angle", "--use-angle=swiftshader"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=float, default=0.0)
    ap.add_argument("--w", type=int, default=1440)
    ap.add_argument("--h", type=int, default=900)
    ap.add_argument("--frame", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    src = open(os.path.join(ROOT, "3d", "index.html"), encoding="utf-8").read()
    src = src.replace("</head>", SHIM.replace("__P__", repr(a.p)) + "</head>")
    shot = os.path.join(ROOT, "3d", "_shot.html")
    open(shot, "w", encoding="utf-8").write(src)

    out = os.path.join(ROOT, a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    url = "http://localhost:%d/3d/_shot.html" % PORT
    win_w, win_h = a.w, a.h
    if a.frame:
        url = ("http://localhost:%d/tools/_frame.html?src=../3d/_shot.html&w=%d&h=%d"
               % (PORT, a.w, a.h))
        win_w, win_h = max(a.w + 20, 520), a.h + 20

    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars"] + GL +
                       ["--window-size=%d,%d" % (win_w, win_h), "--screenshot=" + out,
                        "--virtual-time-budget=11000", url],
                       capture_output=True, timeout=260)
        dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars"] + GL +
                             ["--window-size=%d,%d" % (win_w, win_h), "--dump-dom",
                              "--virtual-time-budget=11000", url],
                             capture_output=True, timeout=260, text=True).stdout
        m = re.search(r'<pre id="__diag"[^>]*>(.*?)</pre>', dom, re.S)
        print("%-22s p=%-5s %s" % (os.path.basename(out), a.p,
                                   (m.group(1).strip() if m else "(no diagnostics)")[:230]))
    finally:
        if os.path.exists(shot):
            os.remove(shot)


if __name__ == "__main__":
    main()
