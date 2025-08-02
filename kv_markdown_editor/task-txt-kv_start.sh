#!/bin/bash
# $PWD directorio actual
# $HOME directorio personal

export PYTHONPATH=$PYTHONPATH:$PWD/Helpers/helpers/src
export PYTHONPATH=$PYTHONPATH:$PWD/kv_widgets/src
#export PYTHONPATH=$PYTHONPATH:$PWD/mpbeWxWidgets/wxwidgets/src
#export PYTHONPATH=$PYTHONPATH:$PWD/CEH/estructura/src

echo "PYTHONPATH=" $PYTHONPATH

cd $PWD/TaskTxt/task-txt-kv/src
python task-txt-kv.py
