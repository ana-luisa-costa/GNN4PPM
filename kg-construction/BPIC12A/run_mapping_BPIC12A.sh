#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RMLMAPPER_JAR="${1:-$SCRIPT_DIR/../rmlmapper.jar}"

yarrrml-parser \
  -i "$SCRIPT_DIR/db_mapping_BPIC12_Application.yarrrml" \
  -o "$SCRIPT_DIR/mapping.rml.ttl"

java -jar "$RMLMAPPER_JAR" \
  -m "$SCRIPT_DIR/mapping.rml.ttl" \
  -o "$SCRIPT_DIR/BPIC12_A.ttl" \
  -s turtle

echo "RDF generated: $SCRIPT_DIR/BPIC12_A.ttl"