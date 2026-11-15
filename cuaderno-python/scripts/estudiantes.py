"""
Manage student accounts for the Python Notebook platform. Run it on YOUR computer only.

    python estudiantes.py create students-8a.csv   create accounts from a CSV (name,username,group)
    python estudiantes.py reset 8a-07              give a student a new temporary password
    python estudiantes.py teacher profe            create your teacher account
    python estudiantes.py check profe              diagnose login problems step by step

(The older Spanish commands crear, reiniciar and docente still work.)

It needs your Project URL and your *secret* key (sb_secret_... or the legacy service_role key).
You can put them in environment variables SUPABASE_URL and SUPABASE_SECRET_KEY, or paste them
when asked. The secret key can do anything in your database: never put it in the website,
in GitHub, or anywhere students can see it.

Only uses Python's standard library: nothing to install.
"""
import argparse
import csv
import getpass
import json
import os
import re
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Must match EMAIL_DOMAIN in js/config.js
EMAIL_DOMAIN = os.environ.get("EMAIL_DOMAIN", "alumnos.example.com")

WORDS = [
    "apple", "banana", "cloud", "comet", "condor", "dolphin", "falcon", "forest", "jaguar",
    "lemon", "mango", "maple", "ocean", "orbit", "panda", "parrot", "pencil", "planet",
    "puma", "river", "rocket", "tiger", "toucan", "volcano", "wave", "zebra",
]

VALID_USERNAME = re.compile(r"^[a-z0-9][a-z0-9._-]{1,30}$")


def clean_url(url):
    """Accept only the API URL (https://<ref>.supabase.co), dropping any extra path."""
    parts = urllib.parse.urlparse(url.strip())
    host = parts.netloc.lower()
    if parts.scheme != "https" or not host.endswith(".supabase.co"):
        sys.exit(
            f"{url!r} is not your Project URL.\n"
            "It should look like this: https://abcdefghijklmnop.supabase.co\n"
            "Find it in Supabase → Project Settings → Data API → Project URL.\n"
            "Don't use the address from your browser bar (https://supabase.com/dashboard/...)."
        )
    return f"https://{host}"


def ask_credentials():
    url = clean_url(os.environ.get("SUPABASE_URL") or input("Project URL (https://....supabase.co): "))
    key = (os.environ.get("SUPABASE_SECRET_KEY")
           or getpass.getpass("Secret key (sb_secret_..., it won't be shown as you type): ")).strip()
    if not key:
        sys.exit("The secret key is missing.")
    if not (key.startswith("sb_secret_") or key.startswith("eyJ")):
        sys.exit("That doesn't look like the secret key. It should start with sb_secret_ "
                 "(or eyJ for the legacy service_role key).\n"
                 "Note: it is not your database password.")
    return url, key


def request(base_url, key, method, path, body=None, extra_headers=None):
    headers = {"apikey": key, "Content-Type": "application/json"}
    if key.startswith("eyJ"):  # legacy JWT-style keys also go in Authorization
        headers["Authorization"] = f"Bearer {key}"
    headers.update(extra_headers or {})
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base_url + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            text = r.read().decode()
            return json.loads(text) if text else None
    except urllib.error.HTTPError as e:
        text = e.read().decode(errors="replace")
        if text.lstrip().startswith("<"):
            sys.exit(f"Error {e.code}: the server answered with a web page instead of the Supabase API. "
                     "Check your Project URL.")
        if '"42501"' in text or "permission denied" in text:
            sys.exit(f"Error {e.code}: the key works, but the database tables don't have permissions yet.\n"
                     "In Supabase, open SQL Editor, paste the contents of supabase/permisos.sql, press Run, "
                     "and then run this command again.")
        if e.code in (401, 403):
            sys.exit(f"Error {e.code}: the key was not accepted. Use the secret key (sb_secret_...).\n{text}")
        raise RuntimeError(f"{e.code}: {text}") from None
    except urllib.error.URLError as e:
        sys.exit(f"Could not connect to {base_url}: {e.reason}")


def new_password():
    return f"{secrets.choice(WORDS)}-{secrets.randbelow(9000) + 1000}"


def create_account(url, key, username, group, password):
    return request(url, key, "POST", "/auth/v1/admin/users", {
        "email": f"{username}@{EMAIL_DOMAIN}",
        "password": password,
        "email_confirm": True,
        "user_metadata": {"username": username, "grupo": group, "must_change_password": True},
    })


