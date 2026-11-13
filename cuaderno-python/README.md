# Python Notebook

A small, free learning platform for a Python fundamentals course. Students log in from the school lab or from home, read lessons, write and run Python in the browser, and check their exercises against automatic tests. Their work is saved as they go. You get a teacher panel showing who solved what, who is stuck and who hasn't logged in lately.

It costs nothing to run:

- **GitHub Pages** hosts the website (plain HTML, CSS and JavaScript, no build step).
- **Pyodide** runs Python inside each student's browser, so no server is needed to execute code.
- **Supabase** (free plan) stores logins and progress.

Everything students see is in English. A few internal names (page file names, and the field names inside the content files) are in Spanish; students never see them.

---

## What's in the folder

```
index.html            login and password change
inicio.html           student home: "pick up where you left off", progress, units
leccion.html          lesson page (shows a Markdown file)
ejercicio.html        exercise page: editor, Run, Check, autosave
docente.html          teacher panel: progress grid, code viewer, CSV export
css/estilos.css       all the styles (light and dark mode)
js/config.js          ← the only code file you need to edit
js/app.js             shared helpers (login check, course loading, etc.)
js/py-runner.js       runs Python with a time limit
js/py-worker.js       loads Pyodide in the background
js/harness.py         runs student code and tests; friendly error hints
content/curso.json    the course map: units, lessons, exercises, unlock dates
content/lecciones/    one Markdown file per lesson
content/ejercicios/   one JSON file per exercise (instructions, starter code, tests)
supabase/esquema.sql  database tables, permissions and security rules (run once)
supabase/permisos.sql permissions only (not needed for a new setup, see Troubleshooting)
scripts/estudiantes.py     creates accounts and resets passwords (runs on your computer)
scripts/example_students.csv  example of the student list format
```

---

## Setup from zero

Plan for about 45 minutes. You need a computer with **Python 3** installed, a free **Supabase** account and a free **GitHub** account.

Supabase and GitHub rename their menus from time to time. If something isn't exactly where this guide says, look for the closest match.

### Step 1. Create the Supabase project

1. Go to **supabase.com**, sign up, and click **New project**.
2. Give it a name (for example, `python-notebook`), choose a region close to Colombia (for example, **South America (São Paulo)**), and set a database password.
3. Save that database password somewhere safe. You won't need it for this platform, but Supabase asks for it in some situations.
4. Wait a minute or two while the project starts.

> If you have an older project from a previous attempt, you can delete it (**Project Settings → General → Delete project**) and start fresh, so you don't mix old and new settings.

### Step 2. Create the database tables

1. In the left sidebar, open **SQL Editor** and start a **New query**.
2. Open `supabase/esquema.sql` from the folder, copy **all** of it, and paste it into the editor.
3. Press **Run**. You should see a "Success" message.

This creates two tables (`profiles` and `submissions`), gives the website permission to use them, and adds the security rules: each student can only see their own work, and only the teacher can see everyone's.

Run this file **only once**. Running it again gives "already exists" errors, which are harmless but confusing.

### Step 3. Turn off public sign-ups

Go to **Authentication → Sign In / Providers** and turn **off** the option **Allow new users to sign up**, then save.

This matters: without it, anyone who finds your site could create an account. You'll create every account yourself with the script, and the script still works with sign-ups off.

### Step 4. Find your three values

You need three values from Supabase. Open **Project Settings** (the gear icon at the bottom of the sidebar).

| Value | Where to find it | What it looks like | Where it goes |
|---|---|---|---|
| **Project URL** | **Data API** (under *Integrations*), or the **Connect** button at the top of the project page | `https://abcdefghijklmnop.supabase.co` | `config.js` and the script |
| **Publishable key** | **API Keys** → *Publishable key* → the **default** row → copy | `sb_publishable_...` | `config.js` only |
| **Secret key** | **API Keys** → *Secret keys* → the **default** row → reveal and copy | `sb_secret_...` | The script only |

