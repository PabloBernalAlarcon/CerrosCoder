# Variables y preguntas con `input()`

Una **variable** es como una caja con nombre donde guardamos un dato para usarlo después.

```python
nombre = "Valentina"
edad = 14
print(nombre, "tiene", edad, "años")
```

El signo `=` no significa "igual" como en matemáticas: significa **guarda esto en la caja**.

## Reglas para los nombres

Los nombres de variables van en minúsculas, sin espacios ni tildes, y no pueden empezar con un número. Si necesitas varias palabras, únelas con guion bajo: `nota_final`, `numero_de_goles`.

## Preguntar al usuario

`input()` hace una pregunta y espera a que la persona escriba algo:

```python
ciudad = input("¿En qué ciudad vives? ")
print("¡Qué bien!", ciudad, "es una gran ciudad.")
```

En esta plataforma, lo que el usuario "escribe" lo pones en la caja **Entradas para input()**, una respuesta por línea.

## Mezclar texto y variables con f-strings

Si pones una `f` antes de las comillas, puedes meter variables entre llaves `{ }`:

```python
nombre = "Samuel"
print(f"Hola, {nombre}. Bienvenido.")
```

## ¡Cuidado! `input()` siempre devuelve texto

Aunque escribas un número, `input()` lo entrega como texto. Para hacer cuentas, conviértelo con `int()` (números enteros) o `float()` (números con decimales):

```python
goles = int(input("¿Cuántos goles hizo tu equipo? "))
print(f"El doble serían {goles * 2} goles")
```

> Si olvidas el `int()`, `"3" + "4"` da `"34"`: Python pega los textos en lugar de sumarlos.
