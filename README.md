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
README.md             this guide (README.es.md: the same guide in Spanish)
index.html            login and password change
inicio.html           student home: "pick up where you left off", progress, units
leccion.html          lesson page (shows a Markdown file)
ejercicio.html        exercise page: editor, Run, Check, autosave
docente.html          teacher panel: progress grid, code viewer, CSV export
visibilidad.html      teacher only: choose which units each class can see
css/estilos.css       all the styles (light and dark mode)
images/mascot.png     the mascot shown on the login and home pages
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
supabase/visibilidad.sql  the Visibility table, for projects set up before it existed
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

This creates three tables (`profiles`, `submissions` and `unit_visibility`), gives the website permission to use them, and adds the security rules: each student can only see their own work, only the teacher can see everyone's, and only the teacher can change which units each class sees.

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

If the Project URL you copy ends in `/rest/v1/`, delete that part: you only want `https://<letters>.supabase.co`.

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

You can also change `APP_NAME` (the name shown at the top of every page) and `COURSE_SUBTITLE` (shown on the login page). `MASCOT` is the image shown on the login and home pages (`images/mascot.png` by default); set it to `""` to hide it, or put another image in the `images` folder and change the name. A transparent PNG, cropped close to the drawing, works best.

The publishable key is designed to be public. The security rules from Step 2 are what keep each student's data private.

### Step 6. Create your teacher account

Open a terminal (on Windows, **PowerShell**), go to the `scripts` folder, and run:

```
cd path\to\cuaderno-python\scripts
python estudiantes.py teacher profe
```

(`profe` is the username. You can choose another one, using lowercase letters, numbers and hyphens.)

The script asks for the **Project URL** and the **secret key**. When you paste the key, nothing appears on screen; that's normal. If **Ctrl + V** doesn't work there, paste with a **right-click**. Press Enter, and the script prints a **temporary password**. Write it down.

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

## The Grade 9 course (weeks 7–29)

The `content` folder holds the Grade 9 inquiry plan, adapted for the site:

- **Review the fundamentals**: an optional section at the top of the home page, collapsed by default. It has 10 detailed lessons on everything week 7 builds on (what a program is, `print`, numbers, variables and `+=`, types and conversion, `input`, building messages, True/False comparisons, reading error messages) and 34 practice exercises, numbered by lesson. It doesn't count toward the weekly progress bar or the teacher panel's "Solved" column, and it's always open. Students can use it to catch up after missed Mondays; you can see their work by choosing it in the panel's **Unit** menu.
- **One unit per week**, from week 7 (if/else) to week 23 (lists and tuples), plus one unit for the project (weeks 24–28) and the showcase (week 29). Weeks 13 and 19 are review units before the written tests.
- **Each week's lesson** carries the inquiry part of the session: the driving question, the code to read and predict (with a confidence rating), "Check your prediction" blocks, the investigation cards, the Make task, and the exit-ticket prompts for the log.
- **Each week's lab** is a free workspace with that week's starter code, for the investigation cards.
- **7 or 8 practice exercises per week**, marked ★ (warm-up), ★★ (core) and ★★★ (challenge), with "Bug hunt" exercises along the way. That's enough for a full 40-minute session, and extra for home.
- **Free workspaces** for the work that is graded or personal: *My Guess the Number game* (week 12), *My game, refactored* (week 18) and *My project* (weeks 24–28). They replace pasting code into Teams.

Exercises only use what students have seen by that week: no `and`/`or` before week 14, no functions before week 17, no `%` before week 21.

**Reference solutions** for every auto-checked exercise are in `solutions.md`, delivered separately. Keep that file private: **don't upload it to GitHub**, since the site's repository can be public.

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
| `no_usar` | not allowed | `definir` | functions that must be defined |
| `etiqueta` | unit label, e.g. "Week 7" | `libre` | free workspace (no tests) |
| `repaso` | review unit (optional practice) | `descripcion` | short description of a review unit |

### The course map: `content/curso.json`

