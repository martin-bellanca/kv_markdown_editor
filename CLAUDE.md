# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**KV Markdown Editor** is a Kivy-based desktop application for editing Markdown documents. It provides a dual-pane interface with a file tree/browser on the left and a markdown editor on the right, supporting project-based document management with filtering and search capabilities.

**Project Information:**
- **Name:** KV Markdown Editor
- **Version:** alfa_0.0.1-2024-09-30
- **License:** GPL3 (Free Software)
- **Author:** Martin Pablo Bellanca
- **Current Branch:** `filtros_y_busqueda` (filter and search features)

## Core Architecture

### Main Application Components

- **KVMarkdownEditorApp** ([kv_markdown_editor_main_rv.py](kv_markdown_editor/kv_markdown_editor_main_rv.py)): The primary application class using RecycleView for better performance (506 lines)
- **Alternative Implementation** ([kv_markdown_editor_main.py](kv_markdown_editor/kv_markdown_editor_main.py)): Legacy version without RecycleView
- **Startup Script** ([kv_markdown_start.py](kv_markdown_editor/kv_markdown_start.py)): Application entry point with logging configuration (82 lines)

### Key Dependencies

The application depends on custom widget libraries located in sibling directories:

#### `helpers_mpbe` Library
Located at: `/home/mpbe/Documentos/.../helpers_mpbe_prj/`

Key modules:
- **markdown_document/md_document.py** (843 lines): MDDocument and MDLine classes
- **markdown_document/md_translate.py**: Markdown to Kivy Markup translator
- **markdown_document/md_labels.py**: Markdown visualization widgets
- **markdown_document/__init__.py**: MD_LINE_TYPE enum and TYPE_PATTERNS
- **python.py**: Python utilities (compose, check_list)
- **geometry.py**: Design constants
- **estructura.py**: Data structures

#### `kivy_mpbe_widgets` Library
Located at: `/home/mpbe/Documentos/.../kivy_mpe_widgets_prj/`

Key widgets used:
- **wg_markdown/md_recycleview_document_editor.py**: MDDocumentEditor (main editor)
- **wg_markdown/md_recycleview_line_editors.py**: MDDocumentLineEditor (individual line editor)
- **wg_recycle_list_view/recycle_list_view.py**: FileListView (file list component)
- **wg_tree_panels/tree_panels.py**: FileTreePanel (folder tree navigator)
- **wg_inputs/inputs.py**: InputSearchOrFilter (search/filter bar)
- **wg_buttons/click_buttons.py**: ClickButton, ClickButtonLabel
- **wg_labels/font_icon_labels.py**: FontIconLabel, FontIconWText
- **wg_panels/panels.py**: BoxPanel
- **wg_undo/undo_manager.py**: UndoManager
- **theming.py**: Theme system (flat_light theme)

### Document Model Architecture

#### MDLine Class
Represents a single line in the markdown document using a linked list structure.

**Properties:**
- `type: MD_LINE_TYPE` - Line type (TITLE, LIST, CODE, etc.)
- `md_text: str` - Markdown text of the line
- `num_line: int` - Line number
- `prev_line: MDLine` - Reference to previous line (linked list)
- `next_line: MDLine` - Reference to next line (linked list)

**Key Methods:**
- Navigation: `get_title_parent()`, `get_title_Childs()`, `get_title_next()`, `get_title_prev()`
- List navigation: `get_list_parent()`, `get_list_Childs()`, `get_list_next()`, `get_list_prev()`
- Processing: `get_markup_text()`, `update_type()`, `get_title_level()`, `get_tab_level()`

#### MDDocument Class
Manages the complete markdown document as a collection of MDLine objects.

**Properties:**
- `document: str` - Complete content in markdown format
- `path_doc: str` - Directory path where document is saved
- `doc_name: str` - File name with extension
- `md_lines: list[MDLine]` - List of lines (read-only)
- `can_lines: int` - Number of lines

**Key Methods:**
- `load_doc(path, doc_name)` - Load document from file
- `save_doc()` - Save current document to file
- `separate_lines()` - Split document into MDLine list
- `join_lines()` - Combine MDLine list into document text
- `append_line(md_text)` - Append new line at end
- `insert_line(id, md_text)` - Insert line at specific position
- `remove_line(md_line)` - Remove a line
- `move_line_up(md_line)` / `move_line_down(md_line)` - Move line up/down
- `update_type_line(md_line)` - Detect and update line type

