# Python Notebook

Una plataforma de aprendizaje pequeña y gratuita para un curso de fundamentos de Python. Los estudiantes entran desde la sala de cómputo o desde la casa, leen las lecciones, escriben y ejecutan Python en el navegador y comprueban sus ejercicios con pruebas automáticas. Su trabajo se guarda mientras avanzan. Tú tienes un panel docente que muestra quién resolvió qué, quién está atascado y quién no ha entrado últimamente.

No cuesta nada mantenerla:

- **GitHub Pages** aloja el sitio web (HTML, CSS y JavaScript simples, sin ningún paso de compilación).
- **Pyodide** ejecuta Python dentro del navegador de cada estudiante, así que no se necesita un servidor para correr el código.
- **Supabase** (plan gratuito) guarda los usuarios y el progreso.

Todo lo que ven los estudiantes está en inglés. Algunos nombres internos (los nombres de las páginas y los nombres de los campos dentro de los archivos de contenido) están en español; los estudiantes nunca los ven.

En esta guía, los nombres de botones y menús aparecen tal como se ven en pantalla: en inglés en el sitio, en Supabase y en GitHub.

---

## Qué hay en la carpeta

```
README.es.md          esta guía (README.md: la misma guía en inglés)
index.html            inicio de sesión y cambio de contraseña
inicio.html           página de inicio del estudiante: "continúa donde quedaste", progreso, unidades
leccion.html          página de lección (muestra un archivo Markdown)
ejercicio.html        página de ejercicio: editor, Run, Check, guardado automático
docente.html          panel docente: tabla de progreso, visor de código, exportar CSV
visibilidad.html      solo docentes: elegir qué unidades ve cada curso
css/estilos.css       todos los estilos (modo claro y oscuro)
images/mascot.png     la mascota de la página de entrada y de inicio
js/config.js          ← el único archivo de código que debes editar
js/app.js             funciones compartidas (verificar sesión, cargar el curso, etc.)
js/py-runner.js       ejecuta Python con un límite de tiempo
js/py-worker.js       carga Pyodide en segundo plano
js/harness.py         ejecuta el código del estudiante y las pruebas; pistas de error amigables
content/curso.json    el mapa del curso: unidades, lecciones, ejercicios, fechas de apertura
content/lecciones/    un archivo Markdown por lección
content/ejercicios/   un archivo JSON por ejercicio (enunciado, código inicial, pruebas)
supabase/esquema.sql  tablas de la base de datos, permisos y reglas de seguridad (se ejecuta una vez)
supabase/permisos.sql solo permisos (no se necesita en una instalación nueva; ver Solución de problemas)
supabase/visibilidad.sql  la tabla de Visibilidad, para proyectos creados antes de que existiera
scripts/estudiantes.py     crea cuentas y reinicia contraseñas (se ejecuta en tu computador)
scripts/example_students.csv  ejemplo del formato de la lista de estudiantes
```

---

## Instalación desde cero

Calcula unos 45 minutos. Necesitas un computador con **Python 3** instalado, una cuenta gratuita de **Supabase** y una cuenta gratuita de **GitHub**.

Supabase y GitHub cambian el nombre de sus menús de vez en cuando. Si algo no está exactamente donde dice esta guía, busca la opción más parecida.

### Paso 1. Crear el proyecto en Supabase

1. Entra a **supabase.com**, regístrate y haz clic en **New project**.
2. Ponle un nombre (por ejemplo, `python-notebook`), elige una región cercana a Colombia (por ejemplo, **South America (São Paulo)**) y define una contraseña para la base de datos.
3. Guarda esa contraseña en un lugar seguro. No la necesitas para esta plataforma, pero Supabase la pide en algunas situaciones.
4. Espera uno o dos minutos mientras el proyecto arranca.

> Si tienes un proyecto viejo de un intento anterior, puedes borrarlo (**Project Settings → General → Delete project**) y empezar de nuevo, para no mezclar configuraciones viejas y nuevas.

### Paso 2. Crear las tablas de la base de datos

1. En la barra lateral izquierda, abre **SQL Editor** y crea una **New query**.
2. Abre `supabase/esquema.sql` de la carpeta, copia **todo** su contenido y pégalo en el editor.
3. Presiona **Run**. Deberías ver un mensaje de "Success".

