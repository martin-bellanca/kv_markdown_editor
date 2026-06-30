# 📊 Diagrama de Clases - MDDocumentEditor V2

## Archivos Generados

✅ **md_document_editor_v2_class_diagram.puml** - Diagrama completo en formato PlantUML
✅ **md_document_editor_v2_class_diagram.md** - Documentación completa de la arquitectura
✅ **generate_diagram.sh** - Script de generación automática
✅ **plantuml.jar** - Herramienta PlantUML descargada

---

## 🎨 Cómo Generar la Imagen del Diagrama

### Método 1: Instalar Graphviz y Generar (RECOMENDADO)

PlantUML necesita Graphviz para generar diagramas de clases en PNG/SVG.

```bash
# Instalar Graphviz (Fedora/RHEL)
sudo dnf install graphviz

# Generar diagrama
./generate_diagram.sh
```

Esto generará:
- `md_document_editor_v2_class_diagram.png` - Imagen del diagrama

### Método 2: Usar VSCode con Extensión PlantUML

1. **Instalar la extensión PlantUML en VSCode:**
   - Buscar "PlantUML" en el marketplace
   - Instalar la extensión de jebbs

2. **Abrir el archivo .puml:**
   ```bash
   code md_document_editor_v2_class_diagram.puml
   ```

3. **Ver preview:**
   - Presionar `Alt + D` para ver el diagrama
   - O hacer click derecho → "Preview Current Diagram"

4. **Exportar:**
   - Click derecho → "Export Current Diagram"
   - Seleccionar formato (PNG, SVG, PDF)

### Método 3: Usar Herramientas Online

**PlantUML Online Server:**

1. Copiar el contenido del archivo `md_document_editor_v2_class_diagram.puml`
2. Ir a: https://www.plantuml.com/plantuml/uml/
3. Pegar el contenido en el editor
4. Ver el diagrama generado
5. Descargar como PNG/SVG

**Alternativa - PlantText:**

- URL: https://www.planttext.com/
- Proceso similar al servidor oficial

---

## 📖 Documentación Completa

El archivo **md_document_editor_v2_class_diagram.md** contiene:

- ✅ Descripción detallada de cada capa
- ✅ Todas las clases con sus métodos y atributos
- ✅ Relaciones entre componentes
- ✅ Flujos de datos típicos
- ✅ Ejemplos de código
- ✅ Guías de testing
- ✅ Comparación con versión anterior

```bash
# Leer la documentación
cat md_document_editor_v2_class_diagram.md
```

---

## 🏗️ Estructura del Diagrama

El diagrama muestra 5 capas principales:

### 1. Vista (UI Layer) 🟠
- MDDocumentEditor (widget principal)
- SelectableRecycleBoxLayout
- MDDocumentLineEditor

### 2. Gestión de Estado (State Layer) 🔵
- DocumentStateManager (Single Source of Truth)
- LineState (estado inmutable)
- StateChangeEvent

### 3. Servicios (Service Layer) 🟢
- LineService (operaciones de líneas)
- SelectionService (selección)
- NavigationService (navegación)
- FilterService (filtrado con filter_up)

### 4. Modelo de Documento (Model Layer) 🟡
- MDDocument (documento completo)
- MDLine (línea individual, linked list)
- MD_LINE_TYPE (enum de tipos)

### 5. Utilidades 🔴
- UndoManager
- TranslateMarkdownToKVMarkup

---

## 🔧 Solución de Problemas

### Error: "Cannot run program /opt/local/bin/dot"

**Problema:** Graphviz no está instalado.

**Solución:**
```bash
# Fedora/RHEL/CentOS
sudo dnf install graphviz

# Ubuntu/Debian
sudo apt install graphviz

# Verificar instalación
dot -V
```

Luego ejecutar de nuevo:
```bash
./generate_diagram.sh
```

### El diagrama no se ve bien

**Problema:** Diagrama muy grande o texto pequeño.

**Solución 1 - Ajustar escala en PlantUML:**
Editar `md_document_editor_v2_class_diagram.puml` y agregar al inicio:
```plantuml
scale 0.8
```

**Solución 2 - Generar en mayor resolución:**
```bash
java -jar plantuml.jar -tpng -Sdpi=300 md_document_editor_v2_class_diagram.puml
```

### No tengo Java

**Problema:** Java no está instalado.

**Solución:**
```bash
# Fedora/RHEL
sudo dnf install java-latest-openjdk

# Ubuntu/Debian
sudo apt install default-jre

# Verificar
java -version
```

---

## 📋 Resumen Rápido

### Para generar el diagrama ahora mismo:

```bash
# 1. Instalar dependencias
sudo dnf install graphviz

# 2. Generar diagrama
./generate_diagram.sh

# 3. Ver diagrama
xdg-open md_document_editor_v2_class_diagram.png
```

### Para ver la documentación:

```bash
# En terminal
cat md_document_editor_v2_class_diagram.md

# O con un editor markdown
code md_document_editor_v2_class_diagram.md
```

---

## 🎯 Características del Diagrama

✅ **Completo**: Todas las clases principales con métodos y atributos
✅ **Organizado**: Código por colores según capas
✅ **Detallado**: Relaciones, composición, agregación, dependencias
✅ **Documentado**: Notas explicativas en áreas clave
✅ **Actualizado**: Versión V2 con StateManager y Services
✅ **Profesional**: Formato UML estándar

---

## 📚 Referencias Adicionales

- **Archivo fuente**: `md_document_editor_v2.py`
- **StateManager**: `state_manager.py`
- **Servicios**: Directorio `services/`
- **Modelo**: `helpers_mpbe/markdown_document/md_document.py`
- **Tests**: Archivos `test_*.py`

---

## 🚀 Próximos Pasos

1. ✅ **Generar el diagrama** siguiendo las instrucciones arriba
2. ✅ **Revisar la documentación** en el archivo .md
3. ✅ **Entender la arquitectura** estudiando las capas
4. ✅ **Explorar el código** usando el diagrama como guía
5. ✅ **Hacer tests** basándose en los ejemplos de la documentación

---

**Versión**: alfa_0.0.1-2024-12-25
**Autor**: Martin Pablo Bellanca
**Licencia**: GPL3

Para más información, consultar `CLAUDE.md` en la raíz del proyecto.
