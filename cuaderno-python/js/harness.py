"""
Runs student code and exercise tests inside Pyodide (loaded by py-worker.js).

The worker calls _atender(request_json) and receives a JSON string back.
Student-facing messages are in simple English.
"""
import ast
import builtins
import io
import json
import math
import sys
import traceback
from contextlib import contextmanager

ARCHIVO = "<your code>"   # filename shown in error messages
MAX_SALIDA = 20_000        # characters of output before we stop a runaway print loop

# Friendly hints for the most common beginner errors.
PISTAS = {
    "IndentationError": "The indentation (the spaces at the start of the line) isn't right. "
                        "Code inside an if, for, while or def must be moved to the right.",
    "SyntaxError": "Python can't understand how this line is written. Check your parentheses, quotes "
                   "and the colon (:) at the end of if, else, for, while and def.",
    "NameError": "You used a name Python doesn't know. Is it spelled correctly (capital letters too)? "
                 "Did you create the variable before using it? Did you forget the quotes around some text?",
    "TypeError": "You're mixing data types that don't go together, like adding text to a number. "
                 "Use int(), float() or str() to convert.",
    "ValueError": "The value isn't in the expected form, for example int(\"hello\"). Check the data you typed.",
    "ZeroDivisionError": "You're dividing by zero.",
    "IndexError": "You're using a position that doesn't exist. Remember that counting starts at 0.",
    "KeyError": "That key doesn't exist in the dictionary.",
    "AttributeError": "That kind of data doesn't have that method. Check how it's spelled.",
    "EOFError": "Your program asked for more input() answers than you typed in the inputs box.",
    "RecursionError": "A function keeps calling itself without stopping.",
    "DemasiadaSalida": "Your program printed a huge amount of text. Is there a loop that never ends?",
}


class DemasiadaSalida(Exception):
    pass


class _SalidaLimitada(io.StringIO):
    def write(self, s):
        if self.tell() + len(s) > MAX_SALIDA:
            super().write(s[: max(0, MAX_SALIDA - self.tell())])
            raise DemasiadaSalida("Too much output")
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
            raise EOFError("input() asked for a value, but there are no inputs left")
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
        mensaje = "Your program printed too much text, so we stopped it."
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
            obtenido = eval(compile(expresion, "<test>", "eval"), espacio)
            fallo = None
        except BaseException as exc:
            fallo = exc
    if fallo is not None:
        r.update(ok=False, error=_info_error(fallo))
        nombre = getattr(fallo, "name", None)
        if isinstance(fallo, NameError) and nombre and nombre in expresion:
            r["nota"] = f"We couldn't find {nombre}. Check that your function is named exactly {nombre}."
        return r
    esperado = ast.literal_eval(prueba["esperado"])
    r["obtenido"] = repr(obtenido)
    r["ok"] = _iguales(obtenido, esperado)
    if obtenido is None and not r["ok"]:
        if salida.getvalue().strip():
            r["nota"] = "Your function printed something but didn't return anything. Did you use print() instead of return?"
        else:
            r["nota"] = "Your function didn't return anything. Did you forget to write return?"
    return r


def _comprobar(codigo, pruebas, prohibidos):
    resultados = []

    usados = _nombres_usados(codigo) & set(prohibidos or [])
    if usados:
        resultados.append({
            "descripcion": "Exercise rules",
            "tipo": "regla",
            "ok": False,
            "nota": "In this exercise you can't use: " + ", ".join(sorted(usados))
                    + ". Try to solve it with what you've learned.",
        })

    espacio_funciones = None   # the program is run once and shared by all expression tests
    error_funciones = None

    for i, prueba in enumerate(pruebas, start=1):
        desc = prueba.get("descripcion") or f"Test {i}"
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
