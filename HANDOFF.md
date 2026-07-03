# HANDOFF — KV Markdown Editor V2

**Última actualización:** 2026-07-02
**Propósito:** Documento de traspaso para continuar el desarrollo en una sesión nueva
(p. ej. con Fable). Resume qué es el proyecto, cómo está organizado, el estado
actual, las convenciones de trabajo y el plan de acción.

---

## 1. Qué es el proyecto

Editor de documentos **Markdown** hecho con **Kivy** (Python). El usuario navega
un árbol de carpetas, elige un archivo `.markdown/.md` y lo edita línea por línea
con render en vivo. Está en una **reescritura V2** del componente editor, porque
la V1 usaba un `RecycleView` genérico que no funcionaba bien para las necesidades
del proyecto y era muy complejo.

**Objetivo de la V2:** que el editor se comporte como un **editor de texto** real
(navegación con teclado, edición inline con render en vivo, selección, etc.),
sobre una arquitectura limpia con estado centralizado, y con un **sistema de
reciclado propio** (a futuro) adaptado al proyecto.

---

## 2. Estructura de repos y entorno

Son **tres** proyectos (carpetas hermanas), enlazados por symlinks:

| Repo (carpeta) | Rol | Rama actual |
|---|---|---|
| `kv_markdown_editor_prj_v2` | La **app** (este repo) | `feature/state-manager-integration` |
| `kivy_mpe_widgets_prj` | Librería de **widgets** (`kivy_mpbe_widgets`) | `uso_de_clases_en_data` |
| `helpers_mpbe_prj` | Helpers (`helpers_mpbe`, incluye `MDDocument`/`MDLine`) | — |

Dentro de la app hay **symlinks**: `kivy_mpbe_widgets -> kivy_mpe_widgets_prj/kivy_mpbe_widgets`
y `helpers_mpbe -> helpers_mpbe_prj/helpers_mpbe`.

> ⚠️ **La mayor parte del trabajo del editor V2 vive en el repo de widgets**, en
> el módulo `kivy_mpbe_widgets/wg_markdown2/`. La app sólo lo instancia.

**Entorno:** venv `.env314/` (Python 3.14, Kivy). Fuentes propias registradas en
`kivy_mpbe_widgets/rsrc_fonts` (incluye `RobotoMono` para el código inline).

**Cómo correr la app:** `kv_markdown_editor/kv_markdown_start_v2.py` con el venv y
`PYTHONPATH` en la raíz de la app. El usuario la ejecuta desde su IDE.

**⚠️ Verificación:** este entorno **no puede instanciar los widgets headless**
(Kivy necesita display; sin él el proceso termina al crear la ventana/GL). Por
eso **la verificación funcional la hace el usuario corriendo la GUI**. Sí se
puede verificar que los módulos **importan** sin errores (útil para atrapar
errores de sintaxis/imports):

```bash
APP=/mnt/Documentos/Documentos_mpbe/Programacion/Programacion_lin/Visual_Studio_Code/kv_markdown_editor_prj_v2
PYTHONPATH="$APP" KIVY_NO_ARGS=1 "$APP/.env314/bin/python" -c \
  "import os; os.environ['KIVY_NO_CONSOLELOG']='1'; \
   import kivy_mpbe_widgets.wg_markdown2.widgets.md_document_editor; print('OK')"
```

---

## 3. Arquitectura V2 (módulo `wg_markdown2`)

Patrón: **estado centralizado + widgets que observan su estado**.

| Componente | Archivo | Rol |
|---|---|---|
| `MDDocumentEditor` | `widgets/md_document_editor.py` | **Coordinador**. ScrollView + FocusBehavior. Carga el documento, crea una fila por línea, maneja teclado (a nivel Window), activación y edición. |
| `MDDocumentLine` | `widgets/md_document_line.py` | **Fila** por línea, atada a su `LineState`. Renderiza el label markdown; hover (líneas azules) y selección (verde) vía gráficos; en edición superpone/agrega un `MDLineTextInput`. |
| `DocumentStateManager` | `core/state_manager.py` | **Única fuente de verdad**. Crea un `LineState` por `MDLine`, tiene geometría (`y_position`, `total_height`, `get_visible_in_viewport`) y las operaciones (activate/deactivate/select/insert/remove/move/update_line_text). |
| `LineState` | `core/line_state.py` | Estado **mutable** de una línea (`EventDispatcher`): `active`, `editing`, `selected`, `hotlight`, `visible`, `md_line`, `widget_type`, etc. Dispara eventos al cambiar. |
| `MDLineTextInput` | `widgets/md_inputs.py` | `TextInput` con atajos (pares, listas de tareas). Se reusa en la edición. |
| Gráficos | `graphics/items_graphics.py` (`GHotlightItem`), `graphics/markdown_graphics.py` (`GSelectItem`) | Hover = 2 líneas verticales azules; selección = relleno verde con animación (fade en click, slide up/down con flechas). |
| Labels | `widgets/md_labels.py` | `BaseMDLabel` y subclases por tipo de línea (texto, título, tabla, separador…). |

