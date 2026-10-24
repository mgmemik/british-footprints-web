#!/usr/bin/env python3
"""Screenshots of every page (EN/TR, dark/light, desktop/mobile) into _screens/ (never published).

    python3 tools/shoot.py [filter]

Serves the site on 127.0.0.1:8765 for the duration of the run. Headless Chrome writes the
screenshot but does not always exit, so each Chrome is stopped once its file is complete.
"""
from urllib.parse import quote
import functools, http.server, os, shutil, subprocess, sys, tempfile, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = ROOT / "_screens"
PAGES = [("home", ""), ("privacy", "privacy/"), ("support", "support/")]
SIZES = [("desktop", 1280, 6400), ("mobile", 390, 9000)]  # mobile: a 390 px iframe in a 390 px clip


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def shoot(name, url, w, h):
    out = OUT / f"{name}.png"
    out.unlink(missing_ok=True)
    prof = tempfile.mkdtemp()
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                          "--no-default-browser-check", f"--user-data-dir={prof}", f"--window-size={w},{h}",
                          "--virtual-time-budget=8000", f"--screenshot={out}", url],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0, last = time.time(), -1
    while time.time() - t0 < 40:
        if p.poll() is not None:
            break
        if out.exists():
            size = out.stat().st_size
            if size > 0 and size == last:
                break
            last = size
        time.sleep(0.7)
    p.kill()
    p.wait()
    shutil.rmtree(prof, ignore_errors=True)
    print(("ok  " if out.exists() else "FAIL"), name)


def main():
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    OUT.mkdir(exist_ok=True)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        for page, path in PAGES:
            for lang in ("en", "tr"):
                for theme in ("dark", "light"):
                    for label, w, h in SIZES:
                        name = f"{page}-{lang}-{theme}-{label}"
                        if flt in name:
                            url = f"http://127.0.0.1:8765/{path}?lang={lang}&theme={theme}"
                            if label == "mobile":
                                url = "http://127.0.0.1:8765/tools/mobile-frame.html?src=" + quote(url, safe="")
                            shoot(name, url, w, h)
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
