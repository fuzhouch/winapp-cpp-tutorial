#!/bin/bash
# Wrapper script for winappCLI on Unix-like systems (Linux, macOS, WSL)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 "$SCRIPT_DIR/winappCLI.py" "$@"
