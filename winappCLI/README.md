# winappCLI

A command-line interface tool for creating Windows C++ application projects.

## Overview

winappCLI is a simple scaffolding tool that helps you quickly set up a basic Windows desktop application project using C++ and CMake.

## Installation

No installation required! Just use the Python script directly.

### Prerequisites

- Python 3.6 or higher
- CMake 3.10 or higher
- A C++ compiler (MSVC, MinGW-w64, or similar)
- Windows SDK

## Usage

### Creating a New Project

```bash
python3 winappCLI.py create <project_name>
```

This will create a new directory with the project name containing:
- A basic Windows application source file (`src/main.cpp`)
- CMake build configuration (`CMakeLists.txt`)
- Project README with build instructions
- Proper directory structure

### Options

- `-o, --output <directory>`: Specify the output directory (default: current directory)

### Examples

Create a project in the current directory:
```bash
python3 winappCLI.py create MyWindowsApp
```

Create a project in a specific directory:
```bash
python3 winappCLI.py create MyWindowsApp -o ./projects
```

## What Gets Generated

When you run `winappCLI.py create MyApp`, the following structure is created:

```
MyApp/
├── src/
│   └── main.cpp          # Main Windows application source
├── include/              # Directory for header files
├── build/                # Directory for build artifacts
├── CMakeLists.txt        # CMake configuration file
└── README.md            # Project documentation
```

### Generated Application Features

The generated Windows application includes:
- A basic window with title bar
- Message loop for handling Windows events
- Window procedure for processing messages
- Welcome text displayed in the window
- Proper cleanup and resource management

## Building Generated Projects

After creating a project with winappCLI:

```bash
cd MyApp
mkdir build && cd build
cmake ..
cmake --build .
```

Run the application:
```bash
./bin/Debug/MyApp.exe
```

## Template Customization

The tool generates a basic Win32 application template that you can extend with:
- Additional UI controls (buttons, menus, text boxes)
- Custom drawing and graphics
- File I/O operations
- Network connectivity
- Database access
- And more...

## Requirements for Generated Projects

To build projects created by winappCLI, you need:
- **CMake**: Version 3.10 or higher
- **C++ Compiler**: Any modern C++ compiler with C++17 support
  - Visual Studio 2017 or later (MSVC)
  - MinGW-w64
  - Clang for Windows
- **Windows SDK**: For Win32 API headers and libraries

## License

This tool is part of the winapp-cpp-tutorial project.
