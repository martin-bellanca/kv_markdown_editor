#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  session_manager.py
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
Gestiona la persistencia de sesión de la aplicación.

Este módulo maneja la carga y guardado de la configuración de sesión,
incluyendo el tamaño y posición de la ventana, proyecto activo y archivo activo.
"""

import os
from pathlib import Path
from configparser import ConfigParser
from kivy.logger import Logger
from kivy.config import Config


class SessionManager:
    """
    Administra la persistencia de sesión de la aplicación.

    Responsable de guardar y cargar la configuración de sesión entre
    ejecuciones de la aplicación, incluyendo geometría de ventana,
    proyecto activo y último archivo abierto.
    """

    def __init__(self, config_file: str = 'config.ini'):
        """
        Inicializa el gestor de sesión.

        Args:
            config_file: Nombre del archivo de configuración (default: 'config.ini')
        """
        self.config_file = config_file
        self._config = ConfigParser()

    def load_session(self, config_dir: Path):
        """
        Carga la configuración de sesión desde archivo.

        Lee la posición y tamaño de la ventana, el proyecto activo
        y el archivo activo desde el archivo de configuración.

        Args:
            config_dir: Directorio donde se encuentra el archivo de configuración

        Returns:
            dict: Diccionario con la configuración cargada:
                {
                    'window': {'width': int, 'height': int, 'left': int, 'top': int},
                    'project': {'active_project': str, 'active_file': str}
                }

        Raises:
            FileNotFoundError: Si el archivo de configuración no existe
            PermissionError: Si no hay permisos para leer el archivo
            ValueError: Si el archivo de configuración está corrupto
        """
        file_path = config_dir / self.config_file

        if not file_path.exists():
            raise FileNotFoundError(
                f"Archivo de configuración '{self.config_file}' no encontrado en {config_dir}"
            )

        if not os.access(file_path, os.R_OK):
            raise PermissionError(
                f"Sin permisos de lectura para {file_path}"
            )

        Logger.info(f"SessionManager: Cargando sesión desde {file_path}")

        try:
            # Lee el archivo y carga los datos en el objeto Config de Kivy
            Config.read(str(file_path))

            # Extraer configuración de ventana
            window_config = {
                'width': Config.getint('Window', 'width', fallback=800),
                'height': Config.getint('Window', 'height', fallback=600),
                'left': Config.getint('Window', 'left', fallback=100),
                'top': Config.getint('Window', 'top', fallback=100)
            }

            # Validar dimensiones de ventana
            if window_config['width'] < 400 or window_config['height'] < 300:
                Logger.warning(
                    f"SessionManager: Dimensiones de ventana inválidas "
                    f"({window_config['width']}x{window_config['height']}), usando valores por defecto"
                )
                window_config['width'] = max(800, window_config['width'])
                window_config['height'] = max(600, window_config['height'])

            # Extraer configuración de proyecto
            project_config = {
                'active_project': Config.get('Project', 'active_project', fallback=None),
                'active_file': Config.get('Project', 'active_file', fallback=None)
            }

            Logger.info(
                f"SessionManager: Sesión cargada - "
                f"Ventana: {window_config['width']}x{window_config['height']}, "
                f"Proyecto: {project_config['active_project']}"
            )

            return {
                'window': window_config,
                'project': project_config
            }

        except Exception as e:
            raise ValueError(
                f"Error al parsear archivo de configuración: {e}"
            ) from e

    def save_session(self, config_dir: Path, window_config: dict, project_config: dict):
        """
        Guarda la configuración actual de sesión.

        Guarda la posición y tamaño de la ventana, el proyecto activo
        y el archivo activo en el archivo de configuración.

        Args:
            config_dir: Directorio donde guardar el archivo de configuración
            window_config: Diccionario con configuración de ventana:
                {'width': int, 'height': int, 'left': int, 'top': int}
            project_config: Diccionario con configuración de proyecto:
                {'active_project': str, 'active_file': str}

        Raises:
            PermissionError: Si no hay permisos para escribir el archivo
            ValueError: Si los parámetros de configuración son inválidos
            OSError: Si hay error al escribir el archivo
        """
        # Validar configuración de ventana
        required_window_keys = {'width', 'height', 'left', 'top'}
        if not all(key in window_config for key in required_window_keys):
            raise ValueError(
                f"Configuración de ventana incompleta. Se requieren: {required_window_keys}"
            )

        # Validar configuración de proyecto
        required_project_keys = {'active_project', 'active_file'}
        if not all(key in project_config for key in required_project_keys):
            raise ValueError(
                f"Configuración de proyecto incompleta. Se requieren: {required_project_keys}"
            )

        # Crear ConfigParser
        config = ConfigParser()

        # Sección Window
        config.add_section('Window')
        config.set('Window', 'width', str(window_config['width']))
        config.set('Window', 'height', str(window_config['height']))
        config.set('Window', 'left', str(window_config['left']))
        config.set('Window', 'top', str(window_config['top']))

        # Sección Project
        config.add_section('Project')
        config.set('Project', 'active_project', project_config['active_project'] or '')
        config.set('Project', 'active_file', project_config['active_file'] or '')

        # Guardar archivo
        file_path = config_dir / self.config_file

        # Verificar permisos del directorio
        if not os.access(config_dir, os.W_OK):
            raise PermissionError(
                f"Sin permisos de escritura en directorio {config_dir}"
            )

        try:
            with open(file_path, 'w') as f:
                config.write(f)

            Logger.info(f"SessionManager: Configuración guardada en {file_path}")

        except OSError as e:
            raise OSError(
                f"Error al escribir archivo de configuración: {e}"
            ) from e
