#!/usr/bin/env python3
import json, os, subprocess, urllib.request

tok = open("/root/.fdl_token").read().strip()
H = {"Authorization": "token " + tok, "Accept": "application/vnd.github+json",
     "Content-Type": "application/json"}

def api(method, path, body=None):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=json.dumps(body).encode() if body else None, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

print("user:", api("GET", "/user")[1].get("login"))
st, body = api("POST", "/user/repos", {"name": "morrow-hci", "private": False,
    "description": "Morrow 学生工作区 HCI 研究议题规划", "has_pages": True})
print("create repo:", st, body.get("full_name") or body.get("message"))

os.chdir("/root/morrow-hci")
env = dict(os.environ, HOME="/root")
def run(*a):
    r = subprocess.run(a, capture_output=True, text=True, env=env)
    print(a[:2], r.returncode, (r.stdout + r.stderr).strip()[-300:])
    return r.returncode

run("git", "init", "-q", "-b", "main")
run("git", "add", "index.html")
run("git", "-c", "user.email=agent@evenna.local", "-c", "user.name=agent", "commit", "-q", "-m", "Morrow student studio: HCI research agenda")
run("git", "remote", "remove", "origin")
run("git", "remote", "add", "origin", "https://x-access-token:" + tok + "@github.com/Evenna/morrow-hci.git")
run("git", "push", "-f", "origin", "main")

st, body = api("POST", "/repos/Evenna/morrow-hci/pages", {"source": {"branch": "main", "path": "/"}})
print("pages:", st, body.get("html_url") or body.get("message"))
