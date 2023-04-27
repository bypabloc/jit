#!/bin/bash

# Ruta del directorio desde donde se llama el script
path_caller=$(pwd)

# Ruta del script (relativa o absoluta, dependiendo de cómo se llamó)
path_script="$0"

# Ruta absoluta del directorio donde se encuentra el script
path_script_abs=$(dirname "$(realpath "$path_script")")

# Ruta relativa del comando al directorio desde donde se llama el script
path_script_rel=$(realpath --relative-to="$path_caller" "$path_script_abs")

function byte-me() {
    # Ejecuta el script de python pasándole los argumentos
    python3 "$path_script_abs/run.py" ${@:1}
}
