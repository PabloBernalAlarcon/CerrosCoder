"""
Manage student accounts for Cuaderno Python. Run it on YOUR computer only.

    python estudiantes.py crear lista.csv          create accounts from a CSV (nombre,usuario,grupo)
    python estudiantes.py reiniciar 8a-07          give a student a new temporary password
    python estudiantes.py docente profe            create your teacher account

It needs your project's URL and its *secret* (service_role) key. You can put them in
environment variables SUPABASE_URL and SUPABASE_SECRET_KEY, or just paste them when asked.
The secret key can do anything in your database: never put it in the website, in GitHub,
or anywhere students can see it.

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

PALABRAS = [
    "arepa", "bambu", "cafe", "colibri", "condor", "cometa", "delfin", "guadua", "jaguar",
    "lapiz", "loro", "mango", "nube", "orquidea", "palma", "piedra", "puma", "rio",
    "tigre", "tucan", "volcan", "brisa", "lulo", "mora", "faro", "ancla",
]

USUARIO_VALIDO = re.compile(r"^[a-z0-9][a-z0-9._-]{1,30}$")


def pedir_credenciales():
    url = os.environ.get("SUPABASE_URL") or input("URL del proyecto (https://....supabase.co): ").strip()
    clave = os.environ.get("SUPABASE_SECRET_KEY") or getpass.getpass("Clave secreta (service_role, no se mostrará): ").strip()
    if not url.startswith("https://") or not clave:
        sys.exit("Faltan la URL o la clave.")
    return url.rstrip("/"), clave


def peticion(url_base, clave, metodo, ruta, cuerpo=None, extra=None):
    cabeceras = {"apikey": clave, "Content-Type": "application/json"}
    if clave.startswith("eyJ"):  # legacy JWT-style keys also go in Authorization
        cabeceras["Authorization"] = f"Bearer {clave}"
    cabeceras.update(extra or {})
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(url_base + ruta, data=datos, method=metodo, headers=cabeceras)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            texto = r.read().decode()
            return json.loads(texto) if texto else None
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code}: {e.read().decode(errors='replace')}") from None


def nueva_clave():
    return f"{secrets.choice(PALABRAS)}-{secrets.randbelow(9000) + 1000}"


def crear_cuenta(url, clave, usuario, grupo, password):
    return peticion(url, clave, "POST", "/auth/v1/admin/users", {
        "email": f"{usuario}@{EMAIL_DOMAIN}",
        "password": password,
        "email_confirm": True,
        "user_metadata": {"username": usuario, "grupo": grupo, "must_change_password": True},
    })


def buscar_perfil(url, clave, usuario):
    q = urllib.parse.quote(usuario)
    filas = peticion(url, clave, "GET", f"/rest/v1/profiles?username=eq.{q}&select=id,username,grupo")
    if not filas:
        sys.exit(f"No existe el usuario {usuario}.")
    return filas[0]


def cmd_crear(args):
    archivo = Path(args.csv)
    with archivo.open(encoding="utf-8-sig", newline="") as f:
        filas = list(csv.DictReader(f))
    if not filas or not {"usuario", "grupo"} <= set(filas[0].keys()):
        sys.exit("El CSV debe tener columnas: nombre,usuario,grupo")

    errores = []
    for fila in filas:
        usuario = fila["usuario"].strip().lower()
        if not USUARIO_VALIDO.match(usuario):
            errores.append(f"Usuario no válido: {usuario!r} (usa minúsculas, números y guiones)")
    if errores:
        sys.exit("\n".join(errores))

    url, clave = pedir_credenciales()
    salida = archivo.with_name(f"credenciales-{archivo.stem}.csv")
    creadas = 0
    with salida.open("w", encoding="utf-8-sig", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["nombre", "usuario", "grupo", "contraseña_temporal"])
        for fila in filas:
            usuario = fila["usuario"].strip().lower()
            grupo = fila["grupo"].strip()
            password = nueva_clave()
            try:
                crear_cuenta(url, clave, usuario, grupo, password)
            except RuntimeError as e:
                print(f"  ✗ {usuario}: {e}")
                continue
            escritor.writerow([fila.get("nombre", "").strip(), usuario, grupo, password])
            creadas += 1
            print(f"  ✓ {usuario}")
    print(f"\n{creadas} de {len(filas)} cuentas creadas.")
    print(f"Contraseñas temporales en: {salida}")
    print("Guárdalo en un lugar privado. Cada estudiante deberá cambiarla la primera vez que entre.")


def cmd_reiniciar(args):
    url, clave = pedir_credenciales()
    perfil = buscar_perfil(url, clave, args.usuario.strip().lower())
    password = nueva_clave()
    peticion(url, clave, "PUT", f"/auth/v1/admin/users/{perfil['id']}", {
        "password": password,
        "user_metadata": {"username": perfil["username"], "grupo": perfil["grupo"], "must_change_password": True},
    })
    print(f"Nueva contraseña temporal para {perfil['username']}: {password}")
    print("La cambiará la próxima vez que entre. Su progreso no se pierde.")


def cmd_docente(args):
    usuario = args.usuario.strip().lower()
    if not USUARIO_VALIDO.match(usuario):
        sys.exit("Usuario no válido (usa minúsculas, números y guiones).")
    url, clave = pedir_credenciales()
    password = nueva_clave()
    cuenta = crear_cuenta(url, clave, usuario, "", password)
    peticion(url, clave, "PATCH", f"/rest/v1/profiles?id=eq.{cuenta['id']}", {"role": "teacher"},
             extra={"Prefer": "return=minimal"})
    print(f"Cuenta docente creada: {usuario}  Contraseña temporal: {password}")


def main():
    p = argparse.ArgumentParser(description="Cuentas de Cuaderno Python")
    sub = p.add_subparsers(dest="comando", required=True)
    c = sub.add_parser("crear", help="crear cuentas desde un CSV (nombre,usuario,grupo)")
    c.add_argument("csv")
    c.set_defaults(func=cmd_crear)
    r = sub.add_parser("reiniciar", help="dar una contraseña temporal nueva")
    r.add_argument("usuario")
    r.set_defaults(func=cmd_reiniciar)
    d = sub.add_parser("docente", help="crear una cuenta de docente")
    d.add_argument("usuario")
    d.set_defaults(func=cmd_docente)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
