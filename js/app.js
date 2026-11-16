// Shared helpers used by every page.
import { CONFIG } from "./config.js";

export { CONFIG };
// Keep only https://<project>.supabase.co, in case "/rest/v1/" was pasted along with the URL.
function projectOrigin(url) {
  try { return new URL(url.trim()).origin; } catch { return url; }
}
export const sb = window.supabase.createClient(projectOrigin(CONFIG.SUPABASE_URL), CONFIG.SUPABASE_ANON_KEY);

const NUNCA = new Promise(() => {}); // used to stop a page while it redirects

// ---------- Auth ----------

export function usernameToEmail(username) {
  return `${username.trim().toLowerCase()}@${CONFIG.EMAIL_DOMAIN}`;
}

export async function currentUser() {
  const { data } = await sb.auth.getSession();
  return data.session?.user ?? null;
}

export async function getProfile(userId) {
  const { data, error } = await sb
    .from("profiles")
    .select("id, username, grupo, role")
    .eq("id", userId)
    .single();
  if (error) throw error;
  return data;
}

// Call at the top of every protected page. Resolves to { user, profile }.
export async function requireLogin({ teacherOnly = false } = {}) {
  const user = await currentUser();
  if (!user) {
    location.replace("index.html");
    return NUNCA;
  }
  if (user.user_metadata?.must_change_password) {
    location.replace("index.html?cambiar=1");
    return NUNCA;
  }
  let profile;
  try {
    profile = await getProfile(user.id);
  } catch {
    showFatal("Couldn't load your profile. Check your internet connection and reload the page.");
    return NUNCA;
  }
  if (teacherOnly && profile.role !== "teacher") {
    location.replace("inicio.html");
    return NUNCA;
  }
  renderHeader(profile);
  return { user, profile };
}

export async function logout() {
  await sb.auth.signOut();
  location.replace("index.html");
}

export function renderHeader(profile) {
  const header = document.querySelector("[data-header]");
  if (!header) return;
  const docente = profile.role === "teacher";
  header.innerHTML = `
    <a class="cabecera-marca" href="inicio.html">${esc(CONFIG.APP_NAME)}</a>
    <nav class="cabecera-nav" aria-label="Main">
      <a href="inicio.html">Home</a>
      ${docente ? `<a href="docente.html">Teacher panel</a><a href="visibilidad.html">Visibility</a>` : ""}
      <a href="index.html?cambiar=1">Change password</a>
      <span class="cabecera-usuario">${esc(profile.username)}</span>
      <button type="button" class="boton boton-suave boton-pequeno" data-salir>Log out</button>
    </nav>`;
  header.querySelector("[data-salir]").addEventListener("click", logout);
  const aqui = location.pathname.split("/").pop() || "index.html";
  header.querySelectorAll(".cabecera-nav a").forEach((a) => {
    if (a.getAttribute("href") === aqui) a.setAttribute("aria-current", "page");
  });
}

// ---------- Mascot ----------

// Shows the mascot in an <img data-mascota hidden> if CONFIG.MASCOT is set.
// If the file is missing, the image simply stays hidden.
export function showMascot(img) {
  if (!img || !CONFIG.MASCOT) return;
  img.addEventListener("load", () => { img.hidden = false; }, { once: true });
  img.src = CONFIG.MASCOT;
}

// ---------- Course content ----------

let cursoCache;
export function loadCourse() {
  cursoCache ??= fetchJSON("content/curso.json");
  return cursoCache;
}

// Flat lists of lessons and exercises, each with a reference to its unit.
export function flatten(curso) {
  const lessons = [];
  const exercises = [];
  curso.unidades.forEach((unit, i) => {
    unit.numero = i + 1;
    // "etiqueta" (label) lets a unit be called "Week 7" instead of "Unit 1"
    // "repaso" (review) units are optional practice: shown apart, and not counted in progress
    unit.nombre = unit.repaso ? unit.titulo : `${unit.etiqueta || `Unit ${unit.numero}`}: ${unit.titulo}`;
    (unit.lecciones || []).forEach((l) => lessons.push({ ...l, unit }));
    (unit.ejercicios || []).forEach((e) => exercises.push({ ...e, unit }));
  });
  return { lessons, exercises };
}

function parseLocalDate(texto) {
  const [y, m, d] = texto.split("-").map(Number);
  return new Date(y, m - 1, d);
}