**Modelo de datos** (en `helpers_mpbe`): `MDDocument` contiene `MDLine[]`. `LineState`
referencia su `MDLine` (compartido → editar persiste directo en el documento).

**Stack de edición viejo (referencia):** `widgets/md_line_editor.py`
(`MDDocumentLineEditor`) + `widgets/md_line_widgets.py` (`MDLineEditor` + sub-widgets
`MDDLDrag/NumberLine/Tree/InfoBar/Space`). No lo usa el coordinador V2, pero tiene
piezas reusables (ver `docs/ref_MDDocumentLineEditor.md`).

---

## 4. Estado actual

### Etapa I — COMPLETA
Render del documento + scroll (labels de solo lectura).

### Etapa II (edición) — EN PROGRESO
| Inc | Qué | Estado |
|---|---|---|
| 0 | Render de líneas *bound* a `LineState` (sin duplicar) | ✅ |
| 1 | Hover (líneas azules) + selección verde animada por click | ✅ |
| 2 | Edición: doble-click, `MDLineTextInput` overlay/below (config `editor_placement`), render en vivo, Enter/Escape | ✅ |
| **3a** | Teclado: **↑/↓, PageUp/Down, Ctrl+Home/End** (a nivel Window, con slide) | ✅ |
| 3b | F2/Enter→editar, ↑↓ en edición (mantener columna), ←→ entre líneas | ⬜ próximo |
| 3c | Enter parte la línea en el cursor, Backspace/Delete (unir/borrar), Alt+↑↓ (mover) | ⬜ |
| 3d | Navegación por títulos (Ctrl+↑↓, Ctrl+Shift+↑↓, Alt+Shift+↑↓) | ⬜ |
| 3e | Selección múltiple (Ctrl+A, Shift+↑↓, Shift/Ctrl+Click, Escape) | ⬜ |
| 4 | **Control del foco de la App** (coordinar foco entre árbol/archivos/editor) | ⬜ |
| 5 | **Sistema de reciclado propio** (solo realiza líneas visibles) | ⬜ |

> Detalle exhaustivo de teclas con estado en **`wg_markdown2/docs/tabla_eventos.md`**.

### Decisiones de diseño clave (ya tomadas)
- **Teclado a nivel `Window`** (`MDDocumentEditor._on_window_key_down`), gateado por
  `_kbd_active` (documento en uso) y `not _is_editing()`. Es robusto: la navegación
  **no depende del foco de Kivy**, así sobrevive a salir de edición con Escape/Enter.
  (Enfoque tomado del editor viejo tras fallar el approach de "devolver el foco".)
- **Edición**: `MDLineTextInput` translúcido **sobre** el label (`overlay`) o **debajo**
  (`below`, default) — configurable con `MDDocumentEditor.editor_placement`. El texto
  se persiste en `md_line.md_text` en cada tecla → render en vivo.
- **Animación de selección**: `markdown_graphics.GSelectItem` (fade en click, slide
  up/down con flechas). Se le agregó seguimiento del widget para acompañar el scroll.
- **Groundwork para el reciclado (Inc 5):** todo acceso a widgets de línea pasa por
  `MDDocumentEditor.get_line_widget(index)` (hoy lee del mapa `_line_widgets`; mañana
  hará scroll + realizará el widget). **Mantener esta convención** al codificar 3b-4.

---

## 5. Convenciones de trabajo (IMPORTANTES)

1. **Reescritura incremental**: agregar **un componente/acción por vez** y
   **verificar en la app** antes de seguir. No hacer features grandes de una.
2. **Explicar antes de editar**: describir bug/diagnóstico y solución propuesta y
   **esperar aprobación del usuario** antes de tocar código (aplica también a
   instrumentación/debug temporal). El usuario quiere entender cada cambio.