Esto crea tres tablas (`profiles`, `submissions` y `unit_visibility`), le da permiso al sitio web para usarlas y agrega las reglas de seguridad: cada estudiante solo puede ver su propio trabajo, solo el docente puede ver el de todos, y solo el docente puede cambiar qué unidades ve cada curso.

Ejecuta este archivo **una sola vez**. Si lo ejecutas de nuevo aparecen errores de "already exists" (ya existe), que no hacen daño pero confunden.

### Paso 3. Desactivar el registro público

Ve a **Authentication → Sign In / Providers**, **desactiva** la opción **Allow new users to sign up** y guarda.

Esto es importante: sin este paso, cualquiera que encuentre tu sitio podría crear una cuenta. Tú vas a crear todas las cuentas con el script, y el script funciona aunque el registro esté desactivado.

### Paso 4. Encontrar tus tres valores

Necesitas tres valores de Supabase. Abre **Project Settings** (el ícono de engranaje en la parte inferior de la barra lateral).

| Valor | Dónde encontrarlo | Cómo se ve | A dónde va |
|---|---|---|---|
| **Project URL** | **Data API** (en *Integrations*), o el botón **Connect** en la parte superior del proyecto | `https://abcdefghijklmnop.supabase.co` | `config.js` y el script |
| **Publishable key** | **API Keys** → *Publishable key* → la fila **default** → copiar | `sb_publishable_...` | Solo `config.js` |
| **Secret key** | **API Keys** → *Secret keys* → la fila **default** → mostrar y copiar | `sb_secret_...` | Solo el script |

Si la Project URL que copias termina en `/rest/v1/`, borra esa parte: solo necesitas `https://<letras>.supabase.co`.

Usa estas claves nuevas, no las "legacy": Supabase planea retirar las claves legacy en 2027.

> **La Project URL no es la dirección de la barra del navegador** (`https://supabase.com/dashboard/project/...`). Esa no funciona.
>
> **Trata la secret key como una contraseña maestra.** Puede hacer cualquier cosa en tu base de datos. Nunca la pongas en `config.js`, en GitHub, en una captura de pantalla ni en ningún lugar donde la vean los estudiantes. Si alguna vez se filtra, bórrala en la página API Keys y crea una nueva.

### Paso 5. Conectar el sitio web

Abre `js/config.js` en un editor de texto (el Bloc de notas sirve; VS Code es más cómodo) y completa:

```js
SUPABASE_URL: "https://abcdefghijklmnop.supabase.co",   // tu Project URL
SUPABASE_ANON_KEY: "sb_publishable_...",                 // tu Publishable key
```

También puedes cambiar `APP_NAME` (el nombre que aparece arriba en todas las páginas) y `COURSE_SUBTITLE` (aparece en la página de entrada). `MASCOT` es la imagen que aparece en la página de entrada y en la de inicio (`images/mascot.png` por defecto). Ponle `""` para ocultarla, o pon otra imagen en la carpeta `images` y cambia el nombre. Funciona mejor un PNG con fondo transparente, recortado cerca del dibujo.

La publishable key está hecha para ser pública. Lo que mantiene privados los datos de cada estudiante son las reglas de seguridad del Paso 2.

### Paso 6. Crear tu cuenta de docente

Abre una terminal (en Windows, **PowerShell**), ve a la carpeta `scripts` y ejecuta:

```
cd ruta\a\cuaderno-python\scripts
python estudiantes.py teacher profe
```

(`profe` es el nombre de usuario. Puedes elegir otro, usando letras minúsculas, números y guiones).

El script pide la **Project URL** y la **secret key**. Cuando pegas la clave, no aparece nada en pantalla; es normal. Si **Ctrl + V** no funciona ahí, pega con **clic derecho**. Presiona Enter y el script muestra una **contraseña temporal**. Anótala.

Para no pegar la URL y la clave cada vez, puedes definirlas una vez por ventana de terminal:

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

Se olvidan al cerrar la ventana, que es justo lo que quieres con la secret key.

### Paso 7. Probarlo en tu computador

Las páginas cargan archivos de la carpeta, así que no funciona abrir `index.html` con doble clic. En su lugar, inicia un pequeño servidor web local. En una terminal, ve a la **carpeta principal del proyecto** (no a `scripts`) y ejecuta:

```
python -m http.server 8000
```

Abre **http://localhost:8000** en el navegador y entra con `profe` y la contraseña temporal. El sitio te pide crear tu propia contraseña y luego te lleva al panel docente.

Haz clic en **Home** para ver la vista del estudiante, abre un ejercicio y presiona **Check**. La primera vez, Python tarda unos segundos en cargar. Si puedes ejecutar código y ver los resultados de las pruebas, todo está conectado.

Detén el servidor con **Ctrl + C** en la terminal.

### Paso 8. Publicar en GitHub Pages

1. En **github.com**, crea un repositorio nuevo (por ejemplo, `python-notebook`). Puede ser público.
2. Sube el contenido de la carpeta del proyecto (**Add file → Upload files**, y arrastra todo lo que hay dentro de `cuaderno-python`). El archivo `index.html` debe quedar en el nivel principal del repositorio, no dentro de una subcarpeta.
3. Antes de subir, revisa que en la carpeta `scripts` no haya listas de estudiantes ni archivos CSV de credenciales. Solo debe estar `example_students.csv`.
4. Ve a **Settings → Pages**. En *Build and deployment*, elige **Deploy from a branch**, rama **main**, carpeta **/ (root)**, y guarda.
5. Después de uno o dos minutos, tu sitio estará en `https://TU-USUARIO.github.io/python-notebook/`.

Entra una vez allí para confirmar que funciona igual que en tu computador.

### Paso 9. Crear las cuentas de los estudiantes

Haz un archivo CSV por curso (Excel puede guardar en CSV) con tres columnas, como `scripts/example_students.csv`. Los encabezados van en inglés:

```
name,username,group
Ana Pérez,8a-01,8A
Juan David Rojas,8a-02,8A
```

Guárdalo en la carpeta `scripts` (por ejemplo, `8a.csv`) y ejecuta:

```
python estudiantes.py create 8a.csv
```

El script crea todas las cuentas y escribe **`credentials-8a.csv`** junto a tu archivo, con la contraseña temporal de cada estudiante. Entrega a cada estudiante su usuario y su contraseña. La primera vez que entren, elegirán su propia contraseña.

Algunas notas:

- **Los usuarios como `8a-07`** funcionan bien: son cortos, no tienen información personal y el curso se ve de inmediato.
- **Los nombres reales se quedan en tu computador.** La base de datos solo guarda el usuario y el curso. Mantén privadas las listas de estudiantes y los archivos de credenciales, y nunca los subas a GitHub (el `.gitignore` incluido ayuda, pero revisa de todos modos).
- **Nunca se envía ningún correo.** Por dentro, cada usuario se convierte en una dirección inventada como `8a-07@alumnos.example.com`. Si Supabase alguna vez rechaza ese dominio, cambia `EMAIL_DOMAIN` al mismo valor nuevo en `js/config.js` y en `scripts/estudiantes.py`, *antes* de crear cuentas.

Ya estás listo para la clase.

---

## El curso de grado 9 (semanas 7 a 29)

La carpeta `content` contiene el plan de indagación de grado 9, adaptado al sitio:

- **Review the fundamentals** (repaso de fundamentos): una sección opcional en la parte superior de la página de inicio, cerrada por defecto. Tiene 10 lecciones detalladas sobre todo lo que necesita la semana 7 (qué es un programa, `print`, números, variables y `+=`, tipos de datos y conversión, `input`, armar mensajes, comparaciones True/False, leer mensajes de error) y 34 ejercicios de práctica, numerados según la lección. No cuenta para la barra de progreso semanal ni para la columna "Solved" del panel docente, y está siempre abierta. Los estudiantes pueden usarla para ponerse al día después de los lunes perdidos; puedes ver su trabajo eligiéndola en el menú **Unit** del panel.
- **Una unidad por semana**, desde la semana 7 (if/else) hasta la semana 23 (listas y tuplas), más una unidad para el proyecto (semanas 24 a 28) y la muestra final (semana 29). Las semanas 13 y 19 son de repaso antes de las evaluaciones escritas.
- **La lección de cada semana** contiene la parte de indagación de la sesión: la pregunta guía, el código para leer y predecir (con una calificación de confianza), los bloques "Check your prediction", las tarjetas de investigación, la tarea de creación (Make) y las preguntas de salida para la bitácora.
- **El laboratorio de cada semana** es un espacio libre con el código inicial de esa semana, para las tarjetas de investigación.
- **7 u 8 ejercicios de práctica por semana**, marcados ★ (calentamiento), ★★ (básico) y ★★★ (reto), con ejercicios de "Bug hunt" (encontrar el error) en el camino. Alcanza para una sesión completa de 40 minutos, y sobra para la casa.
- **Espacios libres** para el trabajo que se califica o que es personal: *My Guess the Number game* (semana 12), *My game, refactored* (semana 18) y *My project* (semanas 24 a 28). Reemplazan pegar código en Teams.

