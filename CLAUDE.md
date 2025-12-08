# CLAUDE.md - KV Markdown Editor

## Project Overview

**KV Markdown Editor** is a desktop Markdown editor built with Python and Kivy framework. It provides a graphical interface for editing, browsing, and managing Markdown documents within a project directory structure.

- **Application Name**: KV Markdown Editor
- **Version**: alfa_0.0.1-2024-09-30
- **Author**: Martin Pablo Bellanca (mpbellanca@gmail.com)
- **License**: GNU General Public License v3 (GPL3)
- **Primary Language**: Python
- **GUI Framework**: Kivy 2.3.1
- **Minimum Kivy Version**: 2.1.0

### Purpose
This application serves as a Markdown document management and editing tool with features including:
- Tree-based file/folder navigation
- Live Markdown document editing with custom MDDocument model
- File filtering and search capabilities
- Session persistence (window size, position, active project/file)
- RecycleView-based document editor for performance

## Codebase Structure

```
kv_markdown_editor/
├── kv_markdown_editor/          # Main application package
│   ├── __init__.py              # Package initialization, constants, and paths
│   ├── kv_markdown_start.py     # Application entry point (current version)
│   ├── kv_markdown_editor_main.py         # Legacy main app (older version)
│   ├── kv_markdown_editor_main_rv.py      # Current main app (RecycleView version)
│   └── rsrc_images/             # Image resources
│       └── __init__.py
├── requirements.txt             # Python dependencies
├── LICENSE                      # GPL3 license text
├── README.md                    # Project readme (currently minimal)
├── .gitignore                   # Git ignore rules
├── task-txt-kv_start.sh        # Linux/Unix startup script
└── kv_markdown_editor.bat      # Windows startup script (empty)
```

### Important Files and Their Roles

#### `kv_markdown_editor/__init__.py` (Lines 1-107)
Defines project-wide constants and directory paths:
- `__app_name__`, `__version__`, `__author__`, `__license__`
- `DIR_APP`: Application directory
- `DIR_PRJ`: Project directory (parent of DIR_APP)
- `DIR_WKB`: Workbench directory (parent of DIR_PRJ)
- `DIR_HOME`: User home directory
- `DIR_IMAGES`: Image resources directory
- `DIR_KV_FILES`: Kivy files directory
- `paths_to_add`: External dependency paths (helpers_mpbe, kivy_mpbe_widgets)

#### `kv_markdown_editor/kv_markdown_start.py` (Lines 1-82)
Current application entry point:
- Configures Kivy logging system
- Sets log file naming and directory
- Logs application startup information
- Launches KVMarkdownEditorApp

#### `kv_markdown_editor/kv_markdown_editor_main_rv.py` (Lines 1-506)
Current production application class (RecycleView version):
- `KVMarkdownEditorApp`: Main Kivy application class
- Uses RecycleView for efficient document rendering
- Implements document filtering and search
- Session management (_load_sesion, _save_sesion)
- File operations (open_file, open_prj)
- Three debug test buttons (Print MDLine, Print MDLine P-N, Print Titles)

#### `kv_markdown_editor/kv_markdown_editor_main.py` (Lines 1-380)
Legacy application version (ListView-based):
- Similar structure to main_rv.py but uses older ListView approach
- Retained for reference or backward compatibility

## Architecture and Key Components

### Application Architecture

The application follows a hierarchical widget structure:

```
Window
└── BoxLayout (horizontal)
    ├── Splitter (left panel)
    │   └── BoxLayout (vertical, lateral bar)
    │       ├── Project Bar (buttons: New, Open, Help)
    │       ├── InputSearchOrFilter (search/filter bar)
    │       ├── FileTreePanel (folder tree navigation)
    │       ├── FileListView (file list in selected folder)
    │       └── Test Buttons (3 debug buttons)
    └── BoxLayout (right panel, vertical)
        └── MDDocumentEditor (RecycleView-based Markdown editor)
```

### Core Components

#### 1. MDDocument (External Dependency)
From `kivy_mpbe_widgets.wg_markdown.md_document`:
- Represents a Markdown document as a collection of `MDLine` objects
- Methods: `load_doc()`, `save_doc()`, `join_lines()`, `filter_lines()`
- Maintains document structure with line-by-line parsing
- Supports hierarchical title navigation (get_first_title, get_title_parent, etc.)

#### 2. MDDocumentEditor (External Dependency)
From `kivy_mpbe_widgets.wg_markdown.md_recycleview_editors`:
- RecycleView-based editor for efficient rendering of large documents
- Uses `MDDocumentLineEditor` as viewclass
- Method: `populate_from_md_lines()` to refresh UI from document model
- Emits events: `on_select_item`, `on_unselect_item`

#### 3. FileTreePanel (External Dependency)
From `kivy_mpbe_widgets.wg_tree_panels.tree_panels`:
- Tree-based folder navigation widget
- Events: `on_tree_node_selected`, `on_new_file`
- Property: `root_path` to change displayed directory