```json
{
  "unidades": [
    {
      "id": "w08",
      "etiqueta": "Week 8",
      "titulo": "elif and the order of conditions",
      "desbloqueo": "2027-02-08",
      "lecciones": [{ "id": "w08-elif", "titulo": "Does the order of my conditions matter?" }],
      "ejercicios": [
        { "id": "w08-lab", "titulo": "Week 8 lab: the grade classifier", "libre": true },
        { "id": "w08-sign", "titulo": "Positive, negative or zero" }
      ]
    }
  ]
}
```

`desbloqueo` is an optional date (YYYY-MM-DD) when students can open the unit. Before that date they see the title with "Opens on…" but can't open anything. A unit with no `desbloqueo` is open straight away. The **Visibility** page (see *Day to day*) can override this for each class, so you may not need dates at all.

`etiqueta` is how the unit is labeled on the site ("Week 8"). Without it, units are called "Unit 1", "Unit 2" and so on, in order.

A unit marked `"repaso": true` is shown as a collapsible **review** section at the top of the home page instead of in the weekly list, with its `descripcion` as a subtitle. Its exercises don't count toward progress. Use it for optional practice.

An exercise marked `"libre": true` is a **free workspace**: it has no tests and no Check button. Students run code as often as they like, it saves automatically, and you can read it in the teacher panel. Free workspaces don't count toward the "solved" progress. The course uses them for each week's investigation lab, for the Guess the Number game, and for the final project.

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

To make students predict before they see an answer, put the answer in a "Check your prediction" block. Leave a blank line after the `<summary>` line and before `</details>`:

````markdown
<details>
<summary>Check your prediction</summary>

```text
True
False
```

</details>
````

Use `text` for blocks that show program output, so they aren't colored like code.

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
- `"definir": ["ask_question"]` lists functions the student must write with `def`. Useful when the point of an exercise is to write a function, and the output alone can't tell.

Function tests run the program once **without any inputs**, so an exercise with function tests shouldn't call `input()` outside a function. Use output tests for programs that ask questions.

Function-style exercises are the easiest to test reliably, and they push students toward `return`, which is worth practicing. When a test fails because a function printed instead of returning, the student gets a specific hint about it.

---

## Day to day

**A student forgot their password:**

```
python estudiantes.py reset 8a-07
```

It prints a new temporary password. Their progress is kept, and they choose a new password at their next login.

**Adding a student later:** put just that student in a new CSV and run `create` again.

**The teacher panel:** each row is a student and each column an exercise. Use the **Unit** menu to see one week at a time: it opens on the latest week that is open for at least one class.

- **Green ✓** means solved.
- **Yellow** means started; the number is how many times they pressed **Check**. A high number usually means they're stuck.
- **A dashed box** means not started.
- **A blue ✎** marks a free workspace where the student has saved code.
- **Click any colored cell** to read that student's current code.
- **The last column** turns red when someone hasn't worked for 14 days (change `DIAS_INACTIVO` in `config.js`).
- **Download CSV** exports the selected group's progress, for your grade book.

**Choosing what each class sees:** open **Visibility** in the top bar. Each row is a unit and each column is a class (the `group` from your student CSV). For every cell, choose:

- **Open:** students can read the lessons and do the exercises.
- **Locked:** students see the title with "Coming soon", but can't open it.
- **Hidden:** students don't see the unit at all.
- **Default:** follows the unit's date in `curso.json`, and open if there is none. The colors show what students actually get; a dashed border means the cell is on Default.

The **All classes** column changes a unit for every class at once. Changes save immediately; students see them the next time they load a page. A typical routine: at the start of the year, set every future week to **Locked** (or **Hidden**) for all classes, then open each week for each class when that class has had the session. So a class that lost a Monday to a holiday simply stays a week behind. As the teacher, you always see every unit.

Two things to know: the teacher panel's "Solved" column counts only units open for each student's class, and the menu's default unit is the latest week open for any class. Locking is a classroom tool, not a security lock: the lesson files are public on GitHub Pages, so a determined student could read a locked lesson directly.

