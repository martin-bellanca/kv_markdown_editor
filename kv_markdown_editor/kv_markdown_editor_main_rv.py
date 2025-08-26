#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kv_markdown_editor_main.py
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

'''
Created on 30/09/2024
@author: mpbe
'''

# system imports ------------------------------------------------------------
import os
import sys
import codecs
import json
from string import Template
from requests import get
# from markdown import markdown
from configparser import ConfigParser # Importante para guardar config.ini
# from helpers_mpbe.python import FolderWrapper
# Kivy imports -------------------------------------------------------------
import kivy
kivy.require('2.1.0')
from kivy.logger import Logger
from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.splitter import Splitter
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Kivy_dkw imports -------------------------------------------------------------
from kivy_mpbe_widgets.theming import Theme
from kivy_mpbe_widgets.wg_undo.undo_manager import UndoManager, Command
from kivy_mpbe_widgets.wg_markdown import MD_LINE_TYPE
from kivy_mpbe_widgets.wg_markdown.md_document import MDLine, MDDocument
from kivy_mpbe_widgets.wg_markdown.md_recycleview_editors import MDDocumentLineEditor, MDDocumentEditor, DocLineDataDic
from kivy_mpbe_widgets.wg_labels.image_labels import ImageLabel, ImageWText
from kivy_mpbe_widgets.wg_labels.font_icon_labels import FontIconLabel, FontIconWText
from kivy_mpbe_widgets.wg_buttons.click_buttons import ClickButton, ClickButtonLabel
from kivy_mpbe_widgets.wg_panels.panels import BoxPanel
from kivy_mpbe_widgets.wg_tree_panels.tree_panels import FileTreePanel
from kivy_mpbe_widgets.wg_lists.list_view import ListView  # Obsoleto
from kivy_mpbe_widgets.wg_inputs.inputs import InputSearchOrFilter
from kivy_mpbe_widgets.wg_recycle_list_view.recycle_list_view import FileListView
from kivy_mpbe_widgets.wg_lists.items import FileItem
# App imports -------------------------------------------------------------
import __init__ as kv_md_editor
from tkinter import Tk, filedialog  # Para el selector del directorio de proyecto


