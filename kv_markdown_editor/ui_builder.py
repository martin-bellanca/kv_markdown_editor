#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ui_builder.py
#
#  Copyright 2024 Martin Pablo Bellanca <mbellanca@gmail.com>
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
Construye componentes de interfaz de usuario.

Este módulo es responsable de crear y configurar todos los widgets
de la interfaz de usuario de la aplicación.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy_mpbe_widgets.theming import Theme
from kivy_mpbe_widgets.wg_markdown.md_recycleview_document_editor import MDDocumentEditor
from kivy_mpbe_widgets.wg_labels.font_icon_labels import FontIconLabel
from kivy_mpbe_widgets.wg_buttons.click_buttons import ClickButton, ClickButtonLabel
from kivy_mpbe_widgets.wg_panels.panels import BoxPanel
from kivy_mpbe_widgets.wg_tree_panels.tree_panels import FileTreePanel
from kivy_mpbe_widgets.wg_inputs.inputs import InputSearchOrFilter
from kivy_mpbe_widgets.wg_recycle_list_view.recycle_list_view import FileListView


class UIConstants:
    """Constantes de configuración de UI."""

    # Splitter
    SIDEBAR_WIDTH_RATIO = 0.3
    SIDEBAR_MAX_WIDTH = 500
    SIDEBAR_MIN_WIDTH = 200
    SPLITTER_STRIP_WIDTH = 8

    # Heights
    SEARCH_BAR_HEIGHT = 36
    BUTTON_TEST_HEIGHT = 30

    # Icons
    ICON_NEW_PROJECT = 'new-box'
    ICON_OPEN_PROJECT = 'archive'
    ICON_HELP = 'help-circle-outline'
    ICON_SIZE = 28


