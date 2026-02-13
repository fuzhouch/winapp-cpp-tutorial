@echo off
REM Wrapper script for winappCLI on Windows

set SCRIPT_DIR=%~dp0

REM Try 'py' launcher first (recommended for Windows), then fallback to python
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py "%SCRIPT_DIR%winappCLI.py" %*
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        python "%SCRIPT_DIR%winappCLI.py" %*
    ) else (
        echo Error: Python is not installed or not in PATH
        echo Please install Python from https://www.python.org/
        exit /b 1
    )
)