def find_profile(url, key, username):
    q = urllib.parse.quote(username)
    rows = request(url, key, "GET", f"/rest/v1/profiles?username=eq.{q}&select=id,username,grupo")
    if not rows:
        sys.exit(f"There is no user called {username}.")
    return rows[0]


def column(row, *names):
    for n in names:
        if n in row and row[n] is not None:
            return row[n].strip()
    return ""


def cmd_create(args):
    path = Path(args.csv)
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("The CSV is empty.")
    headers = set(rows[0].keys())
    if not ({"username", "group"} <= headers or {"usuario", "grupo"} <= headers):
        sys.exit("The CSV needs these columns: name,username,group")

    students = [(column(r, "name", "nombre"), column(r, "username", "usuario").lower(), column(r, "group", "grupo"))
                for r in rows]
    bad = [u for _, u, _ in students if not VALID_USERNAME.match(u)]
    if bad:
        sys.exit("Invalid usernames (use lowercase letters, numbers and hyphens): " + ", ".join(map(repr, bad)))

    url, key = ask_credentials()
    out = path.with_name(f"credentials-{path.stem}.csv")
    created = 0
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "username", "group", "temporary_password"])
        for name, username, group in students:
            password = new_password()
            try:
                create_account(url, key, username, group, password)
            except RuntimeError as e:
                print(f"  ✗ {username}: {e}")
                continue
            writer.writerow([name, username, group, password])
            created += 1
            print(f"  ✓ {username}")
    print(f"\nCreated {created} of {len(students)} accounts.")
    print(f"Temporary passwords are in: {out}")
    print("Keep that file private. Each student will choose a new password the first time they log in.")


def cmd_reset(args):
    url, key = ask_credentials()
    profile = find_profile(url, key, args.username.strip().lower())
    password = new_password()
    request(url, key, "PUT", f"/auth/v1/admin/users/{profile['id']}", {
        "password": password,
        "user_metadata": {"username": profile["username"], "grupo": profile["grupo"], "must_change_password": True},
    })
    print(f"New temporary password for {profile['username']}: {password}")
    print("They'll choose a new one at their next login. Their progress is kept.")


def cmd_teacher(args):
    username = args.username.strip().lower()
    if not VALID_USERNAME.match(username):
        sys.exit("Invalid username (use lowercase letters, numbers and hyphens).")
    url, key = ask_credentials()
    password = new_password()
    try:
        account_id = create_account(url, key, username, "", password)["id"]
        action = "created"
    except RuntimeError as e:
        if "already" not in str(e) and "email_exists" not in str(e):
            raise
        # The account exists (e.g. an earlier attempt stopped halfway): give it a new password.
        account_id = find_profile(url, key, username)["id"]
        request(url, key, "PUT", f"/auth/v1/admin/users/{account_id}", {
            "password": password,
            "user_metadata": {"username": username, "grupo": "", "must_change_password": True},
        })
        action = "already existed, so it was updated"
    request(url, key, "PATCH", f"/rest/v1/profiles?id=eq.{account_id}", {"role": "teacher"},
            extra_headers={"Prefer": "return=minimal"})
    print(f"Teacher account {username} {action}.   Temporary password: {password}")


def read_site_config():
    """Read SUPABASE_URL, SUPABASE_ANON_KEY and EMAIL_DOMAIN from ../js/config.js."""
    path = Path(__file__).resolve().parent.parent / "js" / "config.js"
    if not path.exists():
        sys.exit(f"Can't find {path}. Run this script from inside the project's scripts folder.")
    text = path.read_text(encoding="utf-8")
    values = {}
    for name in ("SUPABASE_URL", "SUPABASE_ANON_KEY", "EMAIL_DOMAIN"):
        m = re.search(name + r"""\s*:\s*["']([^"']*)["']""", text)
        values[name] = m.group(1).strip() if m else ""
    return path, values


def try_login(url, publishable_key, email, password):
    # Same headers the website's Supabase library sends
    headers = {"apikey": publishable_key, "Authorization": f"Bearer {publishable_key}",
               "Content-Type": "application/json"}
    data = json.dumps({"email": email, "password": password}).encode()
    req = urllib.request.Request(f"{url}/auth/v1/token?grant_type=password", data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30):
            return True, "OK"
    except urllib.error.HTTPError as e:
        return False, f"{e.code}: {e.read().decode(errors='replace')}"
    except urllib.error.URLError as e:
        return False, f"could not connect: {e.reason}"


