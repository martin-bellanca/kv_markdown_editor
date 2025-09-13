# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KV Markdown Editor is a Kivy-based desktop application for editing Markdown documents. It provides a dual-pane interface with a file tree/browser on the left and a markdown editor on the right, supporting project-based document management with filtering and search capabilities.

## Core Architecture

### Main Application Components

- **KVMarkdownEditorApp** (`kv_markdown_editor_main_rv.py`): The primary application class using RecycleView for better performance
- **Alternative Implementation** (`kv_markdown_editor_main.py`): Legacy version without RecycleView
- **Startup Script** (`kv_markdown_start.py`): Application entry point with logging configuration

### Key Dependencies

The application depends on custom widget libraries:
- `kivy_mpbe_widgets`: Custom Kivy widgets (file tree panels, markdown editors, buttons, etc.)  
- `helpers_mpbe`: Utility functions and helpers

These dependencies are expected to be in sibling directories relative to the project root.

### Document Model Architecture

- **MDDocument**: Core document model that manages markdown content as linked list of MDLine objects
- **MDDocumentEditor**: RecycleView-based editor that displays and edits markdown lines
- **MDLine**: Individual line representation with prev/next linking for navigation

### UI Layout Structure

```
BoxLayout (horizontal)
├── Splitter (left panel, 30% width)
│   ├── Project Bar (new project, open, help buttons)
│   ├── Search/Filter Bar (InputSearchOrFilter)
│   ├── File Tree Panel (FileTreePanel)
│   └── File List View (FileListView)
└── Document Editor (MDDocumentEditor, RecycleView)
```

### Session Management

- Configuration stored in `config.ini` using ConfigParser
- Window size/position, active project, and active file persistence
- Session data loaded on startup and saved on exit

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

## Key File Locations

- **Main application**: `kv_markdown_editor/kv_markdown_editor_main_rv.py` (current version)
- **Entry point**: `kv_markdown_editor/kv_markdown_start.py`
- **Configuration**: `config.ini` (generated at runtime in app directory)
- **Test markdown files**: `Doc_Markdown_Pruebas/` (sample documents for testing)
- **Experimental code**: `kv_markdown_editor/z_Pruebas/` (testing and prototyping)

## Architecture Notes

### Two-Stage Development

The project has two main implementations:
1. `kv_markdown_editor_main.py` - Original implementation
2. `kv_markdown_editor_main_rv.py` - Current RecycleView-based implementation (better performance)

### External Widget Dependencies

The application heavily relies on custom widget libraries that must be available in the Python path:
- File tree navigation widgets
- Markdown editing components with syntax highlighting
- Custom button and panel widgets
- Theming system

### Document Filtering System

The application supports real-time filtering of markdown content:
- Filter by text content in lines
- Option to include parent context (titles/headers) when filtering
- Filter state toggles between showing all content vs filtered content

### Session Persistence

User session data persists across application restarts:
- Window geometry (size, position)
- Last opened project directory
- Last opened file within project
- Theme and UI preferences