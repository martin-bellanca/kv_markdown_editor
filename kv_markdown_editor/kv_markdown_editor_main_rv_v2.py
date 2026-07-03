#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kv_markdown_editor_main_rv_v2.py
#
#  Copyright 2012 Martin Pablo Bellanca <mbellanca@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

"""
Aplicación principal de KV Markdown Editor V2.

Editor de documentos markdown con interfaz Kivy, basado en RecycleView
para mejor rendimiento con documentos grandes.

VERSIÓN 2.0 - Refactorizada con:
- MDDocumentEditorV2 (StateManager + Services)
- FilterService integrado
- -73% código vs versión legacy
- 98% cobertura de tests

@author: mpbe
@created: 30/09/2024
@refactored: 25/12/2024 (V2 con StateManager + Services)
"""

# System imports
import os
from pathlib import Path
import traceback

# Kivy imports
import kivy
kivy.require('2.1.0')
from kivy.logger import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

# Application imports
import __init__ as kv_md_editor
from kv_markdown_editor.session_manager import SessionManager
from kv_markdown_editor.project_manager import ProjectManager
from kv_markdown_editor.ui_builder_v2 import UIBuilder

# Kivy widgets imports
from kivy_mpbe_widgets.theming import Theme
from kivy_mpbe_widgets.wg_undo.undo_manager import UndoManager
from helpers_mpbe.markdown_document.md_document import MDDocument