3. **Reusar el `wg_markdown` viejo con cuidado**: tiene mucho útil (sobre todo
   animaciones y mecánicas), pero tenía problemas (mayormente visuales) que la V2
   busca no arrastrar.
4. **Verificación**: la hace el usuario en la GUI (headless no sirve). Está OK
   dejar logs `SELDBG`-style temporales para diagnosticar y quitarlos después.
5. **Commits**: mensajes en español, descriptivos, con `Co-Authored-By`. Commitear
   sólo cuando el usuario lo pide; **no hacer push** salvo que lo pida.
6. **Diagramas**: documento vivo en **Mermaid** (`docs/arquitectura.md`), se
   actualiza en cada incremento.

---

## 6. Plan de acción — próximo: Inc 3b

**Objetivo Inc 3b** (todo cuando una línea está activa):
- **F2** y **Enter (en selección)** → entrar en modo edición de la línea activa.
- **↑ / ↓ en edición** → mover la edición a la línea de arriba/abajo manteniendo la
  **columna** del cursor.
- **← / →** en edición → si el cursor está al inicio/fin de la línea, pasar la
  edición a la línea anterior/siguiente (cursor al final/inicio respectivamente).

**Notas de implementación:**
- La navegación en edición requiere leer/fijar el cursor del `MDLineTextInput` y,
  al cambiar de línea, entrar en edición de la nueva con el cursor en la columna/pos
  correspondiente. Reusar `edit_line(index)` + posicionar cursor.
- Recordar el gate: el handler de teclado del documento (`_on_window_key_down`)
  hoy **no** actúa en edición (`_is_editing()` True). Las teclas de edición
  (↑↓←→ en edición) hay que manejarlas donde el `MDLineTextInput` tiene el foco
  (en `MDDocumentLine`, interceptando el teclado del input), no en el handler
  Window del documento. Definir bien esta división al planificar 3b.
- Enter tiene comportamiento definido para 3c: en edición **parte la línea en el
  cursor** (el texto posterior baja a una línea nueva; la actual conserva el
  anterior). En 3b, Enter en **selección** entra a editar.

**Después:** 3c (estructural: insertar/borrar/mover), 3d (títulos), 3e (selección
múltiple), 4 (foco de la app), 5 (reciclado propio).

---

## 7. Bugs resueltos y pendientes

**Resueltos (ver git log del repo de widgets):**
- Fuente `RobotoMono` no registrada → crash al renderizar código inline. (commit `243538e`)
- Animación de selección de archivo caía en la fila equivocada (app: `open_file`
  repoblaba el RecycleView en pleno click). (commit `b72d3a9`)
- Duplicación de líneas al scrollear en el editor V2. (Inc 0)
- ↑/↓ dejaban de andar tras salir de edición con Escape → se rediseñó el teclado a
  nivel Window. (commits `6e8384d`, `438a606`)

**Latentes / a tener en cuenta:**
- Sin reciclado: con documentos muy grandes, todas las líneas se realizan y cada
  fila liga `Window.mouse_pos` (hover) → puede pesar. Se resuelve en Inc 5.
- Foco entre paneles (árbol/archivos/editor) todavía no está coordinado → Inc 4.
- `_page_size()` estima con el alto de la línea activa; con alturas muy dispares
  puede no ser exacto (aceptable por ahora).

---

## 8. Documentación (en `kivy_mpbe_widgets/wg_markdown2/docs/`)

- **`arquitectura.md`** — documento **vivo** (Mermaid): clases, estados de línea,
  secuencia de edición, roadmap. Mantener al día en cada incremento.
- **`tabla_eventos.md`** — todas las combinaciones de teclado/mouse con sub-tarea y
  estado (la **spec** del comportamiento tipo editor de texto).
- **`ref_MDDocumentLineEditor.md`** — diagrama de clases del stack de edición viejo
  (referencia para reusar piezas).
- **`MDDocumentEditor_V2_Arquitectura.md`** — diseño original (parcialmente
  desactualizado; tiene banner con las diferencias).
- **`Eventos_Sistema.md`**, `Tablas de Eventos.ods`, `.uxf` (UMLet) — material de diseño.

**Para verlo:** VS Code con la extensión *Markdown Preview Mermaid Support* (o GitHub).