def cmd_check(args):
    ok = lambda msg: print(f"  ✓ {msg}")
    bad = lambda msg: print(f"  ✗ {msg}")
    problems = 0

    print("1. Reading js/config.js (what the website uses)")
    path, site = read_site_config()
    print(f"   File: {path}")
    site_url = site["SUPABASE_URL"]
    print(f"   SUPABASE_URL:      {site_url or '(empty)'}")
    print(f"   SUPABASE_ANON_KEY: {site['SUPABASE_ANON_KEY'][:20] + '...' if site['SUPABASE_ANON_KEY'] else '(empty)'}")
    print(f"   EMAIL_DOMAIN:      {site['EMAIL_DOMAIN'] or '(empty)'}")
    if not site["SUPABASE_ANON_KEY"].startswith(("sb_publishable_", "eyJ")):
        bad("SUPABASE_ANON_KEY doesn't look like a publishable key (it should start with sb_publishable_).")
        problems += 1
    if site["SUPABASE_ANON_KEY"].startswith("sb_secret_"):
        bad("DANGER: that is the SECRET key. Replace it with the publishable key and delete/rotate the secret key in Supabase.")
        problems += 1

    print("\n2. The project the script uses")
    url, key = ask_credentials()
    print(f"   Project URL: {url}")
    site_origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(site_url.strip().lower()))
    if site_origin == url and site_url.rstrip("/").lower() != url:
        bad(f"config.js has extra text after the Project URL. Change SUPABASE_URL to exactly: {url}")
        problems += 1
    elif site_origin == url:
        ok("config.js and the script point to the same project.")
    else:
        bad("config.js points to a DIFFERENT project. Copy this Project URL into js/config.js, "
            "together with this project's publishable key.")
        problems += 1
    if site["EMAIL_DOMAIN"] == EMAIL_DOMAIN:
        ok(f"Both use the e-mail domain {EMAIL_DOMAIN}.")
    else:
        bad(f"EMAIL_DOMAIN differs: config.js has {site['EMAIL_DOMAIN']!r}, the script uses {EMAIL_DOMAIN!r}. "
            "They must be the same.")
        problems += 1

    print("\n3. The account")
    username = args.username.strip().lower()
    rows = request(url, key, "GET",
                   f"/rest/v1/profiles?username=eq.{urllib.parse.quote(username)}&select=id,username,role")
    if not rows:
        bad(f"There is no profile called {username} in this project. Create it with: "
            f"python estudiantes.py teacher {username}")
        return
    profile = rows[0]
    user = request(url, key, "GET", f"/auth/v1/admin/users/{profile['id']}")
    email = user.get("email", "")
    ok(f"{username} exists. Stored as {email}, role: {profile['role']}")
    expected_email = f"{username}@{site['EMAIL_DOMAIN']}"
    if email != expected_email:
        bad(f"The website will look for {expected_email}, but the account is {email}.")
        problems += 1
    if not user.get("email_confirmed_at"):
        bad("The account's e-mail is not confirmed. Run: python estudiantes.py reset " + username)
        problems += 1

    print("\n4. Logging in exactly like the website does")
    password = getpass.getpass(f"   Temporary password for {username} (hidden): ").strip()
    login_url = site_origin if site_origin.startswith("http") else url
    success, detail = try_login(login_url, site["SUPABASE_ANON_KEY"], expected_email, password)
    if success:
        ok("Login works with these settings.")
        if problems == 0:
            print("\nEverything checks out. If the website still fails, it is probably using an older copy of "
                  "config.js: reload with Ctrl+Shift+R, and if you use GitHub Pages, upload the current config.js "
                  "and wait a couple of minutes.")
    else:
        bad(f"Login failed. Supabase says: {detail}")
        if "invalid_credentials" in detail or "Invalid login" in detail:
            print("   The password doesn't match. Run 'reset' again and type the new password by hand.")
        if "provider" in detail.lower() or "disabled" in detail.lower():
            print("   Password login is turned off: in Authentication → Sign In / Providers, turn the Email provider on.")


def main():
    p = argparse.ArgumentParser(description="Python Notebook accounts")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("create", aliases=["crear"], help="create accounts from a CSV (name,username,group)")
    c.add_argument("csv")
    c.set_defaults(func=cmd_create)
    r = sub.add_parser("reset", aliases=["reiniciar"], help="give a student a new temporary password")
    r.add_argument("username")
    r.set_defaults(func=cmd_reset)
    t = sub.add_parser("teacher", aliases=["docente"], help="create a teacher account")
    t.add_argument("username")
    t.set_defaults(func=cmd_teacher)
    k = sub.add_parser("check", aliases=["revisar"], help="diagnose login problems for one account")
    k.add_argument("username")
    k.set_defaults(func=cmd_check)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
