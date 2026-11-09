# JFLAP UWU

Versión modificada de JFLAP por el odio que se tomo a la primer versión :3.

## Descarga directa

Descarga la última versión disponible de **JFLAP UWU v6** desde el siguiente enlace:

<p align="center">
  <a href="https://github.com/TraceVoid/JFLAP/releases/download/V6/JFLAP_UWU_v6.jar">
    <img src="https://img.shields.io/badge/Descargar-JFLAP_UWU_v6-blue?style=for-the-badge&logo=github" alt="Descargar JFLAP UWU v6">
  </a>
</p>

También puedes consultar el [repositorio del proyecto](https://github.com/TraceVoid/JFLAP) y sus [releases](https://github.com/TraceVoid/JFLAP/releases).

## Requisitos

- **JDK / JRE 21 o superior** (`java -version` debe mostrar 21+).

## Ejecutar

```
java -jar JFLAP_UWU_v6.jar
```

Tema claro en lugar del oscuro: `java -Djflap.dark=false -jar JFLAP_UWU_v6.jar`
Alternar el tema en caliente: **Ctrl + Shift + D**.

---

## Novedades

### 1. Borrar con Supr (selección múltiple)

Selecciona varios nodos y/o transiciones (con el rectángulo de selección o con clics) y pulsa **Supr** (en Mac, Retroceso). Se borran todos de una vez, incluidas las transiciones conectadas a los nodos borrados.

- Se puede deshacer con **Ctrl + Z** (rehacer: Ctrl + Shift + Z o Ctrl + Y).
- No actúa mientras escribes en una caja de texto o editas una tabla.

### 2. Botón **Auto ▶**, velocidad y visor de cinta

En la barra inferior de la simulación (junto a Step, Reset, Freeze…):

| Control | Función |
|---|---|
| **Auto ▶** | Avanza automáticamente. Mientras corre, el botón cambia a **Pause ⏸**. |
| Campo `ms` | Milisegundos entre ticks. **Mínimo 1 ms** (máximo 10000, por defecto 500). Se puede cambiar mientras corre. |
| Campo `× steps` | **Pasos de la máquina por tick** (1 – 1 000 000, por defecto 1). La pantalla se refresca una sola vez por tick, así que subirlo acelera mucho las cadenas largas. |
| Etiqueta de resultado | Muestra **Accepted** o **Rejected** al terminar. |
| **Tape** | Abre el visor de cinta completa (ver abajo). |
| **Tape at end** | Si está marcada (por defecto), al terminar Auto se abre solo el visor de cinta. |

Se detiene solo cuando alguna configuración **acepta**, o cuando ya no queda ninguna configuración válida (**rechaza**). **Reset** también lo detiene. Si la máquina entra en un bucle infinito, no se detiene sola: usa **Pause**.

**Velocidad (medido con una máquina que recorre una cadena de `O`):** con 1 ms y 1 paso por tick, 3000 pasos tardaron unos 3.5 s; con 100 pasos por tick, 0.15 s; una cadena de 20 000 caracteres con 2000 pasos por tick terminó en 0.6 s. La velocidad real depende del equipo.

#### Visor de cinta (**Tape**)

La simulación solo dibuja una ventana de la cinta alrededor del cabezal, por lo que en cadenas largas no se ve el resultado final. El visor muestra **toda** la cinta:

- Contenido completo de cada cinta (con ajuste de línea), con el **cabezal resaltado en naranja** y la vista desplazada hasta él.
- **Content without blanks:** el contenido sin los blancos de los extremos (seleccionable, con botón **Copy content**).
- **Output (head → next blank):** lo que hay desde el cabezal hasta el siguiente blanco.
- **Symbol count:** cuántas veces aparece cada símbolo (por ejemplo `# × 1   O × 20000`), útil para máquinas que cuentan.
- Se actualiza solo con **Step**, **Auto** y **Reset** mientras está abierto.
- Muestra la configuración seleccionada; si no hay ninguna, la aceptada; si no, las activas. Con varias configuraciones (máquinas no deterministas) aparecen en pestañas.

### 3. Notas legibles y con formato

El texto de las notas ahora es oscuro fijo sobre su fondo, por lo que se lee igual en tema claro y oscuro.

**Clic derecho sobre una nota** abre el menú:

- **Font / size…** — familia, tamaño, negrita, cursiva.
- **Text color…** y **Background color…**
- **Box size…** — ancho y alto de la caja (el texto se ajusta en varias líneas).
- **Auto box size** — la caja vuelve a ajustarse sola al texto.
- **Reset style**

(Para crear una nota: clic derecho en un espacio vacío del lienzo → **Add Note**.)

### 4. Color de nodos

**Clic derecho sobre un nodo → Color… / Reset color.** El color se aplica al nodo y a todos los nodos que estén seleccionados. El nombre del nodo cambia a blanco o negro automáticamente según el contraste.

### 5. Alfabetos en las transiciones (`\d`, `\w`, `\W`…)

En el campo **Read** de una transición de Turing (y en las etiquetas de autómatas finitos) se pueden usar clases de caracteres:

| Expresión | Coincide con |
|---|---|
| `\d` | dígitos `0-9` |
| `\D` | cualquier carácter que no sea dígito |
| `\w` | letras y dígitos `A-Za-z0-9` |
| `\W` | caracteres especiales (ni letra/dígito ASCII, ni espacio): `$ # ! - _ …` |
| `\s` / `\S` | espacio en blanco / no espacio en blanco |

Pueden usarse solos o dentro de corchetes, combinados con rangos y con negación:

```
[\d]        dígitos
[\w]        = [A-Za-z0-9]
[\W]        caracteres especiales
[\dA-F]     dígitos o A–F (hexadecimal)
[^\d]       cualquier cosa menos dígitos
[\d\W]      dígitos o caracteres especiales
[ABCD]       rangos
```

Notas:

- `\D`, `\W` y `\S` **no** coinciden con el blanco de la cinta (□). Para detectar el final de la cadena usa □ de forma explícita.
- `\d` ya no significa la letra "d" literal. Para una barra invertida o un corchete literal escribe `\\` o `\[`.
- En el campo **Write** se sigue usando un solo símbolo, o `~` para conservar el que ya estaba en la cinta.
- Funciona con una o varias cintas.
- No está conectado a los autómatas de pila (PDA).

**Ejemplo:** máquina que acepta cadenas formadas solo por dígitos:

```
q0 --[\d] ; ~ , R--> q0
q0 --□    ; □ , S--> q1      (q1 es final)
```

Acepta `12345` y rechaza `12a45`.

### 6. Tabla de reglas para Máquinas de Turing

Permite construir y editar la máquina **como tabla**, sin depender solo del diagrama. Se abre de tres formas (solo en máquinas de Turing):

- botón **Table** en la barra de herramientas del editor,
- clic derecho en un espacio vacío del lienzo → **Transition table…**,
- atajo **Ctrl + Shift + T**.

La ventana tiene dos pestañas:

**Transitions** — una fila por regla: `From | Read | Write | Move | To`. Con varias cintas, las columnas Read/Write/Move se repiten por cinta (`Read 1, Write 1, Move 1, Read 2, …`).

- **Read / Write:** un símbolo. Vacío = blanco (□). `~` en Write = conservar el símbolo. Read acepta además `!a`, `[a-z]`, `[\d]`, `\w`, `\W`… (ver sección 5).
- **Move:** `R`, `L` o `S` (lista desplegable).
- Si escribes en From/To un nombre de estado que no existe, **se crea automáticamente**.
- Botones: **Add rule** (la nueva fila empieza en el estado "To" de la regla seleccionada, para encadenar), **Duplicate**, **Delete rule**.

**States** — una fila por estado: nombre, casilla **Initial** (solo uno) y **Final**.

- Al renombrar un estado, las reglas que lo usan se actualizan solas.
- **Add state** / **Delete state** (borrar un estado elimina también sus reglas).

**Aplicar y sincronizar**

- **Apply** escribe la tabla en el diagrama. Se valida todo antes: si una fila es inválida (por ejemplo, Read con más de un símbolo) aparece un mensaje con el número de fila y no se cambia nada. Se puede **deshacer con Ctrl + Z**.
- Las reglas que no cambiaron se conservan tal cual (incluida la curva de la flecha en el diagrama).
- Los estados nuevos se colocan automáticamente en una cuadrícula libre del lienzo.
- Si dibujas o deshaces en el diagrama, la tabla **se refresca sola** (siempre que no tengas ediciones pendientes). **Refresh** descarta tus ediciones y recarga desde el diagrama.
- Si el diagrama cambió mientras tenías ediciones pendientes (por ejemplo, con deshacer), Apply lo avisa y pide pulsar Refresh.

**Ejemplo** — máquina que acepta cadenas de dígitos, armada solo con la tabla:

| From | Read | Write | Move | To |
|---|---|---|---|---|
| q0 | `[\d]` | `~` | R | q0 |
| q0 | *(vacío)* | `~` | S | q1 |

En States: q0 = Initial, q1 = Final.

### 7. Guardado y deshacer

- Los **colores de nodos** y el **formato de las notas** se guardan en el `.jff` (como elementos XML adicionales) y se recuperan al abrir el archivo. Los archivos antiguos siguen abriéndose normalmente.
- **Deshacer** conserva colores y formato de las notas. Además se corrigió un fallo heredado: en máquinas de Turing, deshacer hacía desaparecer las notas.

---

## Atajos

| Atajo | Acción |
|---|---|
| Supr / Retroceso | Borrar selección (nodos y transiciones) |
| Ctrl + Z | Deshacer |
| Ctrl + Shift + Z / Ctrl + Y | Rehacer |
| Ctrl + 1 … 9 | Elegir la herramienta de la barra del editor (por posición) |
| Ctrl + Shift + D | Cambiar tema claro/oscuro |
| Ctrl + Shift + T | Abrir la tabla de reglas (máquinas de Turing) |

---

## Compilar desde las fuentes (Windows *OPCIONAL*)

1. Instala un **JDK 21+** (por ejemplo Temurin) y comprueba con `javac -version`.
2. Descomprime `fuentes_v6.zip` en una carpeta.
3. Copia tu JAR original a esa carpeta con el nombre **`JFLAP_UWU.jar`** (necesita la extensión `.jar`).
4. Ejecuta `build.bat`. Genera **`JFLAP_v6.jar`**.

El script compila solo las clases modificadas contra el JAR original y las inserta en una copia del mismo. El resto del programa queda intacto.


### Clases modificadas

| Archivo | Cambio |
|---|---|
| `plus/JFLAPPlus` | Atajo Supr / Retroceso |
| `plus/LabelMatcher` | Motor de clases y alfabetos |
| `plus/RuleTable` (nuevo) | Ventana de la tabla de reglas |
| `gui/editor/EditorPane` | Botón **Table** en la barra del editor |
| `gui/sim/ControlPanel`, `ConfigurationController` | Botón Auto (1 ms mínimo, varios pasos por tick), botón Tape y lógica de aceptar/rechazar |
| `plus/TapeViewer` (nuevo) | Visor de cinta completa |
| `automata/Note` | Notas legibles, menú de formato, tamaño de caja |
| `automata/State`, `gui/viewer/StateDrawer`, `gui/editor/ArrowTool` | Color de nodos; entrada **Transition table…** del menú del lienzo |
| `gui/editor/AutomatonSizeSlider` | El zoom respeta la fuente elegida en las notas |
| `automata/Automaton`, `automata/turing/TuringMachine` | Copiar color y formato al deshacer; conservar notas en Turing |
| `automata/turing/TMTransition`, `TMSimulator` | Clases de caracteres en el campo Read |
| `file/xml/AutomatonTransducer` | Guardar/leer color de nodos y formato de notas |

> Estas clases se obtuvieron decompilando el JAR (no había código fuente), y algunas se corrigieron a mano para que compilaran. Si notas un comportamiento raro al arrastrar nodos o abrir archivos antiguos, repórtalo.

---

## Limitaciones conocidas

- Los iconos de la barra de herramientas se ven oscuros sobre fondo oscuro en el tema oscuro.
- Aún no se puede cambiar la fuente global de iconos y textos.
- En máquinas de Turing, la negación `!a` no funcionó en las pruebas, igual que en el JAR original (comportamiento heredado).
- La tabla de reglas no edita las subrutinas (bloques) internas de un nodo: usa **Edit Block** y abre la tabla dentro de ese bloque. Las transiciones de bloque conservan su marca al editarse.
- **Edit Block** (menú del nodo) abre el editor de la subrutina del bloque, que está vacío si el bloque es nuevo; no es un editor de propiedades del nodo (para eso usa **Color…** y **Set Name**).

## Historial

| Versión | Cambios |
|---|---|
| v2 | Supr para borrar selección múltiple; botón Auto en el simulador |
| v3 | Notas legibles y con formato; color de nodos; guardado en `.jff`; deshacer conserva formato |
| v4 | Alfabetos `\d \D \w \W \s \S` en transiciones de Turing y etiquetas de autómatas finitos |
| v5 | Tabla de reglas para Máquinas de Turing (transiciones y estados) |
| v6 | Auto desde 1 ms y varios pasos por tick; visor de cinta completa (Tape) |
| v6_es | Una simple traducción al español de la ultima modificacion de JFLAP |

Cualquier distribución debe incluirla y ser gratuita.