**Before class:** a two-minute look at the panel shows which exercise most of the class struggled with. That's a good place to start the session.

**A new school year:** delete last year's accounts in Supabase (**Authentication → Users**; their progress is deleted with them), create the new accounts with the script, and set up **Visibility** for the new classes (or update the unlock dates in `curso.json`, if you use them).

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

**The Visibility page says "The visibility settings aren't set up yet":** your database was created before this feature. Run `supabase/visibilidad.sql` in the SQL Editor once and reload the page. It's safe to run more than once.

**"permission denied for table profiles" (error 403 / 42501):** the tables don't have permissions. This happens if the database was created with an older version of `esquema.sql`. Run `supabase/permisos.sql` in the SQL Editor, then run your command again.

**"the key was not accepted" (error 401):** you used the publishable key, a legacy key, or the database password. The script needs the **secret key** (`sb_secret_...`).

**"A user with this email address has already been registered":** that username already exists. For your own teacher account, just run `python estudiantes.py teacher profe` again: it gives the existing account a new password. For a student, use `reset`.

**"Wrong username or password" with a password you just copied:** work through these in order.

1. *Use the most recent password.* Every time you run `teacher` or `reset`, the previous temporary password stops working.
2. *Check that the site and the script use the same project.* The `SUPABASE_URL` in `js/config.js` must be the same Project URL you gave the script. This is easy to get wrong after creating a new project.
3. *Check that the account exists, with the right address.* In Supabase, open **Authentication → Users**. You should see `profe@alumnos.example.com` (or your username). The part after `@` must match `EMAIL_DOMAIN` in `js/config.js`.
4. *Reload the site without cache* (**Ctrl + Shift + R**), so the browser isn't using an old `config.js`.
5. *Get a fresh password and type it by hand:* `python estudiantes.py reset profe`.
6. *Let the script check everything for you:* `python estudiantes.py check profe`. It compares `js/config.js` with the project the script uses, looks up the account, and tries to log in exactly like the website does, telling you which part fails.

**"Password login is turned off in Supabase":** in Step 3 the **Email** provider was turned off instead of the sign-up option. In **Authentication → Sign In / Providers**, turn the **Email** provider back on and keep only **Allow new users to sign up** turned off.

**The site says "Couldn't load your profile" or shows nothing after login:** check that `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `js/config.js` are correct, and that `esquema.sql` ran without errors.

**An exercise or lesson page shows an error:** the file name doesn't match its `id` in `curso.json`, or the JSON has a typo (check it on jsonlint.com).

**Changes don't show up on the website:** after you upload files, GitHub Pages needs a minute or two to publish them (watch the **Actions** tab for a green check), and browsers may keep an old copy for up to **10 minutes**. Wait, then reload with **Ctrl + Shift + R**, or check in a private window. To see what the site is really serving, open a file with `?v=check` at the end, for example `…github.io/your-repo/js/app.js?v=check`.

**A page says "This page couldn't start", or stays on "Loading…":** the page's code couldn't run. Usually some files on the website are from different updates, or a file is in the wrong folder (for example `app.js` at the top level instead of inside `js/`). Upload every file from the latest update, keeping the `js` and `css` folders, and wait as described above. The message includes a technical detail; the browser console (**F12 → Console**) shows the exact error.

**It works on GitHub but not on `localhost` (or the other way round):** `python -m http.server` serves the folder it was started in. If you have more than one copy of the project on your computer, stop the server (**Ctrl + C**), go to the right folder, and start it again.

---

## Ideas for the next version

These fit the current design without rewriting anything:

- **Recall quizzes** that mix questions from earlier units, for a warm-up at the start of each class.
- **Holiday packs** that open automatically on festivo Mondays, so a missed class becomes practice.
- **Lesson tracking**, so the panel shows who read each lesson.
- **An AI tutor** that gives hints rather than answers. It would run in a Supabase Edge Function so the API key never reaches the browser.
