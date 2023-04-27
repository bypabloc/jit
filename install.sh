#!/bin/bash

set -e

RUNTIME_VERSION=3.8
VIRTUAL_ENV=.venv_tmp
REQUIREMENTS=requirements
BUILD_DIR=build

PATH_SCRIPT="$0"
PATH_SCRIPT_ABS=$(dirname "$(realpath "$PATH_SCRIPT")")

# Función para validar si un directorio existe y tiene permisos de lectura.
# Si no cumple con estas condiciones, el script termina con un mensaje de error.
function validate_dir() {
    if [ ! -d "$1" ]; then
        echo "El directorio '$1' no existe"
        exit 1
    fi

    if [ ! -r "$1" ]; then
        echo "El directorio '$1' no tiene permisos de lectura"
        exit 1
    fi
}

# Función para crear un entorno virtual de Python.
function create_virtual_env() {
    python"$RUNTIME_VERSION" -m venv $VIRTUAL_ENV
}

# Función para instalar los paquetes necesarios desde el archivo de requisitos.
function install_requirements() {
    "$VIRTUAL_ENV/bin/pip" --no-cache-dir install -Ur $REQUIREMENTS
}

# Función para eliminar el contenido del directorio de compilación (BUILD_DIR).
function clean_package() {
    rm -rf ./$BUILD_DIR/*
}

# Función para copiar los archivos del proyecto al directorio de compilación.
function build_package() {
    mkdir -p ./$BUILD_DIR
    cp -a ./src/. ./$BUILD_DIR
}

# Función para ejecutar la creación del entorno virtual e instalar los paquetes.
function install() {
    create_virtual_env
    install_requirements
}

# Función para copiar los paquetes de Python del entorno virtual al directorio de compilación.
function copy_python() {
    validate_dir "$PATH_SCRIPT_ABS/$VIRTUAL_ENV/lib"
    cp -a $PATH_SCRIPT_ABS/$VIRTUAL_ENV/lib/python$RUNTIME_VERSION/site-packages/. $PATH_SCRIPT_ABS/$BUILD_DIR

    validate_dir "$PATH_SCRIPT_ABS/$VIRTUAL_ENV/lib64"
    cp -a $PATH_SCRIPT_ABS/$VIRTUAL_ENV/lib64/python$RUNTIME_VERSION/site-packages/. $BUILD_DIR
}

# Función para eliminar archivos y directorios innecesarios del directorio de compilación y el entorno virtual.
function remove_unused() {
    local dirs=(
        wheel*
        easy-install*
        easy_install*
        setuptools*
        pip*
        pkg_resources*
        __pycache__
        *.dist-info
        *.egg-info
    )

    for dir in "${dirs[@]}"; do
        rm -rf $BUILD_DIR/$dir
    done

    rm -rf $VIRTUAL_ENV
}

# Función principal para ejecutar todas las funciones necesarias en orden.
function build() {
    install
    clean_package
    build_package
    copy_python
    remove_unused
}

function main() {
    build
}

main
