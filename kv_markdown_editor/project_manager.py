#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  project_manager.py
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
Gestiona operaciones de proyectos y archivos markdown.

Este módulo maneja la apertura de proyectos, lectura/escritura de archivos
markdown, y operaciones relacionadas con la gestión de archivos.
"""

import os
from pathlib import Path
from tkinter import Tk, filedialog
from kivy.logger import Logger
from helpers_mpbe.markdown_document.md_document import MDDocument


class ProjectManager:
    """
    Administra operaciones de proyectos y archivos markdown.

    Responsable de abrir/cerrar proyectos, leer/guardar archivos,
    y mantener el estado del proyecto y documento activo.
    """

    def __init__(self, md_document: MDDocument = None):
        """
        Inicializa el gestor de proyectos.

        Args:
            md_document: Instancia de MDDocument a usar (si es None, crea una nueva)
        """
        self.md_document = md_document or MDDocument()
        self.active_project = ''
        self.md_extensions = ['md', 'markdown', 'mdown', 'mkdn', 'mkd', 'mdwn']

    def get_extensions_string(self) -> str:
        """
        Obtiene las extensiones soportadas como string separado por comas.

        Returns:
            str: Extensiones separadas por comas (ej: 'md,markdown,mdown')
        """
        return ','.join(self.md_extensions)

    def is_markdown_file(self, filename: str) -> bool:
        """
        Verifica si un archivo tiene extensión markdown válida.

        Args:
            filename: Nombre del archivo a verificar

        Returns:
            bool: True si el archivo tiene extensión markdown válida
        """
        if not filename:
            return False

        extension = Path(filename).suffix.lstrip('.')
        return extension.lower() in self.md_extensions

    def open_project_dialog(self, initial_directory: str = None) -> str:
        """
        Abre diálogo nativo del sistema para seleccionar directorio de proyecto.

        Args:
            initial_directory: Directorio inicial del diálogo (default: directorio home)

        Returns:
            str: Ruta del directorio seleccionado, o cadena vacía si se canceló

        Note:
            Usa tkinter para el diálogo nativo del sistema operativo
        """
        try:
            # Ocultar ventana principal de tkinter
            root = Tk()
            root.withdraw()

            # Abrir diálogo para seleccionar directorio
            selected_directory = filedialog.askdirectory(
                initialdir=initial_directory or os.path.expanduser('~'),
                title="Seleccionar Proyecto Markdown"
            )

            # Cerrar ventana de tkinter
            root.destroy()

            if selected_directory:
                Logger.info(f"ProjectManager: Proyecto seleccionado: {selected_directory}")

            return selected_directory or ''

        except Exception as e:
            Logger.error(f"ProjectManager: Error al abrir diálogo de proyecto: {e}")
            return ''

    def validate_project_folder(self, folder: str) -> bool:
        """
        Valida que una carpeta sea un directorio válido para proyecto.

        Args:
            folder: Ruta de la carpeta a validar

        Returns:
            bool: True si la carpeta es válida

        Raises:
            ValueError: Si la carpeta es None o vacía
            FileNotFoundError: Si la carpeta no existe
            NotADirectoryError: Si la ruta no es un directorio
            PermissionError: Si no hay permisos de lectura
        """
        if not folder:
            raise ValueError("La ruta del proyecto no puede estar vacía")

        folder_path = Path(folder)

        if not folder_path.exists():
            raise FileNotFoundError(f"El directorio no existe: {folder}")

        if not folder_path.is_dir():
            raise NotADirectoryError(f"La ruta no es un directorio: {folder}")

        if not os.access(folder, os.R_OK):
            raise PermissionError(f"Sin permisos de lectura en: {folder}")

        return True

    def open_project(self, folder: str) -> bool:
        """
        Abre un proyecto markdown desde un directorio.

        Args:
            folder: Ruta del directorio del proyecto

        Returns:
            bool: True si el proyecto se abrió exitosamente

        Raises:
            ValueError: Si la carpeta es inválida
            FileNotFoundError: Si la carpeta no existe
            NotADirectoryError: Si no es un directorio
            PermissionError: Si no hay permisos
        """
        if not folder:
            return False

        # Validar carpeta
        self.validate_project_folder(folder)

        # Establecer proyecto activo
        self.active_project = folder
        Logger.info(f"ProjectManager: Proyecto abierto: {folder}")

        return True

    def validate_file_path(self, file_path: str, file_name: str) -> Path:
        """
        Valida que un archivo existe y es accesible.

        Args:
            file_path: Directorio del archivo
            file_name: Nombre del archivo

        Returns:
            Path: Objeto Path del archivo completo

        Raises:
            ValueError: Si los parámetros están vacíos o el archivo no es markdown
            FileNotFoundError: Si el archivo no existe
            PermissionError: Si no hay permisos de lectura
        """
        if not file_path or not file_name:
            raise ValueError("La ruta y nombre del archivo son requeridos")

        if not self.is_markdown_file(file_name):
            raise ValueError(
                f"El archivo debe tener extensión markdown válida. "
                f"Extensiones permitidas: {', '.join(self.md_extensions)}"
            )

        full_path = Path(file_path) / file_name

        if not full_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {full_path}")

        if not full_path.is_file():
            raise ValueError(f"La ruta no es un archivo: {full_path}")

        if not os.access(full_path, os.R_OK):
            raise PermissionError(f"Sin permisos de lectura en: {full_path}")

        return full_path

    def open_file(self, file_path: str, file_name: str) -> bool:
        """
        Abre un archivo markdown.

        Args:
            file_path: Directorio del archivo
            file_name: Nombre del archivo

        Returns:
            bool: True si el archivo se abrió exitosamente

        Raises:
            ValueError: Si los parámetros son inválidos
            FileNotFoundError: Si el archivo no existe
            PermissionError: Si no hay permisos de lectura
            OSError: Si hay error al leer el archivo
        """
        # Validar archivo
        full_path = self.validate_file_path(file_path, file_name)

        try:
            # Cargar documento
            self.md_document.load_doc(file_path, file_name)
            Logger.info(f"ProjectManager: Archivo abierto: {full_path}")

            return True

        except Exception as e:
            Logger.error(f"ProjectManager: Error al cargar archivo: {e}")
            raise OSError(f"Error al leer el archivo: {e}") from e

    def save_file(self) -> bool:
        """
        Guarda el archivo markdown actual.

        Returns:
            bool: True si el archivo se guardó exitosamente

        Raises:
            ValueError: Si no hay documento activo
            PermissionError: Si no hay permisos de escritura
            OSError: Si hay error al escribir el archivo
        """
        if not self.md_document.doc_name:
            raise ValueError("No hay documento activo para guardar")

        file_path = Path(self.md_document.doc_path) / self.md_document.doc_name

        # Verificar permisos de escritura
        if file_path.exists() and not os.access(file_path, os.W_OK):
            raise PermissionError(f"Sin permisos de escritura en: {file_path}")

        if not os.access(self.md_document.doc_path, os.W_OK):
            raise PermissionError(
                f"Sin permisos de escritura en directorio: {self.md_document.doc_path}"
            )

        try:
            # Unir líneas y guardar
            self.md_document.join_lines()
            self.md_document.save_doc()
            Logger.info(f"ProjectManager: Archivo guardado: {file_path}")

            return True

        except Exception as e:
            Logger.error(f"ProjectManager: Error al guardar archivo: {e}")
            raise OSError(f"Error al guardar el archivo: {e}") from e

    def create_file(self, parent_folder: str, file_name: str) -> bool:
        """
        Crea un nuevo archivo markdown.

        Args:
            parent_folder: Directorio donde crear el archivo
            file_name: Nombre del nuevo archivo

        Returns:
            bool: True si el archivo se creó exitosamente

        Raises:
            ValueError: Si los parámetros son inválidos
            FileExistsError: Si el archivo ya existe
            PermissionError: Si no hay permisos de escritura
            OSError: Si hay error al crear el archivo
        """
        if not parent_folder or not file_name:
            raise ValueError("El directorio y nombre del archivo son requeridos")

        if not self.is_markdown_file(file_name):
            raise ValueError(
                f"El archivo debe tener extensión markdown válida. "
                f"Extensiones permitidas: {', '.join(self.md_extensions)}"
            )

        full_path = Path(parent_folder) / file_name

        if full_path.exists():
            raise FileExistsError(f"El archivo ya existe: {full_path}")

        if not os.access(parent_folder, os.W_OK):
            raise PermissionError(
                f"Sin permisos de escritura en directorio: {parent_folder}"
            )

        try:
            # Crear archivo vacío
            full_path.touch()
            Logger.info(f"ProjectManager: Archivo creado: {full_path}")

            return True

        except Exception as e:
            Logger.error(f"ProjectManager: Error al crear archivo: {e}")
            raise OSError(f"Error al crear el archivo: {e}") from e

    def close_project(self):
        """
        Cierra el proyecto actual y limpia el documento.

        Side Effects:
            - Limpia active_project
            - Reinicia md_document
        """
        self.active_project = ''
        self.md_document = MDDocument()
        Logger.info("ProjectManager: Proyecto cerrado")