#### 4. FileListView (External Dependency)
From `kivy_mpbe_widgets.wg_recycle_list_view.recycle_list_view`:
- Lists files in current folder filtered by extensions
- Events: `on_select_item`, `on_unselect_item`, `on_save_file`
- Method: `populate()` to refresh with optional file selection

#### 5. Theme System (External Dependency)
From `kivy_mpbe_widgets.theming`:
- `Theme` class with name='flat_light', style='light'
- Provides: `theme.style['background_app']`, `theme.geometry['spacing']`, etc.

### External Dependencies

The application relies heavily on two external libraries (currently symbolic links, excluded in .gitignore):

1. **helpers_mpbe** - Utility helpers
   - Expected location: `DIR_WKB / 'helpers_mpbe_prj'`
   - Used for: `FolderWrapper` class

2. **kivy_mpbe_widgets** - Custom Kivy widgets library
   - Expected location: `DIR_WKB / 'kivy_mpe_widgets_prj'`
   - Provides all custom widgets (MDDocument, FileTreePanel, etc.)

### Session Management

Configuration is stored in `config.ini` in the application directory:

**Window Section:**
- width, height: Window dimensions
- left, top: Window position

**Project Section:**
- active_project: Last opened project path
- active_file: Last opened file name

Methods:
- `_load_sesion()`: Loads config on startup (kv_markdown_editor_main_rv.py:208-239)
- `_save_sesion()`: Saves config on exit (kv_markdown_editor_main_rv.py:241-268)

## Development Setup

### Prerequisites

- Python 3.x (tested with Python 3.8+)
- Virtual environment (recommended)
- External dependencies: helpers_mpbe, kivy_mpbe_widgets

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kv_markdown_editor
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up external dependencies**
   - Ensure `helpers_mpbe_prj` and `kivy_mpe_widgets_prj` are available in parent workbench directory
   - Or modify sys.path in `__init__.py` to point to correct locations

5. **Run the application**
   ```bash
   ./task-txt-kv_start.sh  # Linux/Mac
   # or
   cd kv_markdown_editor
   python kv_markdown_start.py
   ```

### Dependencies (requirements.txt)

- **certifi==2025.7.14**: SSL certificates
- **charset-normalizer==3.4.2**: Character encoding detection
- **docutils==0.22**: Documentation utilities
- **ffpyplayer==4.5.3**: Media player backend
- **filetype==1.2.0**: File type detection
- **idna==3.10**: Internationalized domain names
- **Kivy==2.3.1**: Main GUI framework
- **Kivy-Garden==0.1.5**: Kivy extension ecosystem
- **Markdown==3.8.2**: Markdown parsing library
- **numpy==2.3.2**: Numerical computing (Kivy dependency)
- **pillow==10.4.0**: Image processing
- **Pygments==2.19.2**: Syntax highlighting
- **requests==2.32.4**: HTTP library
- **setuptools==80.9.0**: Package management
- **urllib3==2.5.0**: HTTP client

## Code Conventions

### File Headers

All Python files include a standard GPL3 header:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  filename.py
#
#  Copyright 2012 Martin Pablo Bellanca <mbellanca@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License...
```

### Naming Conventions

- **Files**: snake_case (e.g., `kv_markdown_editor_main.py`)
- **Classes**: PascalCase (e.g., `KVMarkdownEditorApp`)
- **Methods/Functions**: snake_case with prefixes:
  - `_ui_*`: UI construction methods (e.g., `_ui_project_bar`)
  - `_on_*`: Event handlers (e.g., `_on_select_file`)
  - `_*`: Private/internal methods (e.g., `_load_sesion`, `_save_sesion`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DIR_APP`, `MD_LINE_TYPE`)

### Code Organization

**Import Order** (kv_markdown_editor_main_rv.py:29-71):
1. System imports (os, sys, codecs, json, etc.)
2. Kivy imports (kivy, kivy.app, kivy.uix.*, etc.)
3. Kivy_mpbe_widgets imports (custom widgets)
4. Application imports (__init__ as kv_md_editor)
5. External GUI libraries (tkinter for folder dialog)

**Class Structure**:
1. Class attributes (theme, title)
2. `__init__` method
3. Kivy lifecycle methods (build_config, build_settings, build)
4. Session functions (_load_sesion, _save_sesion)
5. UI functions (_ui_*)
6. Document functions (populate_doc_editor, open_file, open_prj)
7. Event functions (on_start, on_stop, _on_*)

### Language and Comments

