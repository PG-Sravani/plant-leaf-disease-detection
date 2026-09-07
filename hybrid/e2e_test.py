"""End-to-end test of the hybrid Gradio backend on this machine."""
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

PORT = "7864"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(ROOT, "run_demo_hybrid.py")
out_p = os.path.join(tempfile.gettempdir(), "hyb_out.txt")
err_p = os.path.join(tempfile.gettempdir(), "hyb_err.txt")

env = dict(os.environ)
env["PORT"] = PORT

with open(out_p, "w") as fo, open(err_p, "w") as fe:
    proc = subprocess.Popen(
        [sys.executable, "-u", SERVER], cwd=ROOT, env=env,
        stdout=fo, stderr=fe,
    )
    print("server pid", proc.pid)

try:
    url = "http://127.0.0.1:" + PORT
    deadline = time.time() + 150
    ok = False
    while time.time() < deadline:
        if proc.poll() is not None:
            print("SERVER DIED rc=", proc.returncode)
            break
        try:
            urllib.request.urlopen(url, timeout=3)
            ok = True
            break
        except Exception:
            time.sleep(2)
    print("server up:", ok)

    if ok:
        from gradio_client import Client, handle_file
        c = Client(url)
        import glob
        files = []
        for cls in ("Potato___Early_blight", "Pepper,_bell___Bacterial_spot",
                    "Tomato___Late_blight"):
            hits = glob.glob(os.path.join(ROOT, "dataset", "valid", cls, "*"))
            if hits:
                files.append(hits[0])
        if not files:
            print("no files found")
        for path in files:
            tag = os.path.basename(os.path.dirname(path))
            try:
                r = c.predict(handle_file(os.path.abspath(path)), api_name="/predict")
                print(tag, "->", list(r.items())[:3])
            except Exception as exc:
                print(tag, "-> ERROR", type(exc).__name__, str(exc)[:160])
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except Exception:
        proc.kill()
    for label, p in (("STDOUT", out_p), ("STDERR", err_p)):
        print("--- %s ---" % label)
        with open(p) as f:
            lines = f.read().splitlines()
        print("\n".join(lines[-30:]))