// ---------- Unit visibility ----------
// A unit is "open", "locked" (title visible, can't be opened) or "hidden" for students.
// The teacher sets it per class on the Visibility page (table unit_visibility).
// Without a setting, the unlock date in curso.json decides: open if there is no date.

export function defaultState(unit) {
  if (!unit.desbloqueo) return "open";
  return new Date() >= parseLocalDate(unit.desbloqueo) ? "open" : "locked";
}

// vis: Map unit_id -> state, for one class (from loadVisibility)
export function unitState(unit, vis) {
  return vis?.get(unit.id) || defaultState(unit);
}

// Teachers always see everything. Pass profile = null to check as a student.
export function isUnlocked(unit, profile, vis) {
  if (profile?.role === "teacher") return true;
  return unitState(unit, vis) === "open";
}

// Settings for one class. If the table doesn't exist yet, dates decide.
export async function loadVisibility(grupo) {
  const vis = new Map();
  if (!grupo) return vis;
  const { data, error } = await sb.from("unit_visibility").select("unit_id, estado").eq("grupo", grupo);
  if (error) { console.warn("Visibility settings unavailable:", error.message); return vis; }
  for (const r of data) vis.set(r.unit_id, r.estado);
  return vis;
}

// Settings for every class (teacher only): Map grupo -> Map unit_id -> state
export async function loadAllVisibility() {
  const all = new Map();
  const { data, error } = await sb.from("unit_visibility").select("grupo, unit_id, estado");
  if (error) return { all, error };
  for (const r of data) {
    if (!all.has(r.grupo)) all.set(r.grupo, new Map());
    all.get(r.grupo).set(r.unit_id, r.estado);
  }
  return { all, error: null };
}

// Message for a student who opens a link to a unit that isn't open
export function closedMessage(unit, vis, que = "page") {
  const st = unitState(unit, vis);
  if (st === "locked" && !vis?.get(unit.id) && unit.desbloqueo) return `This ${que} opens on ${formatDate(unit.desbloqueo)}.`;
  if (st === "locked") return `This ${que} isn't open yet. Your teacher will open it soon.`;
  return `This ${que} isn't available.`;
}

export function formatDate(texto) {
  return parseLocalDate(texto).toLocaleDateString("en-US", { month: "long", day: "numeric" });
}

// ---------- Data ----------

export async function fetchJSON(url) {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`Could not load ${url}`);
  return r.json();
}

export async function fetchText(url) {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`Could not load ${url}`);
  return r.text();
}

// Supabase returns at most 1000 rows per request; this pages through all of them.
// buildQuery must return a fresh, ordered query each time it's called.
export async function fetchAll(buildQuery, pageSize = 1000) {
  const rows = [];
  for (let desde = 0; ; desde += pageSize) {
    const { data, error } = await buildQuery().range(desde, desde + pageSize - 1);
    if (error) throw error;
    rows.push(...data);
    if (data.length < pageSize) return rows;
  }
}

// ---------- UI utilities ----------

export function param(nombre) {
  return new URLSearchParams(location.search).get(nombre);
}

export function esc(texto) {
  return String(texto ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[c]);
}

export function showFatal(mensaje) {
  const main = document.querySelector("main");
  if (main) main.innerHTML = `<div class="aviso aviso-error" role="alert">${esc(mensaje)}</div>`;
}

export function daysSince(iso) {
  if (!iso) return Infinity;
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);
  const dia = new Date(iso);
  dia.setHours(0, 0, 0, 0);
  return Math.round((hoy - dia) / 86400000);
}

export function relativeTime(iso) {
  const dias = daysSince(iso);
  if (dias === Infinity) return "never";
  if (dias <= 0) return "today";
  if (dias === 1) return "yesterday";
  if (dias < 30) return `${dias} days ago`;
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

// Colors Python code inside <pre><code> blocks (lessons, teacher code viewer).
export function highlightPython(raiz) {
  if (!window.CodeMirror?.runMode) return;
  raiz.querySelectorAll("pre code").forEach((code) => {
    const clase = code.className || "";
    if (clase && !/python|language-py\b/.test(clase)) return;
    const texto = code.textContent;
    code.textContent = "";
    window.CodeMirror.runMode(texto, "python", code);
  });
}