- **Code comments**: Spanish (author's preference)
  - Example: `# Configuración de la aplicación`
  - Example: `# Variables internas`
- **Docstrings**: Spanish
- **Variable names**: English
- **Commit messages**: Spanish (based on git log)

### Testing and Debug Code

The application includes debug buttons for testing (kv_markdown_editor_main_rv.py:186-203):
- `btn_mdline1`: Print MDLine - prints each line type
- `btn_mdline`: Print MDLine P-N - prints with prev/next line context
- `btn_mdtitle`: Print Titles - tests title hierarchy navigation

These should be removed or made conditional in production builds.

## Git Workflow

### Branch Strategy

Based on the provided context, development happens on branches with this pattern:
- Feature branches: `claude/claude-md-{random-id}`
- Main branch: Default branch for pull requests
- Current branch: `claude/claude-md-mixt7oxnc3f3xp4e-013YEZMwccxL5mYB8sNEEt16`

### Commit Message Style

Recent commits show Spanish-language commit messages:
- "Actualizacion en Barra de Filtros"
- "Agregado de Barra de Filtro y Busqueda"
- "Agregado de archivos de inicio sh y bat"
- "Agregado de LICENSE y README.md"

Style: Short imperative statements in Spanish, focusing on what was added/updated.

### Git Operations Rules

1. **Always** develop on the designated feature branch
2. **Never** push to main/master without explicit permission
3. **Use** descriptive commit messages following project convention (Spanish)
4. **Branch names** must start with 'claude/' and match session ID for successful push
5. **Push with** `-u origin <branch-name>` flag
6. **Retry** network failures up to 4 times with exponential backoff (2s, 4s, 8s, 16s)

## AI Assistant Guidelines

### Critical Rules

1. **NEVER modify external dependencies**: The `kivy_mpbe_widgets` and `helpers_mpbe` packages are external. Do not attempt to modify them.

2. **Read before modifying**: Always read existing files before suggesting changes. The application structure is complex with many interdependencies.

3. **Respect the version**: The current active version is `kv_markdown_editor_main_rv.py`. The `kv_markdown_editor_main.py` file is legacy. Changes should go to the `_rv.py` version unless explicitly requested otherwise.

4. **Session persistence**: When adding features, consider impact on session management. New state may need to be saved/loaded via `_load_sesion`/`_save_sesion`.

5. **External widget events**: Many widgets emit custom events (on_select_item, on_tree_node_selected, etc.). Check widget documentation before binding.

6. **Language consistency**: Keep code comments in Spanish to match existing style, but use English for variable/method names.

7. **Test buttons**: The three test buttons at the bottom of the sidebar are for debugging. Don't remove them without explicit request as they're used for development testing.

### Common Pitfall Areas

1. **Directory paths**: The app uses `Path` objects from pathlib. Be careful with path joining:
   - Correct: `DIR_APP / 'subdir'`
   - Incorrect: `DIR_APP + '/subdir'`

2. **MDDocument lifecycle**: The MDDocument is recreated when changing folders (line 392). Ensure any references are updated accordingly.

3. **Config loading**: The Kivy Config object and ConfigParser are different. Session loading uses Kivy's Config (read-only), session saving uses ConfigParser.

4. **File extensions**: Markdown extensions are stored as comma-separated string, not a list:
   ```python
   self.md_extensions = 'md, markdown, mdown, mkdn, mkd, mdtxt, mdtext'
   ```

5. **Focus management**: Several widgets have `is_focusable` property set to False. This is intentional for keyboard navigation.

### Adding New Features Checklist

- [ ] Read all relevant existing code first
- [ ] Check if external dependencies need updates (usually NO)
- [ ] Consider session persistence needs
- [ ] Add Spanish comments for complex logic
- [ ] Test with actual Markdown files
- [ ] Verify event binding/unbinding doesn't cause memory leaks
- [ ] Check if FileListView needs refresh after changes
- [ ] Ensure theme consistency (use theme.style and theme.geometry)
- [ ] Update this CLAUDE.md if architecture changes significantly

### Key File References

When working on specific features, reference these key locations:

- **App initialization**: kv_markdown_start.py:62-81, kv_markdown_editor_main_rv.py:78-92
- **UI layout**: kv_markdown_editor_main_rv.py:130-205
- **File operations**: kv_markdown_editor_main_rv.py:321-332 (open_file)
- **Session management**: kv_markdown_editor_main_rv.py:208-268
- **Event handlers**: kv_markdown_editor_main_rv.py:384-452
- **Folder selection**: kv_markdown_editor_main_rv.py:390-394 (tree), 400-403 (file)
- **Document filtering**: kv_markdown_editor_main_rv.py:442-452
- **Project constants**: kv_markdown_editor/__init__.py:75-102

### Current State Notes

- **Latest feature**: Search/Filter bar with toggle for including parent items (lines 154-159, 437-452)
- **Active development**: RecycleView implementation is current; ListView version is legacy
- **Missing functionality**: Help button is present but not implemented
- **Known TODOs in code**:
  - Line 406: "Verificar si el archivo se modifico y guardar" (Check if file modified before saving)
  - Line 423: "Verificar si el archivo es el activo blanquear la interfaz" (Clear interface if active file deleted)

### Testing Approach

The application includes inline test buttons. When testing:
1. Use the three test buttons to verify MDDocument structure
2. Check title hierarchy with "Print Titles" button
3. Verify line navigation with "Print MDLine P-N" button
4. Test with various Markdown files in Doc_Markdown_Pruebas folder (if available)

---

**Document Version**: 1.0
**Last Updated**: 2025-12-08
**For**: AI Assistants working on KV Markdown Editor
