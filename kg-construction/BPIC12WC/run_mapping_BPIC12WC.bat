@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "RMLMAPPER_JAR=%~1"
if "%RMLMAPPER_JAR%"=="" set "RMLMAPPER_JAR=%SCRIPT_DIR%..\rmlmapper.jar"

yarrrml-parser -i "%SCRIPT_DIR%db_mapping_BPIC12_WC.yarrrml" -o "%SCRIPT_DIR%mapping.rml.ttl"
if errorlevel 1 exit /b 1

java -jar "%RMLMAPPER_JAR%" -m "%SCRIPT_DIR%mapping.rml.ttl" -o "%SCRIPT_DIR%BPIC12_WC.ttl" -s turtle
if errorlevel 1 exit /b 1

echo RDF generated: %SCRIPT_DIR%BPIC12_WC.ttl
