"""
Runs student code and exercise tests inside Pyodide (loaded by py-worker.js).

The worker calls _atender(request_json) and receives a JSON string back.
Student-facing messages are in Spanish; comments are in English.
"""
import ast
import builtins
import io
import json
import math
import sys
import traceback
from contextlib import contextmanager

ARCHIVO = "<tu código>"   # filename shown in error messages
MAX_SALIDA = 20_000        # characters of output before we stop a runaway print loop

# Friendly hints for the most common beginner errors.
PISTAS = {
    "IndentationError": "La sangría (los espacios al inicio de la línea) no está bien. "
                        "El código que va dentro de un if, for, while o def debe ir corrido hacia la derecha.",
    "SyntaxError": "Python no entiende cómo está escrita esta línea. Revisa paréntesis, comillas "
                   "y los dos puntos (:) al final de if, else, for, while y def.",
    "NameError": "Usaste un nombre que Python no conoce. ¿Está bien escrito (mayúsculas incluidas)? "
                 "¿Creaste la variable antes de usarla? ¿Olvidaste las comillas de un texto?",
    "TypeError": "Estás mezclando tipos de datos que no combinan, por ejemplo sumar un texto con un número. "
                 "Usa int(), float() o str() para convertir.",
    "ValueError": "El valor no tiene la forma esperada, por ejemplo int(\"hola\"). Revisa los datos que escribiste.",
    "ZeroDivisionError": "Estás dividiendo entre cero.",
    "IndexError": "Intentas usar una posición que no existe. Recuerda que se empieza a contar desde 0.",
    "KeyError": "Esa clave no existe en el diccionario.",
    "AttributeError": "Ese tipo de dato no tiene ese método. Revisa cómo está escrito.",
    "EOFError": "El programa pidió más datos con input() de los que escribiste en la caja de entradas.",
    "RecursionError": "Una función se está llamando a sí misma sin parar.",
    "DemasiadaSalida": "Tu programa imprimió muchísimo texto. ¿Hay un ciclo que nunca termina?",
}


class DemasiadaSalida(Exception):
    pass


class _SalidaLimitada(io.StringIO):
    def write(self, s):
        if self.tell() + len(s) > MAX_SALIDA:
            super().write(s[: max(0, MAX_SALIDA - self.tell())])
            raise DemasiadaSalida("Demasiada salida")
        return super().write(s)


class _Entradas:
    """Replacement for input() that reads from a list instead of the keyboard."""

    def __init__(self, valores, salida, eco):
        self.valores = [str(v) for v in valores]
        self.salida = salida
        self.eco = eco

    def __call__(self, mensaje=""):
        if self.eco:
            self.salida.write(str(mensaje))
        if not self.valores:
            raise EOFError("input() pidió un dato, pero ya no quedan entradas")
        valor = self.valores.pop(0)
        if self.eco:
            self.salida.write(valor + "\n")
        return valor


@contextmanager
def _aislado(entradas=(), eco=False):
    """Capture print() output and feed input() from a list while the block runs."""
    salida = _SalidaLimitada()
    guardado = (sys.stdout, sys.stderr, builtins.input)
    sys.stdout = sys.stderr = salida
    builtins.input = _Entradas(entradas, salida, eco)
    try:
        yield salida
    finally:
        sys.stdout, sys.stderr, builtins.input = guardado


def _espacio():
    return {"__name__": "__main__", "__builtins__": builtins}


def _pista(exc):
    for clase in type(exc).__mro__:
        if clase.__name__ in PISTAS:
            return PISTAS[clase.__name__]
    return ""


def _info_error(exc):
    linea = None
    if isinstance(exc, SyntaxError) and exc.filename == ARCHIVO:
        linea = exc.lineno
    for marco in traceback.extract_tb(exc.__traceback__):
        if marco.filename == ARCHIVO:
            linea = marco.lineno
    if isinstance(exc, DemasiadaSalida):
        mensaje = "Tu programa imprimió demasiado texto y lo detuvimos."
    else:
        try:
            partes = traceback.TracebackException.from_exception(exc).format_exception_only()
            mensaje = "".join(partes).strip()
        except Exception:
            mensaje = f"{type(exc).__name__}: {exc}"
    return {"tipo": type(exc).__name__, "mensaje": mensaje, "linea": linea, "pista": _pista(exc)}


def _ejecutar(codigo, espacio):
    """Run the student's code. Returns error info, or None if it ran fine."""
    try:
        exec(compile(codigo, ARCHIVO, "exec"), espacio)
    except SystemExit:
        return None
    except BaseException as exc:
        return _info_error(exc)
    return None


