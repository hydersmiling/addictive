"""Take a screenshot of a local web page, so Claude can look at what it built.

Uses a Chromium-based browser you already have (Microsoft Edge, Google Chrome or
Chromium) in headless mode. Nothing is installed and nothing is sent anywhere: the
browser only opens the local file you name.

Usage:
    python scripts/screenshot.py index.html                  # writes index.png
    python scripts/screenshot.py index.html --out shot.png --width 1280 --height 3000

Set the BROWSER environment variable to a browser's full path to choose one yourself.
"""

import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

# Where Chromium-based browsers usually live, per operating system.
WINDOWS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
MAC = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]
LINUX_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"]


def find_browser():
    """Return the path of a usable browser, or None if none is found."""
    chosen = os.environ.get("BROWSER")
    if chosen and os.path.exists(chosen):
        return chosen
    candidates = WINDOWS if os.name == "nt" else MAC if sys.platform == "darwin" else []
    for path in candidates:
        if os.path.exists(path):
            return path
    for name in LINUX_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def screenshot_command(browser, page, out, width, height, profile):
    """The headless browser command that writes a PNG of the page."""
    url = pathlib.Path(page).resolve().as_uri()
    return [browser, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
            f"--user-data-dir={profile}", f"--window-size={width},{height}",
            "--virtual-time-budget=8000", f"--screenshot={os.path.abspath(out)}", url]


def take(page, out=None, width=1280, height=3000):
    """Write a screenshot of `page`. Returns the PNG path, or None on failure."""
    browser = find_browser()
    if not browser:
        print("No Chromium-based browser found (Edge, Chrome or Chromium). Set BROWSER to its path.")
        return None
    out = out or os.path.splitext(page)[0] + ".png"
    if os.path.exists(out):
        os.remove(out)
    with tempfile.TemporaryDirectory() as profile:  # a throwaway profile, never your own
        subprocess.run(screenshot_command(browser, page, out, width, height, profile),
                       capture_output=True, timeout=120)
    if not os.path.exists(out):
        print(f"The browser did not write {out}.")
        return None
    return out


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Screenshot a local web page.")
    parser.add_argument("page", help="the HTML file to capture")
    parser.add_argument("--out", help="PNG to write (default: next to the page)")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=3000)
    args = parser.parse_args(argv)
    if not os.path.exists(args.page):
        print(f"Not found: {args.page}")
        return 1
    out = take(args.page, args.out, args.width, args.height)
    if out:
        print(f"Wrote {out}")
    return 0 if out else 1


if __name__ == "__main__":
    sys.exit(main())