Los ejercicios solo usan lo que los estudiantes han visto hasta esa semana: nada de `and`/`or` antes de la semana 14, nada de funciones antes de la semana 17 y nada de `%` antes de la semana 21.

**Las soluciones de referencia** de todos los ejercicios con pruebas automáticas están en `solutions.md`, que se entrega por separado. Mantén ese archivo en privado: **no lo subas a GitHub**, porque el repositorio del sitio puede ser público.

## Escribir contenido del curso

Nunca necesitas tocar el código para agregar contenido. Edita los archivos de `content/`, súbelos a GitHub y el sitio se actualiza en uno o dos minutos.

Los archivos de contenido usan nombres de campos en español:

| Campo | Significado | Campo | Significado |
|---|---|---|---|
| `titulo` | título | `pruebas` | pruebas |
| `desbloqueo` | fecha de apertura | `descripcion` | descripción de una prueba |
| `lecciones` | lecciones | `expresion` | expresión que se evalúa |
| `ejercicios` | ejercicios | `esperado` | resultado esperado |
| `enunciado` | instrucciones | `tipo` / `salida` | tipo / salida |
| `codigo_inicial` | código inicial | `entradas` | entradas |
| `usa_input` | usa input() | `entradas_ejemplo` | entradas de ejemplo |
| `no_usar` | no permitido | `definir` | funciones que deben definirse |
| `etiqueta` | nombre de la unidad, p. ej. "Week 7" | `libre` | espacio libre (sin pruebas) |
| `repaso` | unidad de repaso (práctica opcional) | `descripcion` | descripción corta de una unidad de repaso |

### El mapa del curso: `content/curso.json`

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

`desbloqueo` es una fecha opcional (AAAA-MM-DD) desde la cual los estudiantes pueden abrir la unidad. Antes de esa fecha ven el título con "Opens on…", pero no pueden abrir nada. Una unidad sin `desbloqueo` está abierta de inmediato. La página **Visibility** (ver *Día a día*) puede cambiar esto para cada curso, así que quizás no necesites fechas.

`etiqueta` es el nombre con el que aparece la unidad en el sitio ("Week 8"). Sin ella, las unidades se llaman "Unit 1", "Unit 2" y así sucesivamente, en orden.

Una unidad marcada con `"repaso": true` aparece como una sección de **repaso** desplegable en la parte superior de la página de inicio, en lugar de en la lista semanal, con su `descripcion` como subtítulo. Sus ejercicios no cuentan para el progreso. Úsala para práctica opcional.

Un ejercicio marcado con `"libre": true` es un **espacio libre**: no tiene pruebas ni botón Check. Los estudiantes ejecutan código todas las veces que quieran, se guarda automáticamente y tú puedes leerlo en el panel docente. Los espacios libres no cuentan para el progreso. El curso los usa para el laboratorio de cada semana, para el juego Guess the Number y para el proyecto final.

Cada `id` de lección debe coincidir con un archivo en `content/lecciones/`, y cada `id` de ejercicio con un archivo en `content/ejercicios/`. Usa letras minúsculas, números y guiones en los `id`, y no le cambies el `id` a un ejercicio cuando los estudiantes ya lo empezaron: su trabajo guardado está ligado a ese `id`.

### Lecciones: `content/lecciones/<id>.md`

Markdown simple. Los bloques de código marcados como `python` se colorean:

````markdown
# Variables

A **variable** is like a labeled box.

```python
name = "Valentina"
print(name)
```
````

Para que los estudiantes predigan antes de ver una respuesta, pon la respuesta en un bloque "Check your prediction". Deja una línea en blanco después de la línea `<summary>` y antes de `</details>`:

````markdown
<details>
<summary>Check your prediction</summary>

```text
True
False
```

</details>
````

Usa `text` en los bloques que muestran lo que imprime un programa, para que no se coloreen como código.

Puedes insertar presentaciones. En Canva usa **Share → Embed**, o en Google Slides **File → Share → Publish to web → Embed**, y pega el código `<iframe>` directamente en el archivo Markdown. La página ajusta el tamaño automáticamente.

### Ejercicios: `content/ejercicios/<id>.json`

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

En JSON, un salto de línea dentro de un texto se escribe `\n`, y las comillas dentro de un texto se escriben `\"`. Si una página de ejercicio muestra un error después de editarla, pega el archivo en **jsonlint.com** para encontrar la equivocación.

Hay dos tipos de pruebas, y un mismo ejercicio puede combinarlas.

**Las pruebas de función** llaman a la función del estudiante y comparan lo que *retorna*. `esperado` se escribe como se escribiría en Python: `"True"`, `"8"`, `"'hello'"`, `"[1, 2]"`. Los decimales se comparan con una pequeña tolerancia, y `True` nunca se acepta en lugar de `1`.

```json
{ "descripcion": "Right at the limit: 4.5", "expresion": "is_passing(4.5)", "esperado": "True" }
```

**Las pruebas de salida** ejecutan el programa completo, responden sus preguntas de `input()` con los valores que tú indicas y comparan lo que *imprime*. Se ignoran los espacios al final de las líneas y las líneas en blanco al final. El texto de la pregunta dentro de `input("...")` no forma parte de la salida, así que los estudiantes pueden redactar sus preguntas como quieran.

```json
{ "tipo": "salida", "descripcion": "5 and 7", "entradas": ["5", "7"], "esperado": "The sum is 12" }
```

Campos opcionales:

- `"usa_input": true` muestra desde el principio la caja **Inputs for input()**. (También aparece sola en cuanto el código del estudiante usa `input()`).
- `"entradas_ejemplo": "5\n7"` llena esa caja de antemano.
- `"no_usar": ["max", "sorted"]` indica nombres que el estudiante no puede usar. Si usa alguno, el ejercicio falla con un mensaje claro.
- `"definir": ["ask_question"]` indica funciones que el estudiante debe escribir con `def`. Sirve cuando el objetivo del ejercicio es escribir una función y la salida por sí sola no lo demuestra.

Las pruebas de función ejecutan el programa una vez **sin entradas**, así que un ejercicio con pruebas de función no debe llamar a `input()` fuera de una función. Usa pruebas de salida para los programas que hacen preguntas.

Los ejercicios de funciones son los más fáciles de probar de forma confiable, y llevan a los estudiantes a usar `return`, que vale la pena practicar. Cuando una prueba falla porque una función imprimió en vez de retornar, el estudiante recibe una pista específica.

---

## Día a día

**Un estudiante olvidó su contraseña:**

```
python estudiantes.py reset 8a-07
```

Muestra una contraseña temporal nueva. Su progreso se conserva, y elige una contraseña nueva la próxima vez que entre.

**Agregar un estudiante después:** pon solo ese estudiante en un CSV nuevo y ejecuta `create` otra vez.

**El panel docente (Teacher panel):** cada fila es un estudiante y cada columna un ejercicio. Usa el menú **Unit** para ver una semana a la vez: se abre en la última semana que está abierta para al menos un curso.

- **✓ verde** significa resuelto.
- **Amarillo** significa empezado; el número es cuántas veces presionó **Check**. Un número alto suele indicar que está atascado.
- **Un cuadro punteado** significa que no lo ha empezado.
- **Un ✎ azul** marca un espacio libre donde el estudiante guardó código.
- **Haz clic en cualquier celda de color** para leer el código actual de ese estudiante.
- **La última columna** se pone roja cuando alguien lleva 14 días sin trabajar (cámbialo con `DIAS_INACTIVO` en `config.js`).
- **Download CSV** exporta el progreso del curso seleccionado, para tu libro de notas.

**Elegir qué ve cada curso:** abre **Visibility** en la barra superior. Cada fila es una unidad y cada columna es un curso (el `group` de tu CSV de estudiantes). En cada celda, elige:

- **Open (abierta):** los estudiantes pueden leer las lecciones y hacer los ejercicios.
- **Locked (bloqueada):** los estudiantes ven el título con "Coming soon", pero no pueden abrirla.
- **Hidden (oculta):** los estudiantes no ven la unidad.
- **Default (por defecto):** sigue la fecha de la unidad en `curso.json`, y está abierta si no tiene fecha. Los colores muestran lo que los estudiantes realmente ven; un borde punteado indica que la celda está en Default.

La columna **All classes** cambia una unidad para todos los cursos a la vez. Los cambios se guardan de inmediato; los estudiantes los ven la próxima vez que carguen una página. Una rutina típica: al comenzar el año, pon todas las semanas futuras en **Locked** (o **Hidden**) para todos los cursos, y abre cada semana para cada curso cuando ese curso haya tenido la sesión. Así, un curso que perdió un lunes por un festivo simplemente va una semana atrás. Como docente, tú siempre ves todas las unidades.

Dos cosas para tener en cuenta: la columna "Solved" del panel docente solo cuenta las unidades abiertas para el curso de cada estudiante, y la unidad que muestra el menú por defecto es la última semana abierta para algún curso. Bloquear es una herramienta de clase, no un candado de seguridad: los archivos de las lecciones son públicos en GitHub Pages, así que un estudiante decidido podría leer directamente una lección bloqueada.

**Antes de la clase:** mirar el panel dos minutos muestra en qué ejercicio tuvo más problemas la mayoría del curso. Es un buen punto de partida para la sesión.

**Un año escolar nuevo:** borra las cuentas del año anterior en Supabase (**Authentication → Users**; su progreso se borra con ellas), crea las cuentas nuevas con el script y configura **Visibility** para los cursos nuevos (o actualiza las fechas de apertura en `curso.json`, si las usas).

---

## Bueno saber

**Las pruebas se ejecutan en el navegador del estudiante.** Un estudiante decidido podría encontrar las respuestas esperadas con las herramientas de desarrollador del navegador, o marcar un ejercicio como resuelto sin resolverlo. Trata el trabajo con revisión automática como práctica y como nota de cumplimiento, y deja la evaluación calificada para trabajos que supervises o que los estudiantes tengan que explicar.

**Los ciclos infinitos están controlados.** A los 5 segundos el programa se detiene y se le explica al estudiante por qué, sin que la página se congele. También se corta la salida cuando un programa imprime una cantidad enorme de texto.

**Python se carga una vez por equipo.** La primera vez que un computador abre un ejercicio, descarga Python (unos 10 MB). Después queda guardado y arranca en pocos segundos. Si la conexión de la sala es lenta, abre un ejercicio una vez en cada computador antes de la primera clase.

**Navegadores:** Chrome, Edge o Firefox recientes. Los navegadores muy viejos no pueden ejecutar Pyodide.

**Es difícil perder el trabajo.** El código se guarda en el servidor unos segundos después de que el estudiante deja de escribir, y se guarda una copia en el navegador por si se cae la conexión.

**Plan gratuito de Supabase:** los proyectos gratuitos se pausan después de una semana, más o menos, sin actividad. Durante el año escolar, el trabajo de los estudiantes lo mantiene activo. Después de vacaciones largas quizás debas presionar **Restore project** en el panel de Supabase. Revisa de vez en cuando los límites del plan gratuito de Supabase, porque pueden cambiar.

---

## Solución de problemas

**"Error 405" o "the server answered with a web page":** la Project URL está mal. Usa la de **Data API** (`https://....supabase.co`), no la de la barra de direcciones del navegador. Si antes definiste `$env:SUPABASE_URL` en esa ventana, revísala con `echo $env:SUPABASE_URL`.

**La página Visibility dice "The visibility settings aren't set up yet":** tu base de datos se creó antes de esta función. Ejecuta una vez `supabase/visibilidad.sql` en el SQL Editor y recarga la página. Se puede ejecutar más de una vez sin problema.

**"permission denied for table profiles" (error 403 / 42501):** las tablas no tienen permisos. Pasa si la base de datos se creó con una versión anterior de `esquema.sql`. Ejecuta `supabase/permisos.sql` en el SQL Editor y vuelve a ejecutar tu comando.

