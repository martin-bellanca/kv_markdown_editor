#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kv_markdown_start.py
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
Created on 21/07/2025
@author: mpbe
'''

# system imports ------------------------------------------------------------
import sys
import kivy
from kivy.logger import Logger
from kivy.config import Config

print(sys.path)

import __init__ as kv_md_editor
from kv_markdown_editor.kv_markdown_editor_main_rv import KVMarkdownEditorApp

# --- INICIA CONFIGURACIÓN DE LOG ---
# 1. Activa el guardado en archivo
Config.set('kivy', 'log_enable', 1)

# 2. Define el nombre del archivo de log
Config.set('kivy', 'log_name', 'kv_md_editor_%Y-%m-%d_%H-%M-%S.log')

# 3. Define el directorio donde se guardará el log
# (en este caso, el mismo directorio que el script)
Config.set('kivy', 'log_dir', kv_md_editor.DIR_APP / 'kivy_logs') 

# # 4. Define el nivel máximo de log a guardar
# # (debug, info, warning, error, critical)
# Config.set('kivy', 'log_level', 'info')

# # 5. Define el formato del log
# Config.set('kivy', 'log_format', '[%(asctime)s] [%(levelname)s] %(message)s')

# # 6. Define el formato de fecha y hora
# Config.set('kivy', 'log_date_format', '%Y-%m-%d %H:%M:%S')
# # --- TERMINA CONFIGURACIÓN DE LOG ---

if __name__ == "__main__":
    print()
# # log the application start
    Logger.info("-"*80)
    Logger.info(f"Starting {kv_md_editor.__app_name__} version {kv_md_editor.__version__}")
    Logger.info(f"Python version {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")
    Logger.info(f"Kivy version {kivy.__version__}")
    # Logger.info("KV Markdown Editor version: " + kv_md_editor.__version__)
    Logger.info(f"Licencia {kv_md_editor.__license__}")
    Logger.info(f"Autor {kv_md_editor.__author__}")
    Logger.info("")
    Logger.info(f"DIR_WorkBench - {str(kv_md_editor.DIR_WKB)}")
    Logger.info(f"DIR_APP - {str(kv_md_editor.DIR_APP)}")
    Logger.info(f"KV_FILES - {str(kv_md_editor.DIR_KV_FILES)}")
    Logger.info(f"PATH_HOME - {str(kv_md_editor.DIR_HOME)}")
    Logger.info("-"*80)

    

    KVMarkdownEditorApp().run()
