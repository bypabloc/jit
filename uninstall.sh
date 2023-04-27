#!/bin/bash

set -e

RUNTIME_VERSION=3.8
VIRTUAL_ENV=.venv_tmp
BUILD_DIR=build

# Función para eliminar el entorno virtual de Python.
# Elimina el directorio que contiene el entorno virtual si existe.
function delete_venv() {
    if [ -d "$VIRTUAL_ENV" ]; then
        echo "Eliminando entorno virtual: $VIRTUAL_ENV"
        rm -rf $VIRTUAL_ENV
    else
        echo "Entorno virtual no encontrado: $VIRTUAL_ENV"
    fi
}

# Función para eliminar el directorio de compilación (BUILD_DIR).
# Elimina el directorio si existe.
function clean_package() {
    if [ -d "$BUILD_DIR" ]; then
        echo "Eliminando directorio de compilación: $BUILD_DIR"
        rm -rf ./$BUILD_DIR
    else
        echo "Directorio de compilación no encontrado: $BUILD_DIR"
    fi
}

# Función principal que ejecuta las funciones delete_venv() y clean_package().
function main() {
    delete_venv
    clean_package
}

main