Use these new keys, not the "legacy" ones: Supabase plans to retire the legacy keys in 2027.

> **The Project URL is not the address in your browser bar** (`https://supabase.com/dashboard/project/...`). That one won't work.
>
> **Treat the secret key like a master password.** It can do anything in your database. Never put it in `config.js`, in GitHub, in a screenshot or anywhere students can see it. If it ever leaks, delete it on the API Keys page and create a new one.

### Step 5. Connect the website

Open `js/config.js` in a text editor (Notepad works, VS Code is nicer) and fill in:

```js
SUPABASE_URL: "https://abcdefghijklmnop.supabase.co",   // your Project URL
SUPABASE_ANON_KEY: "sb_publishable_...",                 // your Publishable key
```

You can also change `APP_NAME` (the name shown at the top of every page) and `COURSE_SUBTITLE` (shown on the login page).

The publishable key is designed to be public. The security rules from Step 2 are what keep each student's data private.

### Step 6. Create your teacher account

Open a terminal (on Windows, **PowerShell**), go to the `scripts` folder, and run:

```
cd path\to\cuaderno-python\scripts
python estudiantes.py teacher profe
```

(`profe` is the username. You can choose another one, using lowercase letters, numbers and hyphens.)

The script asks for the **Project URL** and the **secret key**. When you paste the key, nothing appears on screen; that's normal. Press Enter, and the script prints a **temporary password**. Write it down.

To avoid pasting the URL and key every time, you can set them once per terminal window:

```powershell
# Windows PowerShell
$env:SUPABASE_URL="https://abcdefghijklmnop.supabase.co"
$env:SUPABASE_SECRET_KEY="sb_secret_..."
```
```bash
# macOS / Linux
export SUPABASE_URL="https://abcdefghijklmnop.supabase.co"
export SUPABASE_SECRET_KEY="sb_secret_..."
```

These are forgotten when you close the window, which is what you want for the secret key.

### Step 7. Try it on your computer

The pages load files from the folder, so double-clicking `index.html` won't work. Start a small local web server instead. In a terminal, go to the **main project folder** (not `scripts`) and run:

```
python -m http.server 8000
```

Open **http://localhost:8000** in your browser and log in with `profe` and the temporary password. The site asks you to create your own password, then takes you to the teacher panel.

Click **Home** to see the student view, open an exercise, and press **Check**. The first time, Python takes a few seconds to load. If you can run code and see test results, everything is connected.

Stop the server with **Ctrl + C** in the terminal.

### Step 8. Publish on GitHub Pages

1. On **github.com**, create a new repository (for example, `python-notebook`). It can be public.
2. Upload the contents of the project folder (**Add file → Upload files**, then drag in everything inside `cuaderno-python`). The `index.html` file must be at the top level of the repository, not inside a subfolder.
3. Before uploading, check that no student list or credentials CSV is in the `scripts` folder. Only `example_students.csv` should be there.
4. Go to **Settings → Pages**. Under *Build and deployment*, choose **Deploy from a branch**, branch **main**, folder **/ (root)**, and save.
5. After a minute or two, your site is live at `https://YOUR-USERNAME.github.io/python-notebook/`.

Log in there once to confirm it works the same as on your computer.

### Step 9. Create the student accounts

Make a CSV file for each group (Excel can save as CSV) with three columns, like `scripts/example_students.csv`:

```
name,username,group
Ana Pérez,8a-01,8A
Juan David Rojas,8a-02,8A
```

Save it in the `scripts` folder (for example, `8a.csv`) and run:

```
python estudiantes.py create 8a.csv
```

The script creates every account and writes **`credentials-8a.csv`** next to your file, with each student's temporary password. Give each student their username and password. They'll choose their own password the first time they log in.

A few notes:

