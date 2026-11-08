// Shared helpers used by every page.
import { CONFIG } from "./config.js";

export { CONFIG };
export const sb = window.supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);

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
    showFatal("No se pudo cargar tu perfil. Revisa la conexión a internet y recarga la página.");
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
    <nav class="cabecera-nav" aria-label="Principal">
      <a href="inicio.html">Inicio</a>
      ${docente ? `<a href="docente.html">Panel docente</a>` : ""}
      <a href="index.html?cambiar=1">Cambiar contraseña</a>
      <span class="cabecera-usuario">${esc(profile.username)}</span>
      <button type="button" class="boton boton-suave boton-pequeno" data-salir>Salir</button>
    </nav>`;
  header.querySelector("[data-salir]").addEventListener("click", logout);
  const aqui = location.pathname.split("/").pop() || "index.html";
  header.querySelectorAll(".cabecera-nav a").forEach((a) => {
    if (a.getAttribute("href") === aqui) a.setAttribute("aria-current", "page");
  });
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
    (unit.lecciones || []).forEach((l) => lessons.push({ ...l, unit }));
    (unit.ejercicios || []).forEach((e) => exercises.push({ ...e, unit }));
  });
  return { lessons, exercises };
}

function parseLocalDate(texto) {
  const [y, m, d] = texto.split("-").map(Number);
  return new Date(y, m - 1, d);
}

// Teachers always see everything. Pass profile = null to check as a student.
export function isUnlocked(unit, profile) {
  if (profile?.role === "teacher" || !unit.desbloqueo) return true;
  return new Date() >= parseLocalDate(unit.desbloqueo);
}

export function formatDate(texto) {
  return parseLocalDate(texto).toLocaleDateString("es-CO", { day: "numeric", month: "long" });
}

// ---------- Data ----------

export async function fetchJSON(url) {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`No se pudo cargar ${url}`);
  return r.json();
}

export async function fetchText(url) {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`No se pudo cargar ${url}`);
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
  if (dias === Infinity) return "nunca";
  if (dias <= 0) return "hoy";
  if (dias === 1) return "ayer";
  if (dias < 30) return `hace ${dias} días`;
  return new Date(iso).toLocaleDateString("es-CO", { day: "numeric", month: "short" });
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