def _normalizar(texto):
    lineas = [l.rstrip() for l in str(texto).replace("\r\n", "\n").split("\n")]
    while lineas and not lineas[-1]:
        lineas.pop()
    while lineas and not lineas[0]:
        lineas.pop(0)
    return "\n".join(lineas)


def _iguales(obtenido, esperado):
    # True must not pass as 1 (and vice versa)
    if isinstance(obtenido, bool) or isinstance(esperado, bool):
        return type(obtenido) is type(esperado) and obtenido == esperado
    numeros = (int, float)
    if isinstance(obtenido, numeros) and isinstance(esperado, numeros):
        if isinstance(obtenido, float) or isinstance(esperado, float):
            return math.isclose(obtenido, esperado, rel_tol=1e-9, abs_tol=1e-9)
    try:
        return bool(obtenido == esperado)
    except Exception:
        return False


def _nombres_usados(codigo):
    try:
        arbol = ast.parse(codigo)
    except SyntaxError:
        return set()
    nombres = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Name):
            nombres.add(nodo.id)
        elif isinstance(nodo, ast.Attribute):
            nombres.add(nodo.attr)
    return nombres


def _prueba_salida(codigo, prueba, desc):
    entradas = prueba.get("entradas", [])
    with _aislado(entradas, eco=False) as salida:
        error = _ejecutar(codigo, _espacio())
    r = {
        "descripcion": desc,
        "tipo": "salida",
        "entradas": entradas,
        "esperado": prueba["esperado"],
        "obtenido": salida.getvalue(),
    }
    if error:
        r.update(ok=False, error=error)
    else:
        r["ok"] = _normalizar(r["obtenido"]) == _normalizar(prueba["esperado"])
    return r


def _prueba_expresion(espacio, prueba, desc):
    expresion = prueba["expresion"]
    r = {"descripcion": desc, "tipo": "expresion", "expresion": expresion, "esperado": prueba["esperado"]}
    with _aislado([], eco=False) as salida:
        try:
            obtenido = eval(compile(expresion, "<prueba>", "eval"), espacio)
            fallo = None
        except BaseException as exc:
            fallo = exc
    if fallo is not None:
        r.update(ok=False, error=_info_error(fallo))
        nombre = getattr(fallo, "name", None)
        if isinstance(fallo, NameError) and nombre and nombre in expresion:
            r["nota"] = f"No encontramos {nombre}. Revisa que tu función se llame exactamente {nombre}."
        return r
    esperado = ast.literal_eval(prueba["esperado"])
    r["obtenido"] = repr(obtenido)
    r["ok"] = _iguales(obtenido, esperado)
    if obtenido is None and not r["ok"]:
        if salida.getvalue().strip():
            r["nota"] = "Tu función imprimió algo, pero no devolvió nada. ¿Usaste print() en lugar de return?"
        else:
            r["nota"] = "Tu función no devolvió nada. ¿Te faltó escribir return?"
    return r


def _comprobar(codigo, pruebas, prohibidos):
    resultados = []

    usados = _nombres_usados(codigo) & set(prohibidos or [])
    if usados:
        resultados.append({
            "descripcion": "Reglas del ejercicio",
            "tipo": "regla",
            "ok": False,
            "nota": "En este ejercicio no puedes usar: " + ", ".join(sorted(usados))
                    + ". Intenta resolverlo con lo que has aprendido.",
        })

    espacio_funciones = None   # the program is run once and shared by all expression tests
    error_funciones = None

    for i, prueba in enumerate(pruebas, start=1):
        desc = prueba.get("descripcion") or f"Prueba {i}"
        if prueba.get("tipo") == "salida":
            resultados.append(_prueba_salida(codigo, prueba, desc))
            continue
        if espacio_funciones is None:
            espacio_funciones = _espacio()
            with _aislado([], eco=False):
                error_funciones = _ejecutar(codigo, espacio_funciones)
        if error_funciones:
            resultados.append({
                "descripcion": desc, "tipo": "expresion", "expresion": prueba["expresion"],
                "esperado": prueba["esperado"], "ok": False, "error": error_funciones,
            })
            continue
        resultados.append(_prueba_expresion(espacio_funciones, prueba, desc))

    return resultados


def _atender(peticion_json):
    p = json.loads(peticion_json)
    codigo = p.get("code", "")
    if p.get("mode") == "check":
        res = {"pruebas": _comprobar(codigo, p.get("tests", []), p.get("prohibidos", []))}
    else:
        with _aislado(p.get("inputs", []), eco=True) as salida:
            error = _ejecutar(codigo, _espacio())
        res = {"salida": salida.getvalue(), "error": error}
    return json.dumps(res, ensure_ascii=False)
