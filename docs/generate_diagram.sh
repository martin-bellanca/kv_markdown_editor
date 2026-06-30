#!/bin/bash

# Script para generar diagrama de clases desde PlantUML
# Requiere: Java instalado

PUML_FILE="md_document_editor_v2_class_diagram.puml"
PLANTUML_JAR="plantuml.jar"
PLANTUML_URL="https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar"

echo "======================================================================"
echo "Generador de Diagrama de Clases - MDDocumentEditor V2"
echo "======================================================================"
echo ""

# Verificar que existe el archivo .puml
if [ ! -f "$PUML_FILE" ]; then
    echo "❌ Error: No se encuentra el archivo $PUML_FILE"
    exit 1
fi

echo "✅ Archivo fuente encontrado: $PUML_FILE"
echo ""

# Verificar Java
if ! command -v java &> /dev/null; then
    echo "❌ Error: Java no está instalado"
    echo "   Instalar Java: sudo dnf install java-latest-openjdk"
    exit 1
fi

echo "✅ Java encontrado: $(java -version 2>&1 | head -n 1)"
echo ""

# Descargar PlantUML si no existe
if [ ! -f "$PLANTUML_JAR" ]; then
    echo "📥 Descargando PlantUML..."
    if command -v wget &> /dev/null; then
        wget -O "$PLANTUML_JAR" "$PLANTUML_URL"
    elif command -v curl &> /dev/null; then
        curl -L -o "$PLANTUML_JAR" "$PLANTUML_URL"
    else
        echo "❌ Error: No se encontró wget ni curl para descargar PlantUML"
        echo "   Descarga manualmente desde: $PLANTUML_URL"
        exit 1
    fi
fi

echo "✅ PlantUML disponible: $PLANTUML_JAR"
echo ""

# Generar diagrama
echo "🎨 Generando diagrama..."
java -jar "$PLANTUML_JAR" -tpng "$PUML_FILE"

if [ $? -eq 0 ]; then
    OUTPUT_FILE="${PUML_FILE%.puml}.png"
    echo ""
    echo "======================================================================"
    echo "✅ Diagrama generado exitosamente!"
    echo "======================================================================"
    echo ""
    echo "📄 Archivo de salida: $OUTPUT_FILE"
    echo ""
    echo "Para ver el diagrama:"
    echo "  xdg-open $OUTPUT_FILE"
    echo ""
    echo "También generado:"
    echo "  - md_document_editor_v2_class_diagram.md (documentación completa)"
    echo ""
else
    echo ""
    echo "❌ Error al generar el diagrama"
    exit 1
fi
