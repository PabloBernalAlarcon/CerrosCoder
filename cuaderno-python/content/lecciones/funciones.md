# Funciones: `def` y `return`

Ya usaste funciones que vienen con Python: `print()`, `input()`, `int()`. Ahora vas a crear las tuyas.

Una **función** es un pequeño programa con nombre que recibe datos, hace algo con ellos y **devuelve** un resultado.

```python
def triple(numero):
    return numero * 3

print(triple(5))    # 15
print(triple(10))   # 30
```

Las partes son:

- `def` le dice a Python que vas a definir una función.
- `triple` es el nombre de la función.
- `numero` es el **parámetro**: el dato que recibe.
- Los dos puntos `:` y la **sangría** (los 4 espacios) indican qué código pertenece a la función.
- `return` devuelve el resultado a quien la llamó.

## `return` no es lo mismo que `print`

Esta es la confusión más común. `print()` solo **muestra** algo en pantalla. `return` **entrega** el resultado para poder usarlo después:

```python
def doble_mal(n):
    print(n * 2)      # lo muestra, pero no lo devuelve

def doble_bien(n):
    return n * 2      # lo devuelve

total = doble_bien(4) + 1    # funciona: total vale 9
```

En los ejercicios de funciones, las pruebas usan lo que tu función **devuelve**. Si usas `print` en lugar de `return`, las pruebas fallarán.

## Varios parámetros

```python
def area_rectangulo(base, altura):
    return base * altura

print(area_rectangulo(3, 4))   # 12
```
