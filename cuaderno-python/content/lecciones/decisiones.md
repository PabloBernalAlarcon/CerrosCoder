# Decisiones con `if`, `elif` y `else`

Los programas pueden tomar decisiones. Para eso hacemos una **pregunta** que Python responde con `True` (verdadero) o `False` (falso).

## Comparaciones

```python
print(8 > 5)     # True
print(3 == 4)    # False  (== pregunta "¿son iguales?")
print(7 != 2)    # True   (!= pregunta "¿son distintos?")
print(5 >= 5)    # True
```

No confundas `=` (guardar en una variable) con `==` (comparar).

## if y else

```python
temperatura = 28

if temperatura > 25:
    print("Hace calor")
else:
    print("Está fresco")
```

Igual que en las funciones, los dos puntos `:` y la sangría marcan qué código depende de la condición.

## elif: más de dos caminos

```python
nota = 5.8

if nota >= 6:
    print("Excelente")
elif nota >= 4.5:
    print("Aprobado")
else:
    print("Hay que reforzar")
```

Python revisa las condiciones en orden y ejecuta **solo la primera** que sea verdadera.

## Devolver True o False desde una función

Una comparación ya es `True` o `False`, así que puedes devolverla directamente:

```python
def es_mayor_de_edad(edad):
    return edad >= 18

print(es_mayor_de_edad(14))   # False
```
