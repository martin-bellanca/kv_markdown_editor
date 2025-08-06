#!/bin/bash
# $PWD directorio actual
# $HOME directorio personal

export PYTHONPATH=$PYTHONPATH:$PWD
# export PYTHONPATH=$PYTHONPATH:$PWD/Helpers/helpers/src
# export PYTHONPATH=$PYTHONPATH:$PWD/kv_widgets/src
#export PYTHONPATH=$PYTHONPATH:$PWD/mpbeWxWidgets/wxwidgets/src
#export PYTHONPATH=$PYTHONPATH:$PWD/CEH/estructura/src

echo "PYTHONPATH=" $PYTHONPATH

# $PWD es el directorio actual
cd $PWD/kv_markdown_editor
python kv_markdown_start.py