#### Supported Markdown Line Types

The `MD_LINE_TYPE` enumeration defines 14 different types:

```python
class MD_LINE_TYPE(Enum):
    TEXT = 0              # Normal text
    TITLE = 1             # Title with # (# Title)
    HEAD_TITLE = 2        # Underlined title (Title\n===)
    UNDERLINE_TITLE = 3   # Underline line
    SEPARATOR = 4         # Separator line (---)
    LIST = 5              # Unordered list (- Item)
    ORDER_LIST = 6        # Ordered list (1. Item)
    TASK = 7              # Task list (- [ ] Task)
    TODO = 8              # TODO type (- [x] Done)
    TABLE = 9             # Markdown table (| col |)
    BLOCKQUOTE = 10       # Quote (> Text)
    IMAGEN = 11           # Image (![alt](url))
    CODE = 12             # Code block
    START_CODE = 13       # Code start (```)
    END_CODE = 14         # Code end (```)
```

**Detection via Regular Expressions (TYPE_PATTERNS):**
- `title`: `r'^#{1,6}\s+.*$'`
- `list`: `r'^\s*- [^\[].*'`
- `task`: `r'^\s*-\s\[[x\s]\].*'`
- `todo`: `r'^\s*-\[[xo>\-\s].*'`
- `table`: `r'^\|.*\|$'`
- `separator`: `r'^---[-\s]*$'`
- `image`: `r'^!\[.*?\]\(.*?\)$'`

### UI Layout Structure

```
BoxLayout (horizontal)
├── Splitter (left panel, 30% width)
│   ├── Project Bar (new project, open, help buttons)
│   │   ├── ClickButton: New Project
│   │   ├── ClickButton: Open Project
│   │   └── ClickButton: Help
│   ├── Search/Filter Bar (InputSearchOrFilter)
│   │   ├── Text search input
│   │   ├── Filter toggle button
│   │   └── Include parents toggle button
│   ├── File Tree Panel (FileTreePanel)
│   │   └── TreeView for folder navigation
│   └── File List View (FileListView - RecycleView)
│       └── List of markdown files in selected directory
└── Document Editor (70% width)
    └── MDDocumentEditor (RecycleView)
        └── Editable markdown lines (MDDocumentLineEditor)
```

### Session Management

- Configuration stored in [config.ini](kv_markdown_editor/config.ini) using ConfigParser
- Window size/position, active project, and active file persistence
- Session data loaded on startup and saved on exit

**Configuration Format:**
```ini
[Window]
width = 1452
height = 896
left = 0
top = 0

[Project]
active_project = /path/to/project
active_file = filename.markdown
```

**Methods:**
- `_load_sesion()`: Loads previous session on app start
- `_save_sesion()`: Saves current session on app exit

## Common Development Commands

### Running the Application

```bash
# Linux/macOS
./task-txt-kv_start.sh

# Or directly with Python
cd kv_markdown_editor
python kv_markdown_start.py
```

```cmd
# Windows
kv_markdown_editor.bat
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- Kivy 2.3.1 - GUI framework
- Markdown 3.8.2 - Markdown processing
- Pillow 10.4.0 - Image processing
- Pygments 2.19.2 - Syntax highlighting
- numpy 2.3.2 - Numerical operations

## Key File Locations

- **Main application**: [kv_markdown_editor/kv_markdown_editor_main_rv.py](kv_markdown_editor/kv_markdown_editor_main_rv.py) (current version - 506 lines)
- **Entry point**: [kv_markdown_editor/kv_markdown_start.py](kv_markdown_editor/kv_markdown_start.py) (82 lines)
- **Configuration**: [config.ini](kv_markdown_editor/config.ini) (generated at runtime in app directory)
- **Test markdown files**: [Doc_Markdown_Pruebas/](Doc_Markdown_Pruebas/) (sample documents for testing)
- **Experimental code**: [kv_markdown_editor/z_Pruebas/](kv_markdown_editor/z_Pruebas/) (testing and prototyping)
- **Kivy files**: [kv_markdown_editor/kv_files/](kv_markdown_editor/kv_files/) (Kivy configuration files)
- **Resources**: [kv_markdown_editor/rsrc_images/](kv_markdown_editor/rsrc_images/) (image resources)
- **Logs**: [kv_markdown_editor/kivy_logs/](kv_markdown_editor/kivy_logs/) (application logs)