class KVMarkdownEditorApp(App):
    """
    Aplicación principal de KV Markdown Editor V2.

    Editor de documentos markdown con interfaz de doble panel:
    - Panel izquierdo: navegación de proyectos y archivos
    - Panel derecho: editor de markdown con MDDocumentEditorV2

    VERSIÓN 2.0 con arquitectura refactorizada:
    - StateManager: Estado centralizado e inmutable
    - Services: LineService, SelectionService, NavigationService, FilterService
    - FilterService: Filtrado funcional con inclusión de títulos padre
    - 98% cobertura de tests

    Attributes:
        theme: Tema visual de la aplicación
        title: Título de la ventana
        session_manager: Gestor de persistencia de sesión
        project_manager: Gestor de proyectos y archivos
        ui_builder: Constructor de interfaz de usuario
        _undo_manager: Gestor de deshacer/rehacer (futuro)
    """

    def __init__(self, **kwargs):
        """Inicializa la aplicación V2 y sus componentes."""
        super(KVMarkdownEditorApp, self).__init__(**kwargs)

        Logger.info("KVMarkdownEditorApp V2: Inicializando aplicación")

        # Configuración de tema
        self.theme = Theme(name='flat_light', style='light')

        # Título de la aplicación
        version_str = f"{kv_md_editor.__version__} - V2 (StateManager + Services)"
        self._title = f"KV Markdown Editor ({version_str})"
        self.title = self._title

        # Managers
        self.session_manager = SessionManager(config_file='config.ini')
        self.project_manager = ProjectManager(md_document=MDDocument())
        self.ui_builder = UIBuilder(theme=self.theme)
        self._undo_manager = UndoManager()

        # Referencias a widgets UI (se inicializan en build())
        self.widgets = {}


        Logger.info("KVMarkdownEditorApp V2: Inicialización completada con arquitectura refactorizada")

    def build_settings(self, settings):
        """
        Panel de configuración de la aplicación (se llama con F1).

        Args:
            settings: Panel de configuración de Kivy

        Returns:
            Panel de configuración configurado
        """
        settings.add_json_panel(
            'KV Markdown Editor',
            self.config,
            data='''
                [
                    {
                        "type": "title",
                        "title": "KV Markdown Editor",
                        "collapsable": false,
                        "open": false
                    }
                ]'''
        )
        return super().build_settings(settings)

    def build(self):
        """
        Construye la interfaz de usuario de la aplicación V2.

        Returns:
            Widget: Layout raíz de la aplicación
        """
        Logger.info("KVMarkdownEditorApp V2: Construyendo interfaz de usuario")

        # Configurar color de fondo de ventana
        Window.clearcolor = self.theme.style['background_app']

        # Construir UI completa con MDDocumentEditorV2

        print("-"*120)
        print("Project Manager active project: ", self.project_manager.active_project)


        self.widgets = self.ui_builder.build_complete_ui(
            active_project=self.project_manager.active_project,
            md_extensions=self.project_manager.get_extensions_string(),
            include_debug_buttons=True  # Cambiar a False en producción
        )

        # Conectar eventos
        self._connect_events()

        Logger.info("KVMarkdownEditorApp V2: Interfaz de usuario construida con MDDocumentEditorV2")

        return self.widgets['root_layout']

    def _connect_events(self):
        """
        Conecta todos los eventos de la interfaz de usuario.

        Side Effects:
            Vincula callbacks a eventos de widgets
        """
        # Eventos del editor de documento
        self.widgets['doc_editor'].bind(
            on_select_item=self._on_select_line,
            on_unselect_item=self._on_unselect_line
        )

        # Eventos de la barra de proyecto
        self.widgets['btn_new_prj'].bind(size=self._on_size_prj_btns)
        self.widgets['btn_open_prj'].bind(
            size=self._on_size_prj_btns,
            on_click=self._on_open_prj
        )
        self.widgets['btn_help'].bind(size=self._on_size_prj_btns)

        # Eventos de búsqueda/filtro
        self.widgets['search_filter_bar'].bind(
            on_search=self._on_search_event,
            filter_state=self._on_filter_state_change
        )

        # Eventos del árbol de archivos
        self.widgets['tree_panel'].tree_view.bind(
            on_tree_node_selected=self._on_select_folder,
            on_new_file=self._on_new_file
        )

        # Eventos de la vista de archivos
        self.widgets['file_list_view'].bind(
            on_select_item=self._on_select_file,
            on_unselect_item=self._on_unselect_file,
            on_save_file=self._on_save_file
        )

        # Eventos de botones de debug
        if 'btn_mdline1' in self.widgets:
            self.widgets['btn_mdline1'].bind(on_click=self._on_btn_mdline1_test)
            self.widgets['btn_mdline'].bind(on_click=self._on_btn_mdline_test)
            self.widgets['btn_mdtitle'].bind(on_click=self._on_btn_mdtitle_test)

    # Session Management Methods

    def _load_session(self):
        """
        Carga la configuración de la sesión anterior.

        Side Effects:
            - Restaura tamaño y posición de ventana
            - Abre proyecto anterior
            - Abre último archivo activo

        Raises:
            FileNotFoundError: Si no existe archivo de configuración
            PermissionError: Si no hay permisos de lectura
            ValueError: Si el archivo está corrupto
        """
        Logger.info("KVMarkdownEditorApp: Cargando sesión")

        try:
            session_data = self.session_manager.load_session(kv_md_editor.DIR_APP)

            # Restaurar configuración de ventana
            window_cfg = session_data['window']
            Window.size = (window_cfg['width'], window_cfg['height'])
            Window.left = window_cfg['left']
            Window.top = window_cfg['top']

            # Restaurar proyecto activo
            project_cfg = session_data['project']
            if project_cfg['active_project']:
                try:
                    self.open_project(project_cfg['active_project'])

                    # Abrir último archivo activo
                    if project_cfg['active_file']:
                        self.open_file(
                            project_cfg['active_project'],
                            project_cfg['active_file']
                        )

                except Exception as e:
                    tb = traceback.extract_tb(e.__traceback__)[-1]
                    Logger.warning(
                        f"KVMarkdownEditorApp: No se pudo restaurar proyecto/archivo: {e}\n"
                        f"              Modulo: [{tb.filename}:{tb.lineno}]"
                    )
                    return

            Logger.info("KVMarkdownEditorApp: Sesión cargada exitosamente")

        except FileNotFoundError:
            tb = traceback.extract_tb(e.__traceback__)[-1]
            Logger.info(
                "KVMarkdownEditorApp: No existe archivo de configuración, "
                "usando valores por defecto/n"
                f"              Modulo: [{tb.filename}:{tb.lineno}]"
            )
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)[-1]
            Logger.error(f"KVMarkdownEditorApp: Error al cargar sesión: {e}\n"
                         f"                 Modulo: [{tb.filename}:{tb.lineno}]")
            raise

    def _save_session(self):
        """
        Guarda la configuración actual de sesión.

        Side Effects:
            Guarda estado actual en config.ini

        Raises:
            PermissionError: Si no hay permisos de escritura
            OSError: Si hay error al escribir archivo
        """
        Logger.info("KVMarkdownEditorApp: Guardando sesión")

        try:
            window_config = {
                'width': int(Window.width),
                'height': int(Window.height),
                'left': int(Window.left),
                'top': int(Window.top)
            }

            project_config = {
                'active_project': self.project_manager.active_project,
                'active_file': self.project_manager.md_document.doc_name or ''
            }

            self.session_manager.save_session(
                kv_md_editor.DIR_APP,
                window_config,
                project_config
            )

            Logger.info("KVMarkdownEditorApp: Sesión guardada exitosamente")

        except Exception as e:
            Logger.error(f"KVMarkdownEditorApp: Error al guardar sesión: {e}")
            raise

    # Project and File Management Methods

    def open_project(self, folder: str) -> bool:
        """
        Abre un proyecto markdown.

        Args:
            folder: Ruta del directorio del proyecto

        Returns:
            bool: True si el proyecto se abrió exitosamente

        Raises:
            ValueError: Si la carpeta es inválida
            FileNotFoundError: Si la carpeta no existe
            PermissionError: Si no hay permisos
        """
        if not folder:
            return False

        try:
            # Abrir proyecto usando ProjectManager
            self.project_manager.open_project(folder)

            # Actualizar UI
            self.widgets['tree_panel'].tree_view.root_path = folder
            self.widgets['file_list_view'].folder = folder

            Logger.info(f"KVMarkdownEditorApp: Proyecto abierto: {folder}")
            return True

        except Exception as e:
            Logger.error(f"KVMarkdownEditorApp: Error al abrir proyecto: {e}")
            raise

    def open_file(self, file_path: str, file_name: str, refresh_list: bool = True) -> bool:
        """
        Abre un archivo markdown.

        Args:
            file_path: Directorio del archivo
            file_name: Nombre del archivo
            refresh_list: Si True, repuebla la lista de archivos marcando el archivo
                abierto. Debe ser False cuando la apertura proviene de un click en la
                propia lista, ya que el widget ya seleccionó el item y repoblar
                reconstruiría el RecycleView en pleno click, rompiendo las animaciones.

        Returns:
            bool: True si el archivo se abrió exitosamente

        Raises:
            ValueError: Si los parámetros son inválidos
            FileNotFoundError: Si el archivo no existe
            PermissionError: Si no hay permisos de lectura
        """
        try:
            # Abrir archivo usando ProjectManager
            self.project_manager.open_file(file_path, file_name)

            # Actualizar editor
            self.populate_doc_editor()
            # Actualizar vista de archivos sólo en aperturas programáticas (no por click).
            # Repoblar en un click reconstruye el RecycleView y arrastra las animaciones
            # de selección a la fila equivocada.
            if refresh_list:
                self.widgets['file_list_view'].populate(
                    folder=file_path,
                    select_file=file_name
                )

            Logger.info(f"KVMarkdownEditorApp: Archivo abierto: {file_name}")
            return True

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)[-1]
            Logger.error(f"KVMarkdownEditorApp: Error al abrir archivo: {e}\n"
                         f"             Modulo: [{tb.filename}:{tb.lineno}]")
            raise

    def save_file(self) -> bool:
        """
        Guarda el archivo markdown actual.

        Returns:
            bool: True si el archivo se guardó exitosamente

        Raises:
            ValueError: Si no hay documento activo
            PermissionError: Si no hay permisos de escritura
            OSError: Si hay error al escribir
        """
        try:
            self.project_manager.save_file()
            Logger.info("KVMarkdownEditorApp: Archivo guardado exitosamente")
            return True

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)[-1]
            Logger.error(f"KVMarkdownEditorApp: Error al guardar archivo: {e}\n"
                         f"             Modulo: [{tb.filename}:{tb.lineno}]")
            raise

    # Document Editor Methods

    def populate_doc_editor(self):
        """
        Puebla el editor con las líneas del documento actual.

        Side Effects:
            Actualiza widgets['doc_editor'] con las líneas del documento
        """


        print(self.project_manager.active_project)


        self.widgets['doc_editor'].populate_md_lines(self.project_manager.md_document)
        Logger.debug(f"KVMarkdownEditorApp: Editor poblado con {len(self.project_manager.md_document.md_lines)} líneas")

    # Event Handlers - Lifecycle

    def on_start(self):
        """
        Callback ejecutado cuando la aplicación inicia.

        Side Effects:
            Carga la sesión anterior si existe
        """
        Logger.info("KVMarkdownEditorApp: Aplicación iniciando")
        App.on_start(self)

        try:
            self._load_session()
        except FileNotFoundError as e:  # Es normal en primera ejecución
            Logger.warning(
                f"KVMarkdownEditorApp: No se encontró archivo de inicializacion de la sesión: {e}"
            )
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)[-1]
            Logger.warning(
                f"KVMarkdownEditorApp: Error al cargar sesión inicial: {e}\n"
                f"              Modulo: [{tb.filename}:{tb.lineno}]"
            )

        Logger.info("KVMarkdownEditorApp: Aplicación iniciada")

    def on_stop(self):
        """
        Callback ejecutado cuando la aplicación se cierra.

        Side Effects:
            Guarda la sesión actual
        """
        Logger.info("KVMarkdownEditorApp: Aplicación cerrando")

        try:
            self._save_session()
        except Exception as e:
            Logger.error(f"KVMarkdownEditorApp: Error al guardar sesión final: {e}")

        App.on_stop(self)
        Logger.info("KVMarkdownEditorApp: Aplicación cerrada")

    # Event Handlers - Project Bar

    def _on_size_prj_btns(self, instance, value):
        """
        Ajusta el tamaño de los botones de la barra de proyecto.

        Args:
            instance: Widget que disparó el evento
            value: Nuevo valor de size
        """
        if instance.height < 30 or instance.height > instance.width:
            instance.height = instance.width
            self.widgets['project_bar_layout'].height = instance.height

    def _on_open_prj(self, instance, touch, keycode):
        """
        Maneja el click en el botón de abrir proyecto.

        Args:
            instance: Botón que disparó el evento
            touch: Información del toque
            keycode: Código de tecla
        """
        Clock.schedule_once(self._open_project_dialog, 0.4)

    def _open_project_dialog(self, dt):
        """
        Abre el diálogo de selección de proyecto.

        Args:
            dt: Delta time (requerido por Clock.schedule_once)
        """
        try:
            selected_folder = self.project_manager.open_project_dialog(
                self.project_manager.active_project
            )

            if selected_folder:
                self.open_project(selected_folder)

        except Exception as e:
            Logger.error(f"KVMarkdownEditorApp: Error al abrir diálogo de proyecto: {e}")

    # Event Handlers - Folder and File Selection

    def _on_select_folder(self, tree, folder, touch):
        """
        Maneja la selección de una carpeta en el árbol.

        Args:
            tree: TreeView que disparó el evento
            folder: Nodo de carpeta seleccionado
            touch: Información del toque

        Side Effects:
            - Reinicia el documento actual
            - Actualiza la lista de archivos
        """
        Logger.debug(f"KVMarkdownEditorApp: Carpeta seleccionada: {folder.path_node}")

        # Reiniciar documento
        self.project_manager.md_document = MDDocument()
        self.widgets['doc_editor'].md_document = self.project_manager.md_document

        # Actualizar lista de archivos
        self.widgets['file_list_view'].folder = folder.path_node

    def _on_select_file(self, instance, data, index):
        """
        Maneja la selección de un archivo en la lista.

        Args:
            instance: FileListView que disparó el evento
            data: Diccionario con datos del archivo seleccionado
            index: Índice del archivo en la lista
        """
        file_name = data.get('file_name', '')
        folder_path = self.widgets['tree_panel'].tree_view.selected_node.path_node

        Logger.debug(f"KVMarkdownEditorApp: Archivo seleccionado: {file_name}")

        try:
            # refresh_list=False: el item ya fue seleccionado por el click en la lista;
            # repoblar reconstruiría el RecycleView y rompería las animaciones.
            self.open_file(folder_path, file_name, refresh_list=False)
        except Exception as e:
            Logger.error(f"KVMarkdownEditorApp: Error al seleccionar archivo: {e}")

    def _on_unselect_file(self, instance, data, index):
        """
        Maneja la deselección de un archivo en la lista.

        Args:
            instance: FileListView que disparó el evento
            data: Diccionario con datos del archivo
            index: Índice del archivo

        Note:
            TODO: Verificar si el archivo se modificó y guardar automáticamente
        """
        Logger.debug("KVMarkdownEditorApp: Archivo deseleccionado")

    def _on_save_file(self, instance, file_name):
        """
        Maneja el evento de guardar archivo.

        Args:
            instance: Widget que disparó el evento
            file_name: Nombre del archivo a guardar
        """
        Logger.info(f"KVMarkdownEditorApp: Guardando archivo: {file_name}")

        try:
            self.save_file()
        except Exception as e:
            Logger.error(f"KVMarkdownEditorApp: Error al guardar: {e}")

    def _on_new_file(self, instance, parent_folder):
        """
        Maneja la creación de un nuevo archivo.

        Args:
            instance: Widget que disparó el evento
            parent_folder: Carpeta padre donde crear el archivo

        Side Effects:
            Actualiza la lista de archivos si la carpeta coincide
        """
        Logger.debug(f"KVMarkdownEditorApp: Nuevo archivo en: {parent_folder}")

        selected_path = self.widgets['tree_panel'].tree_view.selected_node.path_node
        if parent_folder == selected_path:
            self.widgets['file_list_view'].update_folder()

    # Event Handlers - Document Editor

    def _on_select_line(self, instance, data, index):
        """
        Maneja la selección de una línea en el editor.

        Args:
            instance: Editor que disparó el evento
            data: Datos de la línea seleccionada
            index: Índice de la línea
        """
        Logger.debug(f"KVMarkdownEditorApp: Línea seleccionada: {index}")

    def _on_unselect_line(self, instance, data, index):
        """
        Maneja la deselección de una línea en el editor.

        Args:
            instance: Editor que disparó el evento
            data: Datos de la línea
            index: Índice de la línea
        """
        Logger.debug(f"KVMarkdownEditorApp: Línea deseleccionada: {index}")

    # Event Handlers - Search and Filter

    def _on_search_event(self, instance, text):
        """
        Maneja el evento de búsqueda.

        Args:
            instance: InputSearchOrFilter que disparó el evento
            text: Texto de búsqueda ingresado

        Note:
            TODO: Implementar lógica de búsqueda
        """
        Logger.debug(f"KVMarkdownEditorApp: Búsqueda: '{text}'")

    def _on_filter_state_change(self, instance, state):
        """
        Maneja el cambio de estado del filtro (V2 con FilterService).

        Cuando el filtro está activo, usa FilterService integrado en
        MDDocumentEditorV2 para filtrar las líneas. Opcionalmente incluye
        títulos padres para proporcionar contexto.

        Args:
            instance: InputSearchOrFilter que disparó el evento
            state: Estado del filtro ('toggled' o 'normal')

        Side Effects:
            Actualiza el editor con líneas filtradas o completas usando FilterService
        """
        include_parents = (
            self.widgets['search_filter_bar'].include_parents_toggle.state == 'toggled'
        )

        Logger.debug(
            f"KVMarkdownEditorApp V2: Filtro {state}, "
            f"incluir padres: {include_parents}"
        )

        try:
            if state == 'toggled':
                # ✅ V2: Aplicar filtro usando FilterService integrado
                search_text = self.widgets['search_filter_bar'].text

                if search_text.strip():
                    # Usar el método apply_filter() de MDDocumentEditorV2
                    self.widgets['doc_editor'].apply_filter(
                        filter_text=search_text,
                        include_parents=include_parents
                    )
                    Logger.info(
                        f"KVMarkdownEditorApp V2: Filtro aplicado con FilterService "
                        f"(texto='{search_text}', incluir_padres={include_parents})"
                    )
                else:
                    Logger.warning("KVMarkdownEditorApp V2: Texto de búsqueda vacío")
            else:
                # ✅ V2: Quitar filtro usando clear_filter()
                self.widgets['doc_editor'].clear_filter()
                Logger.info("KVMarkdownEditorApp V2: Filtro eliminado")

        except Exception as e:
            Logger.error(f"KVMarkdownEditorApp V2: Error al filtrar: {e}")

    # Debug/Test Event Handlers

    def _on_btn_mdline1_test(self, instance, touch, keycode):
        """Imprime información de todas las líneas del documento."""
        Logger.info("=== MDLine Test - Lista completa ===")
        for line in self.project_manager.md_document.md_lines:
            Logger.info(f"Línea {line.type}: {line.md_text}")

    def _on_btn_mdline_test(self, instance, touch, keycode):
        """Imprime información de líneas con prev/next."""
        Logger.info("=== MDLine Test - Con Prev/Next ===")
        for line in self.project_manager.md_document.md_lines:
            Logger.info("-" * 80)
            if line.prev_line:
                Logger.info(f"Prev: {line.prev_line.md_text}")
            Logger.info(f"Actual: {line.md_text}")
            if line.next_line:
                Logger.info(f"Next: {line.next_line.md_text}")

    def _on_btn_mdtitle_test(self, instance, touch, keycode):
        """Imprime información de títulos y jerarquía."""
        Logger.info("=== MDTitle Test - Jerarquía de títulos ===")

        first_title = self.project_manager.md_document.get_first_title()
        if not first_title:
            Logger.info("No hay títulos en el documento")
            return

        Logger.info(f"Primer título: {first_title.md_text}")

        # Hijos del primer título
        children = first_title.get_title_Childs()
        Logger.info(f"Hijos ({len(children)}):")
        for child in children:
            Logger.info(f"  - {child.md_text}")

        # Padre del primer título
        parent = first_title.get_title_parent()
        if parent:
            Logger.info(f"Padre: {parent.md_text}")
        else:
            Logger.info("Padre: None (es título raíz)")

        # Navegación de títulos
        if len(children) > 1:
            Logger.info(f"Padre de '{children[1].md_text}': {children[1].get_title_parent().md_text}")
            Logger.info(f"Título previo de '{children[1].md_text}': {children[1].get_title_prev().md_text}")
            Logger.info(f"Título siguiente de '{children[0].md_text}': {children[0].get_title_next().md_text}")

            first_child = children[0].get_title_first_child()
            if first_child:
                Logger.info(f"Primer hijo de '{children[0].md_text}': {first_child.md_text}")