class UIBuilder:
    """
    Construye y configura componentes de interfaz de usuario.

    Responsable de crear todos los widgets de la aplicación y
    ensamblarlos en la estructura de layout correcta.
    """

    def __init__(self, theme: Theme):
        """
        Inicializa el constructor de UI.

        Args:
            theme: Instancia de Theme para aplicar estilos
        """
        self.theme = theme
        self.sp = theme.geometry['spacing']
        self.pa = theme.geometry['padding']

    def build_main_layout(self) -> tuple[BoxLayout, dict]:
        """
        Construye el layout principal de la aplicación.

        Returns:
            tuple: (layout_raiz, widgets_dict) donde widgets_dict contiene:
                - 'splitter': Widget Splitter
                - 'doc_editor': Editor de documento markdown
                - 'sidebar_layout': Layout de la barra lateral
                - 'editor_layout': Layout del editor
        """
        # Layout principal horizontal
        layout = BoxLayout(orientation='horizontal')

        # Splitter para panel izquierdo
        splitter = Splitter(
            sizable_from='right',
            size_hint=(UIConstants.SIDEBAR_WIDTH_RATIO, 1),
            max_size=UIConstants.SIDEBAR_MAX_WIDTH,
            min_size=UIConstants.SIDEBAR_MIN_WIDTH,
            strip_size=UIConstants.SPLITTER_STRIP_WIDTH
        )
        layout.add_widget(splitter)

        # Layout del editor (panel derecho)
        editor_layout = BoxLayout(orientation='vertical')
        layout.add_widget(editor_layout)

        # Editor de documento markdown
        doc_editor = MDDocumentEditor(size_hint=(1, 1))
        doc_editor.viewclass = 'MDDocumentLineEditor'
        editor_layout.add_widget(doc_editor)

        # Layout de barra lateral (panel izquierdo)
        sidebar_layout = BoxLayout(
            orientation='vertical',
            spacing=self.sp,
            padding=self.pa,
            size_hint=(None, 1)
        )
        splitter.add_widget(sidebar_layout)

        widgets = {
            'splitter': splitter,
            'doc_editor': doc_editor,
            'sidebar_layout': sidebar_layout,
            'editor_layout': editor_layout
        }

        return layout, widgets

    def build_project_bar(self) -> tuple[BoxLayout, dict]:
        """
        Construye la barra de herramientas del proyecto.

        Returns:
            tuple: (layout_bar, buttons_dict) donde buttons_dict contiene:
                - 'btn_new_prj': Botón nuevo proyecto
                - 'btn_open_prj': Botón abrir proyecto
                - 'btn_help': Botón ayuda
        """
        # Layout horizontal para la barra
        project_bar_layout = BoxLayout(
            orientation='horizontal',
            spacing=self.sp,
            padding=0,
            size_hint=(1, None)
        )

        # Botón Nuevo Proyecto
        icon = FontIconLabel(
            icon_name=UIConstants.ICON_NEW_PROJECT,
            icon_size=UIConstants.ICON_SIZE
        )
        btn_new_prj = ClickButtonLabel(label=icon, size_hint=(1, None))
        project_bar_layout.add_widget(btn_new_prj)

        # Botón Abrir Proyecto
        icon = FontIconLabel(
            icon_name=UIConstants.ICON_OPEN_PROJECT,
            icon_size=UIConstants.ICON_SIZE
        )
        btn_open_prj = ClickButtonLabel(label=icon, size_hint=(1, None))
        project_bar_layout.add_widget(btn_open_prj)

        # Botón Ayuda
        icon = FontIconLabel(
            icon_name=UIConstants.ICON_HELP,
            icon_size=UIConstants.ICON_SIZE
        )
        btn_help = ClickButtonLabel(label=icon, size_hint=(1, None))
        project_bar_layout.add_widget(btn_help)

        buttons = {
            'btn_new_prj': btn_new_prj,
            'btn_open_prj': btn_open_prj,
            'btn_help': btn_help,
            'layout': project_bar_layout
        }

        return project_bar_layout, buttons

    def build_search_filter_bar(self) -> InputSearchOrFilter:
        """
        Construye la barra de búsqueda y filtrado.

        Returns:
            InputSearchOrFilter: Widget de búsqueda/filtro configurado
        """
        search_filter_bar = InputSearchOrFilter(
            size_hint_y=None,
            height=UIConstants.SEARCH_BAR_HEIGHT
        )
        return search_filter_bar

    def build_file_tree_panel(self, root_path: str) -> FileTreePanel:
        """
        Construye el panel de árbol de archivos.

        Args:
            root_path: Ruta raíz del árbol de archivos

        Returns:
            FileTreePanel: Panel de árbol configurado
        """
        tree_panel = FileTreePanel(root_path, show_files=False)
        tree_panel.transparent = True
        return tree_panel

    def build_file_list_view(self, folder: str, extensions: str) -> tuple[BoxPanel, FileListView]:
        """
        Construye la vista de lista de archivos.

        Args:
            folder: Carpeta inicial
            extensions: Extensiones de archivo a mostrar (separadas por comas)

        Returns:
            tuple: (panel_contenedor, file_list_view)
        """
        # Panel contenedor
        panel = BoxPanel(padding=(0, 0))
        panel.transparent = True

        # Vista de lista de archivos
        file_list_view = FileListView(folder=folder, extensions=extensions)
        panel.container.add_widget(file_list_view)

        return panel, file_list_view

    def build_debug_buttons(self) -> dict:
        """
        Construye botones de debug/test.

        Returns:
            dict: Diccionario con botones de debug:
                - 'btn_mdline1': Botón imprimir MDLine
                - 'btn_mdline': Botón imprimir MDLine P-N
                - 'btn_mdtitle': Botón imprimir títulos
        """
        # Botón Print MDLine
        btn_mdline1 = ClickButton(
            text='Print MDLine',
            size_hint=(1, None),
            height=UIConstants.BUTTON_TEST_HEIGHT
        )
        btn_mdline1.is_focusable = False

        # Botón Print MDLine P-N
        btn_mdline = ClickButton(
            text='Print MDLine P-N',
            size_hint=(1, None),
            height=UIConstants.BUTTON_TEST_HEIGHT
        )
        btn_mdline.is_focusable = False

        # Botón Print Titles
        btn_mdtitle = ClickButton(
            text='Print Titles',
            size_hint=(1, None),
            height=UIConstants.BUTTON_TEST_HEIGHT
        )
        btn_mdtitle.is_focusable = False

        return {
            'btn_mdline1': btn_mdline1,
            'btn_mdline': btn_mdline,
            'btn_mdtitle': btn_mdtitle
        }

    def build_complete_ui(self, active_project: str, md_extensions: str,
                         include_debug_buttons: bool = True) -> dict:
        """
        Construye la interfaz de usuario completa.

        Args:
            active_project: Ruta del proyecto activo
            md_extensions: Extensiones de archivo markdown (separadas por comas)
            include_debug_buttons: Si True, incluye botones de debug

        Returns:
            dict: Diccionario con todos los widgets creados:
                - 'root_layout': Layout principal
                - 'splitter': Splitter
                - 'doc_editor': Editor de documento
                - 'sidebar_layout': Layout barra lateral
                - 'project_bar_layout': Layout barra proyecto
                - 'btn_new_prj': Botón nuevo proyecto
                - 'btn_open_prj': Botón abrir proyecto
                - 'btn_help': Botón ayuda
                - 'search_filter_bar': Barra de búsqueda/filtro
                - 'tree_panel': Panel árbol de archivos
                - 'file_list_panel': Panel contenedor de lista
                - 'file_list_view': Vista de lista de archivos
                - 'btn_mdline1': Botón debug (opcional)
                - 'btn_mdline': Botón debug (opcional)
                - 'btn_mdtitle': Botón debug (opcional)
        """
        # Layout principal
        root_layout, main_widgets = self.build_main_layout()
        sidebar_layout = main_widgets['sidebar_layout']

        # Barra de proyecto
        project_bar_layout, project_buttons = self.build_project_bar()
        sidebar_layout.add_widget(project_bar_layout)

        # Barra de búsqueda/filtro
        search_filter_bar = self.build_search_filter_bar()
        sidebar_layout.add_widget(search_filter_bar)

        # Panel de árbol de archivos
        tree_panel = self.build_file_tree_panel(active_project)
        sidebar_layout.add_widget(tree_panel)

        # Vista de lista de archivos
        file_list_panel, file_list_view = self.build_file_list_view(
            folder=active_project,
            extensions=md_extensions
        )
        sidebar_layout.add_widget(file_list_panel)

        # Actualizar folder del file_list_view con el root_path del tree
        file_list_view.folder = tree_panel.tree_view.root_path

        # Compilar todos los widgets
        all_widgets = {
            'root_layout': root_layout,
            'splitter': main_widgets['splitter'],
            'doc_editor': main_widgets['doc_editor'],
            'sidebar_layout': sidebar_layout,
            'editor_layout': main_widgets['editor_layout'],
            'project_bar_layout': project_bar_layout,
            'btn_new_prj': project_buttons['btn_new_prj'],
            'btn_open_prj': project_buttons['btn_open_prj'],
            'btn_help': project_buttons['btn_help'],
            'search_filter_bar': search_filter_bar,
            'tree_panel': tree_panel,
            'file_list_panel': file_list_panel,
            'file_list_view': file_list_view
        }

        # Agregar botones de debug si está habilitado
        if include_debug_buttons:
            debug_buttons = self.build_debug_buttons()
            sidebar_layout.add_widget(debug_buttons['btn_mdline1'])
            sidebar_layout.add_widget(debug_buttons['btn_mdline'])
            sidebar_layout.add_widget(debug_buttons['btn_mdtitle'])
            all_widgets.update(debug_buttons)

        return all_widgets