## Main Application Class

### KVMarkdownEditorApp Attributes

```python
class KVMarkdownEditorApp(App):
    # Theme configuration
    theme = ObjectProperty(Theme(name='flat_light', style='light'))

    # Undo/Redo management
    _undo_manager = ObjectProperty(UndoManager())

    # Document model
    md_document = ObjectProperty(MDDocument())

    # Project configuration
    active_project = StringProperty('')
    md_extensions = StringProperty('md,markdown,mdown,mkdn,mkd,mdwn')

    # UI References (set in build())
    left_panel = ObjectProperty(None)
    right_panel = ObjectProperty(None)
    file_tree_panel = ObjectProperty(None)
    file_list_view = ObjectProperty(None)
    input_search_or_filter = ObjectProperty(None)
    doc_editor = ObjectProperty(None)
```

### Key Methods

**Project Management:**
- `open_prj(folder: str)` - Open project folder
- `_open_folderchooser(initial_directory)` - Open native folder chooser dialog
- `_on_select_folder(tree, folder, touch)` - Handle folder selection in tree

**File Management:**
- `open_file(file_path: str, file_name: str)` - Open markdown file
- `_on_select_file(instance, file_name)` - Handle file selection from list
- `_on_save_file(instance, file_name)` - Save current file
- `_on_new_file(instance, parent_folder)` - Create new file

**Document Editing:**
- `populate_from_md_lines(md_lines: list)` - Populate editor from MDLine list
- `populate_doc_editor()` - Populate editor from current document

**Filter and Search:**
- `_on_filter_state_change(instance, value)` - Handle filter state changes
- Note: `filter_lines()` method is called but not yet implemented in MDDocument

**Session Management:**
- `_load_sesion()` - Load previous session configuration
- `_save_sesion()` - Save current session configuration

## Architecture Notes

### Two-Stage Development

The project has two main implementations:
1. [kv_markdown_editor_main.py](kv_markdown_editor/kv_markdown_editor_main.py) - Original implementation without RecycleView
2. [kv_markdown_editor_main_rv.py](kv_markdown_editor/kv_markdown_editor_main_rv.py) - Current RecycleView-based implementation (better performance with large documents)

**Advantages of RecycleView version:**
- Efficient rendering of large documents (hundreds/thousands of lines)
- Widget recycling reduces memory footprint
- Smoother scrolling performance
- Better scalability

### External Widget Dependencies

The application heavily relies on custom widget libraries that must be available in the Python path:
- File tree navigation widgets (FileTreePanel with TreeView)
- Markdown editing components with syntax highlighting (MDDocumentEditor, MDDocumentLineEditor)
- Custom button and panel widgets (ClickButton, BoxPanel)
- Search and filter inputs (InputSearchOrFilter)
- Theming system (flat_light theme with light style)

### Document Filtering System

The application supports real-time filtering of markdown content (currently in development):
- Filter by text content in lines
- Option to include parent context (titles/headers) when filtering
- Filter state toggles between showing all content vs filtered content
- UI component complete, backend logic pending implementation

**Status:** The `InputSearchOrFilter` widget is fully integrated, but the `filter_lines()` method in MDDocument is not yet implemented.

### Session Persistence

User session data persists across application restarts:
- Window geometry (size, position)
- Last opened project directory
- Last opened file within project
- Theme and UI preferences

### Linked List Architecture

MDLine objects use a doubly-linked list structure:
- Each line has `prev_line` and `next_line` references
- Enables efficient bidirectional navigation without array indexing
- Supports hierarchical navigation (parent/child titles and lists)
- Optimized for document structure traversal

## Typical Application Flow

