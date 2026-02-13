@echo off
REM Wrapper script for winappCLI on Windows

set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%winappCLI.py" %*
