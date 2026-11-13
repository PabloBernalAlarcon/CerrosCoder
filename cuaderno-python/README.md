# Python Notebook

A small, free learning platform for a Python fundamentals course. Students log in from the school lab or from home, read lessons, write and run Python in the browser, check their exercises against automatic tests, and their progress is saved. The teacher gets a panel showing who solved what, who is stuck and who hasn't logged in lately.

It costs nothing to run: the site is static files on **GitHub Pages**, Python runs inside each student's browser with **Pyodide**, and logins and progress live in a free **Supabase** project.

Everything students see is in English. A few internal names (file names, and the field names inside the content files) are in Spanish; students never see them.

## What's in the folder

```
index.html          login and password change
inicio.html         student home: "continue where you left off", progress, units
leccion.html        lesson page (renders a Markdown file)
ejercicio.html      exercise page: editor, Run, Check, autosave
docente.html        teacher panel: progress grid, code viewer, CSV export
css/estilos.css     all styles (light and dark mode)
js/config.js        ← the only file you must edit to connect your project
js/app.js           shared helpers (login guard, course loading, etc.)
js/py-runner.js     runs Python with a time limit
js/py-worker.js     loads Pyodide in a background thread
js/harness.py       runs student code and the tests; friendly error hints
content/curso.json  the course map: units, lessons, exercises, unlock dates
content/lecciones/  one Markdown file per lesson
content/ejercicios/ one JSON file per exercise (statement, starter code, tests)
supabase/esquema.sql  database tables and security rules (run once)
scripts/estudiantes.py  create accounts and reset passwords (run on your computer)
```

## One-time setup (about 45 minutes)

Menu names in Supabase and GitHub change from time to time; if something isn't exactly where described, look for the closest equivalent.

**1. Create the Supabase project.** Sign up at supabase.com (free plan) and create a new project. Pick a region close to Colombia (for example, São Paulo or US East) and save the database password somewhere safe.

**2. Create the tables.** In the project, open **SQL Editor**, paste the whole content of `supabase/esquema.sql` and press **Run**. It should finish without errors.

**3. Turn off public sign-ups.** Go to **Authentication → Sign In / Providers** and turn off **Allow new users to sign up**. This matters: only you should be able to create accounts. Your script will still work, because it uses the admin key.

**4. Connect the website.** You need two values for `js/config.js`:

- `SUPABASE_URL`: in **Project Settings**, open **Data API** (under *Integrations*) and copy the **Project URL**. It looks like `https://abcdefghijklmnop.supabase.co`. The **Connect** button at the top of the project page shows it too.
- `SUPABASE_ANON_KEY`: in **Project Settings → API Keys**, copy the **Publishable key** (it starts with `sb_publishable_`). Use the new keys rather than the legacy ones, which Supabase plans to retire.

Both values are designed to be public; the security rules in `esquema.sql` are what keep each student's data private. Never put the **secret** key in this file.

**5. Publish on GitHub Pages.** Create a GitHub repository (it can be public), upload the whole folder, then go to **Settings → Pages**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`. After a minute your site will be at `https://YOUR-USER.github.io/REPO-NAME/`.

**6. Create your teacher account.** On your computer, with Python installed:

```bash
cd scripts
python estudiantes.py teacher profe
```

It asks for the Project URL and the **secret key** (**Project Settings → API Keys → Secret keys**, it starts with `sb_secret_`; your database password is not needed). Then it prints a temporary password. Log in on the site with `profe` and that password; you'll be asked to choose your own.

**7. Create student accounts.** Make a CSV like `scripts/example_students.csv`, with columns `name,username,group`:

```bash
python estudiantes.py create 8a.csv
```

This creates every account and writes `credentials-8a.csv` with each student's temporary password. Real names stay in that file on your computer only: the database stores just the username and group. The `.gitignore` keeps CSV files out of GitHub, but double-check before uploading anything.

Usernames like `8a-07` work well: short, no personal data, and the group is visible at a glance. Behind the scenes each one becomes a fake e-mail address (`8a-07@alumnos.example.com`). No e-mail is ever sent. If Supabase rejects that domain, change `EMAIL_DOMAIN` in both `js/config.js` and `scripts/estudiantes.py` to something else, such as a subdomain of your school's website.

To save typing, you can set the credentials once per terminal session instead of pasting them each time:

```bash
# macOS / Linux
export SUPABASE_URL="https://xxxx.supabase.co"
export SUPABASE_SECRET_KEY="..."
```
```powershell
# Windows PowerShell
$env:SUPABASE_URL="https://xxxx.supabase.co"
$env:SUPABASE_SECRET_KEY="..."
```

## Trying it on your own computer

The pages load files with `fetch`, so opening `index.html` by double-clicking won't work. Start a tiny local server in the project folder instead:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`. It talks to your real Supabase project, so you can test with your teacher account.

## Writing course content

You never touch the code to add content: you edit files in `content/`, upload them to GitHub, and the site updates.

### The course map: `content/curso.json`

