# -*- coding: utf-8 -*-
#
#  kv_markdown_editor_prj
#
#  Copyright 2018 Martin Pablo Bellanca <mbellanca@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
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
Base Package of KV Markdown Editor \n
Created on 01/10/2024

@author: mpbe
@note:
'''


# imports -------------------------------------------------------------------
import os
import sys
from pathlib import Path

# Configura los directorios de trabajo ---------------------------------------
try:
    DIR_APP = Path(__file__).resolve().parent
except NameError:
    DIR_APP = Path(sys.argv[0]).resolve().parent
if not hasattr(sys, 'WORK_DIR'):
    sys.WORK_DIR = DIR_APP

# Agrega los path de la aplicacion
DIR_PRJ = DIR_APP.parent  # Directorio del Proyecto (Ex DIRBASE)
DIR_WKB = DIR_PRJ.parent  # Directorio Workbench. Area de Trabajo

DIR_IMAGES = DIR_APP / 'rsrc_images'  # os.path.join(DIR_APP, 'rsrc_images/') 
DIR_KV_FILES = DIR_APP / 'kv_files'  # os.path.join(DIR_APP, 'kv_files/')

# Lista de directorios a agregar a sys.path
paths_to_add = [
    DIR_WKB / 'kv_markdown_editor_prj',
    DIR_WKB / 'helpers_mpbe_prj',
    DIR_WKB / 'kivy_mpe_widgets_prj',
]

# # Itera y agrega las rutas a sys.path solo si no existen
# print(sys.path)
# for path in paths_to_add:
#     path_str = str(path)
#     if path_str not in sys.path:
#         sys.path.insert(0, path_str) # insert(0,...) da prioridad
# print(sys.path)

# Directorio Home del Usuario
try:
    STR_DIR_HOME = os.environ['HOME']
except KeyError:
    STR_DIR_HOME = os.environ['HOMEPATH']
DIR_HOME = Path(STR_DIR_HOME)

# Constantes del Modulo -----------------------------------------------------
__app_name__ = 'KV Markdown Editor'
__author__ = 'Martin Pablo Bellanca'
__contact__ = 'mpbellanca@gmail.com'
__organization__ = 'mpbe'
__license__ = "GPL3"
__version_info__ = (0, 0, 1)
__version__ = 'alfa_0.0.1-2024-09-30'
INFO_DESCRIPCION = """
  KV Markdown Editor es un software para edicion de textos en formato markdown.
  Es software libre y se encuentra licenciado bajo los 
términos de la Licencia Pública General de GNU versión 3 
según se encuentra publicada por la Free Software Foundation.
"""
INFO_LICENSE = """
  Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los términos de la 
Licencia Pública General de GNU según se encuentra publicada por la Free Software Foundation, 
bien de la versión 3 de dicha Licencia o bien (según su elección) de cualquier versión posterior.
  Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA, 
incluso sin la garantía MERCANTIL implícita o sin garantizar la ADECUACIÓN A UN PROPÓSITO PARTICULAR. 
Véase la Licencia Pública General de GNU para más detalles.
  Debería haber recibido una copia de la Licencia Pública General junto con este programa. 
Si no ha sido así, escriba a la Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

http://www.fsf.org/
http://www.gnu.org/home.es.html
http://es.wikipedia.org/wiki/GNU
"""




