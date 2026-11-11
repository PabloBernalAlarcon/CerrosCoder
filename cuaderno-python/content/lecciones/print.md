# Hablar con la computadora: `print()`

Un **programa** es una lista de instrucciones que la computadora sigue en orden, de arriba hacia abajo. La primera instrucción que vamos a aprender es `print()`, que muestra algo en la pantalla.

```python
print("¡Hola, mundo!")
print("Estoy aprendiendo Python")
```

El texto va entre **comillas**. Para Python, todo lo que está entre comillas es un *texto* (en programación se le dice *string*).

## Números y cuentas

Los números van **sin** comillas, y Python puede hacer cuentas:

```python
print(7 + 5)      # suma: 12
print(10 - 3)     # resta: 7
print(4 * 6)      # multiplicación: 24
print(15 / 2)     # división: 7.5
```

Fíjate en la diferencia: `print("7 + 5")` muestra el texto `7 + 5`, pero `print(7 + 5)` muestra `12`.

## Varias cosas a la vez

Si separas con comas, `print()` muestra todo en la misma línea con un espacio en medio:

```python
print("Tengo", 14, "años")
```

## Comentarios

Lo que escribes después de `#` es un **comentario**: Python lo ignora. Sirve para dejar notas para ti o para otras personas.

> **Errores comunes:** olvidar cerrar las comillas o el paréntesis, y escribir `Print` con mayúscula. Python distingue entre mayúsculas y minúsculas.