**"the key was not accepted" (error 401):** usaste la publishable key, una clave legacy o la contraseña de la base de datos. El script necesita la **secret key** (`sb_secret_...`).

**"A user with this email address has already been registered":** ese usuario ya existe. Para tu propia cuenta de docente, simplemente ejecuta otra vez `python estudiantes.py teacher profe`: le asigna una contraseña nueva a la cuenta existente. Para un estudiante, usa `reset`.

**"Wrong username or password" con una contraseña que acabas de copiar:** revisa esto en orden.

1. *Usa la contraseña más reciente.* Cada vez que ejecutas `teacher` o `reset`, la contraseña temporal anterior deja de funcionar.
2. *Revisa que el sitio y el script usen el mismo proyecto.* La `SUPABASE_URL` de `js/config.js` debe ser la misma Project URL que le diste al script. Es fácil equivocarse después de crear un proyecto nuevo.
3. *Revisa que la cuenta exista con la dirección correcta.* En Supabase, abre **Authentication → Users**. Deberías ver `profe@alumnos.example.com` (o tu usuario). Lo que va después de `@` debe coincidir con `EMAIL_DOMAIN` en `js/config.js`.
4. *Recarga el sitio sin caché* (**Ctrl + Shift + R**), para que el navegador no use un `config.js` viejo.
5. *Pide una contraseña nueva y escríbela a mano:* `python estudiantes.py reset profe`.
6. *Deja que el script revise todo por ti:* `python estudiantes.py check profe`. Compara `js/config.js` con el proyecto que usa el script, busca la cuenta e intenta entrar exactamente como lo hace el sitio, y te dice qué parte falla.

**"Password login is turned off in Supabase":** en el Paso 3 se desactivó el proveedor **Email** en lugar de la opción de registro. En **Authentication → Sign In / Providers**, vuelve a activar el proveedor **Email** y deja desactivada solo la opción **Allow new users to sign up**.

**El sitio dice "Couldn't load your profile" o no muestra nada después de entrar:** revisa que `SUPABASE_URL` y `SUPABASE_ANON_KEY` en `js/config.js` estén correctas, y que `esquema.sql` se haya ejecutado sin errores.

**Una página de ejercicio o de lección muestra un error:** el nombre del archivo no coincide con su `id` en `curso.json`, o el JSON tiene un error de escritura (revísalo en jsonlint.com).

**Los cambios no aparecen en el sitio web:** después de subir archivos, GitHub Pages necesita uno o dos minutos para publicarlos (en la pestaña **Actions** debe aparecer un chulo verde), y los navegadores pueden guardar una copia vieja hasta por **10 minutos**. Espera y recarga con **Ctrl + Shift + R**, o revisa en una ventana privada. Para ver lo que el sitio está entregando de verdad, abre un archivo agregando `?v=check` al final, por ejemplo `…github.io/tu-repositorio/js/app.js?v=check`.

**Una página dice "This page couldn't start", o se queda en "Loading…":** el código de la página no pudo arrancar. Normalmente hay archivos de actualizaciones distintas en el sitio, o un archivo quedó en la carpeta equivocada (por ejemplo, `app.js` en el nivel principal en lugar de dentro de `js/`). Sube todos los archivos de la última actualización, conservando las carpetas `js` y `css`, y espera como se explica arriba. El mensaje incluye un detalle técnico; la consola del navegador (**F12 → Console**) muestra el error exacto.

**Funciona en GitHub pero no en `localhost` (o al revés):** `python -m http.server` entrega la carpeta desde la que se inició. Si tienes más de una copia del proyecto en tu computador, detén el servidor (**Ctrl + C**), ve a la carpeta correcta e inícialo de nuevo.

---

## Ideas para la próxima versión

Encajan en el diseño actual sin reescribir nada:

- **Quices de recuerdo** que mezclen preguntas de unidades anteriores, como calentamiento al comienzo de cada clase.
- **Paquetes para festivos** que se abran solos los lunes festivos, para que una clase perdida se convierta en práctica.
- **Seguimiento de lecciones**, para que el panel muestre quién leyó cada lección.
- **Un tutor con IA** que dé pistas en lugar de respuestas. Funcionaría en una Supabase Edge Function, para que la clave de la API nunca llegue al navegador.