```json
{
  "unidades": [
    {
      "id": "u1",
      "titulo": "First steps",
      "desbloqueo": "2027-02-08",
      "lecciones": [{ "id": "print", "titulo": "Talking to the computer: print()" }],
      "ejercicios": [{ "id": "greeting", "titulo": "Personal greeting" }]
    }
  ]
}
```

`titulo` is the title students see, and `desbloqueo` ("unlock") is the date (YYYY-MM-DD) when students can open the unit. Before that date they see the titles but can't open anything; you always see everything, with a note saying when it opens for students. The sample units are dated in the past so you can try everything right away. Units are numbered automatically in the order they appear.

### Lessons: `content/lecciones/<id>.md`

Plain Markdown. Code blocks marked as `python` get syntax colors. You can also embed slides: in Canva use **Share → Embed** (or in Google Slides **File → Share → Publish to web → Embed**) and paste the `<iframe>` code straight into the Markdown file. The page sizes it automatically.

### Exercises: `content/ejercicios/<id>.json`

```json
{
  "id": "is-passing",
  "titulo": "Did it pass?",
  "enunciado": "Markdown text shown to the student…",
  "codigo_inicial": "def is_passing(grade):\n    pass\n",
  "usa_input": false,
  "entradas_ejemplo": "",
  "no_usar": [],
  "pruebas": [ ... ]
}
```

The field names are Spanish, so here is a quick glossary: `titulo` title, `enunciado` instructions (Markdown), `codigo_inicial` starter code, `usa_input` uses input, `entradas_ejemplo` sample inputs, `no_usar` not allowed, `pruebas` tests, `descripcion` description, `expresion` expression, `esperado` expected, `tipo` type, `salida` output, `entradas` inputs.

There are two kinds of tests, and an exercise can mix them.

**Function tests** call the student's function and compare what it *returns*. `esperado` is written as Python (so `"True"`, `"8"`, `"'hello'"`, `"[1, 2]"`). Decimals are compared with a small tolerance, and `True` never passes for `1`.

```json
{ "descripcion": "Right at the limit: 4.5", "expresion": "is_passing(4.5)", "esperado": "True" }
```

**Output tests** run the whole program with given `input()` answers and compare what it *prints*. Spaces at the end of lines and blank lines at the end are ignored; the text of the `input("…")` question is not part of the output.

```json
{ "tipo": "salida", "descripcion": "5 and 7", "entradas": ["5", "7"], "esperado": "The sum is 12" }
```

Other fields: `usa_input: true` shows the "Inputs for input()" box from the start (it also appears by itself whenever a student's code uses `input()`), `entradas_ejemplo` pre-fills it, and `no_usar` lists names the student may not use, such as `["max", "sorted"]`.

Function-style exercises are the easiest to test reliably, and they push students toward `return`, which is worth the effort. When a test fails because a function printed instead of returning, the student gets a specific hint about it.

## Day to day

**A student forgot the password:** `python estudiantes.py reset 8a-07`. Their progress is kept; they choose a new password at their next login.

**Teacher panel:** each row is a student, each column an exercise. Green means solved, yellow means started (the number is how many times they pressed *Check*: a high number means they're stuck), and a dashed box means not started. Click any colored cell to read the student's current code. The last column turns red when someone hasn't worked for 14 days (change `DIAS_INACTIVO` in `config.js`). *Download CSV* exports the current group's progress for your grade book.

**Before class:** a two-minute look at the panel shows which exercise most of the class struggled with, which is a good place to start the session.

## Good to know

**Tests run in the student's browser,** so a determined student could find the expected answers with the browser's developer tools, or mark an exercise as solved without solving it. Treat auto-checked work as practice and completion credit, and keep graded evaluation for work you supervise or that students must explain.

**Infinite loops are handled:** after 5 seconds the program is stopped and the student is told why, without freezing the page. Very long printed output is also cut off.

**The first time** a device opens an exercise, it downloads Python (about 10 MB). After that it's cached and starts in a couple of seconds. On a slow lab connection, it helps to open one exercise on every lab computer once before class.

**Browsers:** recent Chrome, Edge or Firefox. Very old browsers can't run Pyodide.

**Supabase free plan:** free projects are paused after a stretch of inactivity (currently about a week). During the school year, students' activity keeps it awake; after long vacations you may need to press **Restore** in the Supabase dashboard. Check Supabase's current free-plan limits from time to time.

**Work is never lost easily:** code is saved to the server a few seconds after the student stops typing, and a copy is also kept in the browser in case the connection drops.

**Starting a new school year:** delete the old accounts in Supabase (Authentication → Users; their progress is deleted with them) and create the new ones with the script.

## Ideas for the next version

These fit the current design without rewriting anything: recall quizzes that mix questions from earlier units (for a warm-up at the start of each class), "holiday packs" that open automatically on festivo Mondays, a lesson-read tracker, and later the AI tutor, which would run in a Supabase Edge Function so the API key never reaches the browser.