class KVMarkdownEditorApp(App):
    theme = Theme(name='flat_light', style='light')
    title = "Test Markdown"

    def __init__(self, **kwargs):
        super(KVMarkdownEditorApp, self).__init__(**kwargs)

        print('+++ INITIALIZE APP +++++++++++++++')
        # self.md_extensions = ['md', 'markdown', 'mdown', 'mkdn', 'mkd', 'mdtxt', 'mdtext']
        self._undo_manager = UndoManager()
        self.md_extensions = 'md, markdown, mdown, mkdn, mkd, mdtxt, mdtext'
        self._title = "KV Markdown Editor (" + kv_md_editor.__version__ +" - RecycleView)"
        self.title = self._title
        # Variables internas ------------------------------------------------
        self.md_document = MDDocument()
        self.active_project = ''  # "/home/mpbe/Documentos/Programacion/Programacion_lin/PyCharmProjects/kv_markdown_editor_prj/Doc_Markdown_Pruebas"
        self._config_file = 'config.ini'
        
        print('+++ INITIALIZE APP -> OK')

    def build_settings(self, settings):
        """Panel de configuración de la aplicación. Se llama con F1"""
        # Configuración de la aplicación
        # VER COMO SE CONFIGURA
        settings.add_json_panel('KV Markdown Editor',
                                self.config,
                                data='''
                                [
                                    {"type": "title",
                                    "title": "KV Markdown Editor",
                                    "collapsable": false,
                                    "open": false
                                    }]''')
        return super().build_settings(settings) # Configuración de la aplicación

    def build_config(self, config):
        pass
        # # Configuracion de la aplicacion
        # config.setdefaults('app', {
        #     'theme': 'flat_light',
        #     'style': 'light',
        #     'window_size': (1700, 900),
        #     'window_position': (100, 100),
        #     'window_maximized': False,
        #     'window_fullscreen': False,
        # })
        # config.setdefaults('project', {
        #     'active_project': '/home/mpbe/Documentos/Programacion_lin/PyCharmProjects/kv_markdown_editor_prj/Doc_Markdown_Pruebas',
        #     'active_file': 'Base_001.markdown'
        # })
        # Configuracion del tema
        # self.theme.load_config(config)
        # Proyecto activo ------------------------------------------------
        # self.active_project = "/home/mpbe/Documentos/Programacion_lin/PyCharmProjects/kv_markdown_editor_prj/Doc_Markdown_Pruebas"


    def build(self):
        print('+++ Build User Interfaz ++++++++++')
        Window.clearcolor = self.theme.style['background_app']
        sp = self.theme.geometry['spacing']
        pa = self.theme.geometry['padding']
        layout = BoxLayout(orientation='horizontal')
        # Splitter --------------------------------
        self.splitter = Splitter(sizable_from='right', size_hint=(0.3, 1), max_size=500,min_size=200, strip_size=8)
        layout.add_widget(self.splitter)
        # Layout del Editor -----------------------
        lay_edit = BoxLayout(orientation='vertical')
        layout.add_widget(lay_edit)
        ### Markdown Editor -----------------------
        self.doc_editor = MDDocumentEditor(size_hint=(1,1))
        self.doc_editor.viewclass = 'MDDocumentLineEditor'
        self.doc_editor.bind(on_select_item=self._on_select_line, on_unselect_item=self._on_unselect_line)
        # self.doc_editor.focus = True
        lay_edit.add_widget(self.doc_editor)
        print('---- Document Editor -> OK')
        # Layout de barra lateral -----------------
        lay_lateral_bar = BoxLayout(orientation='vertical', spacing=sp, padding=pa, size_hint=(None, 1))
        self.splitter.add_widget(lay_lateral_bar)
        ### File Bar ------------------------------
        lay_lateral_bar.add_widget(self._ui_project_bar())
        ### Search or Filter Bar ------------------
        self.search_filter_bar = InputSearchOrFilter(size_hint_y=None, height=36)
        self.search_filter_bar.bind(on_search=self._on_search_event)
        self.search_filter_bar.bind(filter_state=self._on_filter_state_change)
        # self.search_filter_bar.bind(parent_selection_state=self._on_parent_selection_state_change)
        lay_lateral_bar.add_widget(self.search_filter_bar)
        ### Tree Project --------------------------
        self.tree_prj = FileTreePanel(self.active_project, show_files=False)
        self.tree_prj.tree_view.bind(on_tree_node_selected=self._on_select_folder)
        self.tree_prj.tree_view.bind(on_new_file=self._on_new_file)
        # self.tree_prj.is_focusable = False
        self.tree_prj.transparent = True

        lay_lateral_bar.add_widget(self.tree_prj)
        print('---- Tree Project -> OK')
        ### Files view ----------------------------
        bpanel = BoxPanel(padding=(0, 0))
        bpanel.transparent = True
        lay_lateral_bar.add_widget(bpanel)
        self.files_view = FileListView(folder=self.active_project, extensions=self.md_extensions)
        # self.files_view.is_focusable = False
        bpanel.container.add_widget(self.files_view)
        ### Actualizacion de la Interfaz ----------
        self.files_view.folder = self.tree_prj.tree_view.root_path
        # ---------------------------------------------------------------------
        # Events --------------------------------------------------------------
        # self.tree_prj.bind(on_tree_node_selected=self._on_select_folder)
        self.files_view.bind(on_select_item=self._on_select_file, on_unselect_item=self._on_unselect_file)
        # self.files_view.bind(on_delete_file=self._on_delete_file)
        self.files_view.bind(on_save_file=self._on_save_file)
        print('---- File View -> OK')
        ### BOTONES PARA TESTS ============================================================
        ### IMPRIMIR LISTADO MDLine
        self.btn_mdline1 = ClickButton(text='Print MDLine', size_hint=(1, None))
        self.btn_mdline1.is_focusable = False
        self.btn_mdline1.height = 30
        self.btn_mdline1.bind(on_click=self._on_btn_mdline1_test)
        lay_lateral_bar.add_widget(self.btn_mdline1)
        ### IMPRIMIR LISTADO MDLine con P-N
        self.btn_mdline = ClickButton(text='Print MDLine P-N', size_hint=(1, None))
        self.btn_mdline.is_focusable = False
        self.btn_mdline.height = 30
        self.btn_mdline.bind(on_click=self._on_btn_mdline_test)
        lay_lateral_bar.add_widget(self.btn_mdline)
        ### IMPRIMIR TITULOS
        self.btn_mdtitle = ClickButton(text='Print Titles', size_hint=(1, None))
        self.btn_mdtitle.is_focusable = False
        self.btn_mdtitle.height = 30
        self.btn_mdtitle.bind(on_click=self._on_btn_mdtitle_test)
        lay_lateral_bar.add_widget(self.btn_mdtitle)
        print('+++ Build User Interfaz -> OK')
        return layout

    """ Sesion Funtions ----------------------------------------------------------------"""    
    def _load_sesion(self):
        """
        Carga la configuración de la aplicación desde un archivo.

        Lee la posición y el tamaño de la ventana, el proyecto activo
        y el archivo activo.
        """
        Logger.info('Carga y configura la sesion de la aplicación.-----------------------')
        print(str(kv_md_editor.DIR_APP / self._config_file))
        file = str(kv_md_editor.DIR_APP / self._config_file)
        if not os.path.exists(file):
            Logger.error(f"Archivo de configuración '{self._config_file}' NO ENCONTRADO.")
            return False
        # Lee el archivo y carga los datos en el objeto global Config de Kivy
        Config.read(file)  # NO LEE EL ARCHIVO
        # Establecer la configuración de la ventana antes de que se cree
        w = Config.getint('Window', 'width', fallback='800')
        h = Config.getint('Window', 'height', fallback='600')
        l = Config.getint('Window', 'left', fallback=100)
        t = Config.getint('Window', 'top', fallback=100)
        # Configuración de la ventana
        Window.size = (w, h)
        Window.left = l
        Window.top = t
        # Configuración del proyecto
        self.open_prj(Config.get('Project', 'active_project', fallback=None))
        active_file = Config.get('Project', 'active_file', fallback=None)
        if not os.path.exists(self.active_project+os.sep+active_file):
            Logger.error(f"El archivo activo '{active_file}' no existe en el proyecto '{self.active_project}'.")
            active_file = None
        else:
            self.open_file(self.active_project, active_file)

    def _save_sesion(self):
        """
        Guarda la configuración actual de la aplicación.

        Guarda la posición y tamaño de la ventana, el proyecto activo
        y el archivo activo.
        """
        # Kivy no actualiza el ConfigParser principal, así que creamos uno nuevo
        config = ConfigParser()
        config.add_section('Window')
        config.set('Window', 'width', str(Window.width))
        config.set('Window', 'height', str(Window.height))
        config.set('Window', 'left', str(Window.left))
        config.set('Window', 'top', str(Window.top))
        
        # Configuración del Proyecto
        config.add_section('Project')
        project = self.active_project or ''
        config.set('Project', 'active_project', (self.active_project or ''))
        config.set('Project', 'active_file', (self.md_document.doc_name or ''))

        # Guardar la configuración en el archivo
        file = str(kv_md_editor.DIR_APP / self._config_file)
        with open(file, 'w') as f:
            config.write(f)

        Logger.info(f"Configuración guardada en {file}")




    """ UI Funtions ----------------------------------------------------------------"""
    def _ui_project_bar(self):
        sp = self.theme.geometry['spacing']
        ### File Bar layout -----------------------
        self.lay_prj_bar = BoxLayout(orientation='horizontal', spacing=sp, padding=0, size_hint=(1, None))
        ##### Btn New Project ------------------------
        icon = FontIconLabel(icon_name='new-box', icon_size=28)
        self.btn_new_prj = ClickButtonLabel(label=icon, size_hint=(1, None))
        # self.btn_new_prj.is_focusable = False
        # self.btn_new_prj = ClickButton(text_label='N', size_hint=(1, None))
        self.btn_new_prj.bind(size=self._on_size_prj_btns)
        self.lay_prj_bar.add_widget(self.btn_new_prj)
        ##### Btn Open Prohect -----------------------
        icon = FontIconLabel(icon_name='archive', icon_size=28)
        self.btn_open_prj = ClickButtonLabel(label=icon, size_hint=(1, None))
        # self.btn_open_prj.is_focusable = False
        # self.btn_open_prj = ClickButton(text_label='O', size_hint=(1, None))
        self.btn_open_prj.bind(size=self._on_size_prj_btns)
        self.btn_open_prj.bind(on_click=self._on_open_prj)
        self.lay_prj_bar.add_widget(self.btn_open_prj)
        ##### Btn Help -------------------------------
        icon = FontIconLabel(icon_name='help-circle-outline', icon_size=28)
        self.btn_help = ClickButtonLabel(label=icon, size_hint=(1, None))
        # self.btn_help = ClickButton(text_label='H', size_hint=(1, None))
        # self.btn_help.is_focusable = False
        self.btn_help.bind(size=self._on_size_prj_btns)
        self.lay_prj_bar.add_widget(self.btn_help)
        return self.lay_prj_bar

    def _open_folderchooser(self, initial_directory):
        # Ocultar la ventana principal de tkinter
        root = Tk()
        root.withdraw()
        # Abrir el diálogo para seleccionar un directorio
        selected_directory = filedialog.askdirectory(initialdir=initial_directory)
        # Cerrar la ventana de tkinter
        root.destroy()
        return selected_directory

    def open_prj(self, folder:str):
        if folder:
            self.tree_prj.tree_view.root_path = folder
            self.files_view.folder = folder
            self.active_project = folder

    def on_open_prj(self, dt):
        sel_folder = self._open_folderchooser(self.active_project)  # kivy_dkw.PATH_HOME
        self.open_prj(sel_folder)

    def open_file(self, file_path, file_name):
        if os.path.isfile(file_path+os.sep+file_name):
            self.md_document.load_doc(file_path, file_name)
            self.populate_doc_editor()
            self.files_view.populate(folder=file_path, select_file=file_name)
            # hay que seleccionar el archivo en el recycleview
            # self.files_view.select_item(file_name)

            return True
        else:
            Logger.error(f"Error: El archivo {file_path+os.sep+file_name} no existe o no es un archivo válido.")
            return False

    # def _populate_file_view(self, folder):
    #     # try:
    #     wrapper = FolderWrapper(folder)
    #     lstfolders, lstfiles = wrapper.getChildsNames(sorted, show_hidden=False, filters=self.md_extensions)
    #     self.files_view.clear_items()
    #     for fl in lstfiles:
    #         it = FileItem(fl, icon_name='file-document', icon_size=18)
    #         it.btn_save.bind(on_click=self._on_save_file)
    #         # AGREGAR BIND A BOTON OPTIONS. VER SI PUEDO CAPTURAR BOTON DERECHO Y TAP LARGO O DOBLE CLICK
    #
    #         self.files_view.add_item(it)
    #     # except:
    #     #     print("Error al cargar el proyecto. Verificar si existe el directorio")
    # # Funciones de archivos ----------------------------------------------
    # # def _new_mdfile(self):
    # #     # Crea el texto Markdown de prueba (BORRAR)
    # #     lines = [MDLine(md_text='# Titulo', prev_line=None, next_line=None)]
    # #     for i in range(1, 20):
    # #         mdt = '**Linea {}** Linea de texto jfasd'.format(str(i + 1))
    # #         lines.append(MDLine(md_text=mdt, prev_line=None, next_line=None))
    # #     return lines

    ' MDDocument Functions -----------------------------------------------------------'
    def populate_doc_editor(self):
        # self.doc_editor.initialize_document()
        # self.doc_editor.data = []
        # for id, mdl in enumerate(self.md_document.md_lines, start=1):
        #     data_line = DocLineDataDic(id, mdl)
        #     dic_line = data_line.to_dict()
        #     self.doc_editor.data.append(dic_line)
        # #self.doc_editor.refresh_from_data()
        self.doc_editor.populate_from_md_lines(self.md_document.md_lines)
        pass

    """ Events Funtions --------------------------------------------------------------"""
    def on_start(self):
        print("+++ On Start +++++++++++++++++++++")
        App.on_start(self)
        # update widgets to the last session -----------------
        # Window.size = (1700, 900)
        try:
            self._load_sesion()  # Carga la informacion de la ultima sesion
        except Exception as e:
            print(f'Warning:  {self.__class__} Se produjo un error al iniciar Task-txt. Detalle: {e}')
        print("+++ On Start -> OK")

    def on_stop(self):
        self._save_sesion()
        App.on_stop(self)

    '-- Events project bar -------------------------------------------------------------'
    def _on_size_prj_btns(self, instance, value):
        if instance.height < 30 or instance.height > instance.width:
            instance.height = instance.width
            self.lay_prj_bar.height = instance.height

    def _on_select_folder(self, tree, folder, touch):
        # print("KVMarkdownEditor._on_select_folder")
        self.md_document = MDDocument()
        self.doc_editor.md_document = self.md_document
        self.files_view.folder = folder.path_node

    def _on_open_prj(self, instance, touch, keycode):
        Clock.schedule_once(self.on_open_prj, 0.4)

    '-- Eventos of the files ------------------------------------------------------------'
    def _on_select_file(self, instance, data, index):
        # self.md_document.load_doc(self.tree_prj.tree_view.selected_node.path_node, data['file_name'])  # lee el archivo
        # self.populate_doc_editor()
        self.open_file(self.tree_prj.tree_view.selected_node.path_node, data['file_name'])

    def _on_unselect_file(self, instance, data, index):
        # TODO: Verificar si el archivo se modifico y guardar
        pass

    def _on_save_file(self, instance, file_name):
        file = self.active_project+os.sep+file_name
        print(f'Guardar el archivo {file}')
        self.md_document.join_lines()
        self.md_document.save_doc()

    def _on_new_file(self, instance, parent_folder):
        print(f"KVMarkdownEditorApp._on_new_file - {parent_folder}")
        sel_path = self.tree_prj.tree_view.selected_node.path_node
        if parent_folder == sel_path:
            self.files_view.update_folder()


    # def _on_delete_file(self, file_name):
    #     # TODO: Verificar si el archivo es el activo blanquear la interfaz
    #     pass

    '-- Eventos de Document Editor ------------------------------------------------------'
    def _on_select_line(self, instance, data, index):
        'Eveto lanzado con la seleccion de una linea en Document Editor'
        # print(f'KVMarkdownEditorApp._on_select_line -> {index} - name {data}')
        pass

    def _on_unselect_line(self, instance, data, index):
        'Eveto lanzado con la seleccion de una linea en Document Editor'
        # print(f'KVMarkdownEditorApp._on_select_line -> {index} - name {data}')
        pass

    '-- Eventos de Search or Filter Bar --------------------------------------------------'
    def _on_search_event(self, instance, text):
        print(f"Search event triggered with text: '{text}'")
        # Lógica de búsqueda futura aquí

    def _on_filter_state_change(self, instance, state):
        # Lógica de filtro futura aquí
        include_parents = self.search_filter_bar.include_parents_toggle.state == 'toggled'
        print(f"+++++++++ Filter state changed to: {state}, include parents: {include_parents}")
        if state == 'toggled':  ## SEGUIR DE ACA
            # Aplicar el filtro
            filtered_lines = self.md_document.filter_lines(self.search_filter_bar.text, include_parents=include_parents)
            self.doc_editor.populate_from_md_lines(filtered_lines)
        else:
            # Quitar el filtro
            self.doc_editor.populate_from_md_lines(self.md_document.md_lines)


    # EVENTOS DE BOTONES DE TESTEO ==============================================================
    def _on_btn_mdline_test(self, instance, touch, keycode):
        for ll in self.md_document.md_lines:
            print("----------------------------------------------------------------------------")
            if ll.prev_line:
                print(f"Prev line: {ll.prev_line.md_text}")
            print(f"Actual Line: {ll.md_text}")
            if ll.next_line:
                print(f"next Line: {ll.next_line.md_text}")

    def _on_btn_mdline1_test(self, instance, touch, keycode):
        for ll in self.md_document.md_lines:
            print(f"Actual Line {ll.type}: {ll.md_text}")

    def _on_btn_mdtitle_test(self, instance, touch, keycode):
        ft = self.md_document.get_first_title()
        if ft:
            print(f"Primer Titulo: {ft.md_text}")
            chs = ft.get_title_Childs()
            print("Hijos ---------------------")
            for ch in chs:
                print(ch.md_text)
            print("Padre ---------------------")
            tp = ft.get_title_parent()
            if tp == None:
                tpt = "None, No tiene Padre"
            else:
                tpt = tp.md_text
            print(f"El padre de {ft.md_text} es {tpt}")
            print(f"El padre de {chs[1].md_text} es {chs[1].get_title_parent().md_text}")
            print("Titulo Prev --------------")
            print(f"El titulo Previo de {chs[1].md_text} es {chs[1].get_title_prev().md_text}")
            print("Titulo Next --------------")
            print(f"El titulo Posterior de {chs[0].md_text} es {chs[0].get_title_next().md_text}")
            print("Titulo Primer Hijo --------------")
            print(f"El titulo Posterior de {chs[0].md_text} es {chs[0].get_title_first_child().md_text}")


if __name__ == "__main__":
    print()
    print("python version: %s.%s.%s" % sys.version_info[:3])
    print("Kivy version: " + kivy.__version__)
    print("KV Markdown Editor version: " + kv_md_editor.__version__)
    print("Licencia: " + kv_md_editor.__license__)
    print("Autor: " + kv_md_editor.__author__)
    print()
    print("DIR_APP: " + kv_md_editor.DIR_APP)
    print("DIR_BASE: " + kv_md_editor.DIRBASE)
    print("PATH_HOME: " + kv_md_editor.PATH_HOME)
    print("KV_DIRECTORY: " + kv_md_editor.KV_DIRECTORY)
    print()
    KVMarkdownEditorApp().run()