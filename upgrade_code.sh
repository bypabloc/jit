#!/bin/bash

set -e

BUILD_DIR=build

# Función para copiar los archivos del proyecto al directorio de compilación.
function copy_python() {
    cp -a ./src/. ./$BUILD_DIR
}

# Función principal para ejecutar todas las funciones necesarias en orden.
function upgrade() {
    copy_python
}

function main() {
    upgrade
}

main