- **Usernames like `8a-07`** work well: short, no personal information, and the group is visible at a glance.
- **Real names stay on your computer.** The database only stores the username and group. Keep the student lists and credentials files private, and never upload them to GitHub (the included `.gitignore` helps, but check anyway).
- **No e-mail is ever sent.** Behind the scenes each username becomes a made-up address like `8a-07@alumnos.example.com`. If Supabase ever rejects that domain, change `EMAIL_DOMAIN` to the same new value in both `js/config.js` and `scripts/estudiantes.py` *before* creating any accounts.

You're ready for class.

---

## Writing course content

You never need to touch the code to add content. Edit the files in `content/`, upload them to GitHub, and the site updates within a minute or two.

The content files use Spanish field names. Here's a quick glossary:

| Field | Meaning | Field | Meaning |
|---|---|---|---|
| `titulo` | title | `pruebas` | tests |
| `desbloqueo` | unlock date | `descripcion` | test description |
| `lecciones` | lessons | `expresion` | expression to evaluate |
| `ejercicios` | exercises | `esperado` | expected result |
| `enunciado` | instructions | `tipo` / `salida` | type / output |
| `codigo_inicial` | starter code | `entradas` | inputs |
| `usa_input` | uses input() | `entradas_ejemplo` | sample inputs |
| `no_usar` | not allowed | | |

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

`desbloqueo` is the date (YYYY-MM-DD) when students can open the unit. Before that date they see the titles but can't open anything. You always see everything, with a note saying when each unit opens for students. The sample units are dated in the past so you can try everything right away. Units are numbered automatically in the order they appear.

Each lesson `id` must match a file in `content/lecciones/`, and each exercise `id` must match a file in `content/ejercicios/`. Use lowercase letters, numbers and hyphens for ids, and don't rename an exercise once students have started it: their saved work is linked to the id.

### Lessons: `content/lecciones/<id>.md`

Plain Markdown. Code blocks marked as `python` get syntax colors:

````markdown
# Variables

A **variable** is like a labeled box.

```python
name = "Valentina"
print(name)
```
````

You can embed slides. In Canva use **Share → Embed**, or in Google Slides **File → Share → Publish to web → Embed**, and paste the `<iframe>` code straight into the Markdown file. The page sizes it automatically.

### Exercises: `content/ejercicios/<id>.json`

```json
{
  "id": "is-passing",
  "titulo": "Did it pass?",
  "enunciado": "Create a function `is_passing(grade)` that returns `True` if the grade is 4.5 or more.",
  "codigo_inicial": "def is_passing(grade):\n    pass\n",
  "pruebas": [
    { "descripcion": "Right at the limit: 4.5", "expresion": "is_passing(4.5)", "esperado": "True" },
    { "descripcion": "Almost: 4.4", "expresion": "is_passing(4.4)", "esperado": "False" }
  ]
}
```

In JSON, a line break inside text is written as `\n`, and quotes inside text as `\"`. If an exercise page shows an error after you edit it, paste the file into **jsonlint.com** to find the mistake.

There are two kinds of tests, and one exercise can mix them.

**Function tests** call the student's function and compare what it *returns*. `esperado` is written the way you'd write it in Python: `"True"`, `"8"`, `"'hello'"`, `"[1, 2]"`. Decimal numbers are compared with a small tolerance, and `True` never passes for `1`.

```json
{ "descripcion": "Right at the limit: 4.5", "expresion": "is_passing(4.5)", "esperado": "True" }
```

**Output tests** run the whole program, answer its `input()` questions with the values you give, and compare what it *prints*. Spaces at the end of lines and blank lines at the end are ignored. The question text inside `input("...")` is not part of the output, so students can word their questions however they like.

```json
{ "tipo": "salida", "descripcion": "5 and 7", "entradas": ["5", "7"], "esperado": "The sum is 12" }
```

Optional fields:

- `"usa_input": true` shows the **Inputs for input()** box from the start. (It also appears by itself as soon as a student's code uses `input()`.)
- `"entradas_ejemplo": "5\n7"` pre-fills that box.
- `"no_usar": ["max", "sorted"]` lists names the student may not use. Using one makes the exercise fail with a clear message.

Function-style exercises are the easiest to test reliably, and they push students toward `return`, which is worth practicing. When a test fails because a function printed instead of returning, the student gets a specific hint about it.

---

## Day to day

**A student forgot their password:**

```
python estudiantes.py reset 8a-07
```

It prints a new temporary password. Their progress is kept, and they choose a new password at their next login.

**Adding a student later:** put just that student in a new CSV and run `create` again.

**The teacher panel:** each row is a student and each column an exercise.

- **Green ✓** means solved.
- **Yellow** means started; the number is how many times they pressed **Check**. A high number usually means they're stuck.
- **A dashed box** means not started.
- **Click any colored cell** to read that student's current code.
- **The last column** turns red when someone hasn't worked for 14 days (change `DIAS_INACTIVO` in `config.js`).
- **Download CSV** exports the selected group's progress, for your grade book.

**Before class:** a two-minute look at the panel shows which exercise most of the class struggled with. That's a good place to start the session.

**A new school year:** delete last year's accounts in Supabase (**Authentication → Users**; their progress is deleted with them), update the unlock dates in `curso.json`, and create the new accounts with the script.

---

## Good to know

**Tests run in the student's browser.** A determined student could find the expected answers with the browser's developer tools, or mark an exercise as solved without solving it. Treat auto-checked work as practice and completion credit, and keep graded evaluation for work you supervise or that students have to explain.

**Infinite loops are handled.** After 5 seconds the program is stopped and the student is told why, without freezing the page. Huge amounts of printed text are also cut off.

**Python loads once per device.** The first time a computer opens an exercise, it downloads Python (about 10 MB). After that it's cached and starts in a few seconds. On a slow lab connection, open one exercise on every lab computer once before the first class.

**Browsers:** recent Chrome, Edge or Firefox. Very old browsers can't run Pyodide.

**Work is hard to lose.** Code is saved to the server a few seconds after the student stops typing, and a copy is kept in the browser in case the connection drops.

**Supabase free plan:** free projects are paused after about a week without activity. During the school year, students' work keeps it awake. After long vacations you may need to press **Restore project** in the Supabase dashboard. Check Supabase's free-plan limits from time to time, since they can change.

---

## Troubleshooting

**"Error 405" or "the server answered with a web page":** the Project URL is wrong. Use the one from **Data API** (`https://....supabase.co`), not your browser's address bar. If you set `$env:SUPABASE_URL` earlier in that window, check it with `echo $env:SUPABASE_URL`.

**"permission denied for table profiles" (error 403 / 42501):** the tables don't have permissions. This happens if the database was created with an older version of `esquema.sql`. Run `supabase/permisos.sql` in the SQL Editor, then run your command again.

**"the key was not accepted" (error 401):** you used the publishable key, a legacy key, or the database password. The script needs the **secret key** (`sb_secret_...`).

**"A user with this email address has already been registered":** that username already exists. For your own teacher account, just run `python estudiantes.py teacher profe` again: it gives the existing account a new password. For a student, use `reset`.

**The site says "Couldn't load your profile" or shows nothing after login:** check that `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `js/config.js` are correct, and that `esquema.sql` ran without errors.

**An exercise or lesson page shows an error:** the file name doesn't match its `id` in `curso.json`, or the JSON has a typo (check it on jsonlint.com).

**Changes don't show up on the website:** GitHub Pages can take a couple of minutes. Then reload with **Ctrl + Shift + R**.

---

## Ideas for the next version

These fit the current design without rewriting anything:

- **Recall quizzes** that mix questions from earlier units, for a warm-up at the start of each class.
- **Holiday packs** that open automatically on festivo Mondays, so a missed class becomes practice.
- **Lesson tracking**, so the panel shows who read each lesson.
- **An AI tutor** that gives hints rather than answers. It would run in a Supabase Edge Function so the API key never reaches the browser.