```
1. START
   └─ kv_markdown_start.py
      └─ Configure logging
         └─ KVMarkdownEditorApp().run()

2. BUILD UI (build())
   ├─ Create horizontal layout with Splitter
   ├─ Left panel (30%):
   │  ├─ Project bar (buttons)
   │  ├─ Filter/search bar
   │  ├─ Folder tree
   │  └─ File list
   └─ Right panel (70%):
      └─ Document editor

3. LOAD SESSION (on_start())
   └─ _load_sesion()
      ├─ Read config.ini
      ├─ Restore window size
      ├─ Open previous project
      └─ Open last file

4. SELECT FOLDER
   └─ _on_select_folder()
      ├─ Reset document
      └─ Load file list

5. SELECT FILE
   └─ _on_select_file()
      └─ open_file()
         ├─ Load file
         ├─ separate_lines() (split into MDLine)
         ├─ populate_doc_editor() (display in editor)
         └─ Update file list

6. EDIT CONTENT
   └─ User edits lines in MDDocumentEditor
      ├─ MDLine objects updated
      └─ Types auto-detected

7. FILTER CONTENT
   └─ _on_filter_state_change()
      ├─ If ON: filter_lines() (not implemented yet)
      └─ If OFF: populate_from_md_lines(md_lines)

8. SAVE
   └─ _on_save_file()
      ├─ join_lines() (combine MDLine into document)
      └─ save_doc() (save file)

9. EXIT
   └─ on_stop()
      └─ _save_sesion()
         └─ Save state to config.ini
```

## Features In Development

Based on current branch `filtros_y_busqueda`:

### Filter and Search System
- ✅ UI created (InputSearchOrFilter widget)
- ✅ Event handlers connected
- ✅ Toggle buttons functional
- ❌ Backend `filter_lines()` method not implemented in MDDocument
- ❌ Parent title inclusion logic not completed

### RecycleView Restructuring
- ✅ Migration to RecycleView completed
- ✅ Better performance with large documents
- ✅ Widget recycling working
- ❌ Some synchronization events pending

## Recent Commit History

```
ae3ce89 Re-estructuracion de RecycleView para usar filtros
c64d17a update 25-09-16
46495ac Actualizacion al uso de index para ubicar data
c7326c5 Actualizacion en Barra de Filtros
377f3cd Agregado de Barra de Filtro y Busqueda
dd45282 Agregado de archivos de inicio sh y bat
fc2e946 Agregado de LICENSE y README.md
33f0633 Agregado del archivo requirements.txt
dab85ca Commit Inicial
```

## Design Principles

1. **Separation of Concerns:**
   - Document logic in `helpers_mpbe`
   - UI widgets in `kivy_mpbe_widgets`
   - Application logic in `kv_markdown_editor`

2. **Performance Optimization:**
   - RecycleView for efficient large document handling
   - Widget recycling reduces memory usage
   - Linked list structure for fast navigation

3. **User Experience:**
   - Automatic session persistence
   - Dual-pane interface for browsing and editing
   - Real-time markdown type detection
   - Theme support for customization

4. **Code Organization:**
   - Modular widget architecture
   - Reusable components across projects
   - Clear separation between model and view

## Known Limitations

1. **Filter System:** Backend implementation incomplete (UI ready)
2. **Undo/Redo:** UndoManager integrated but functionality may be limited
3. **Help System:** Help button present but help content not defined
4. **Testing:** Limited test coverage in `z_Pruebas/` directory

## Development Notes

- Always check that helper libraries are accessible in Python path
- Use RecycleView version (`kv_markdown_editor_main_rv.py`) for new features
- Legacy version (`kv_markdown_editor_main.py`) maintained for reference
- Logs stored in `kivy_logs/` with timestamp format: `kv_md_editor_YYYY-MM-DD_HH-MM-SS.log`
- Theme system uses `flat_light` theme with `light` style
- Markdown extensions: `.md`, `.markdown`, `.mdown`, `.mkdn`, `.mkd`, `.mdwn`

## Testing

Test documents available in [Doc_Markdown_Pruebas/](Doc_Markdown_Pruebas/) directory for:
- Various markdown syntax elements
- Large documents for performance testing
- Edge cases in markdown formatting

## Contributing Guidelines

When working on this project:
1. Use the RecycleView version as the main codebase
2. Maintain compatibility with external widget libraries
3. Update CLAUDE.md when adding significant features
4. Test with sample documents in `Doc_Markdown_Pruebas/`
5. Follow existing code style and patterns
6. Ensure session persistence works correctly
7. Verify theme system integration
