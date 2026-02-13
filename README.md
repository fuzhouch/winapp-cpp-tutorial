# winapp-cpp-tutorial

Learn how to develop Windows applications with C++ using the winappCLI tool!

## Overview

This repository provides a comprehensive tutorial and tooling for creating Windows desktop applications using C++. It includes **winappCLI**, a command-line scaffolding tool that helps you quickly bootstrap new Windows C++ projects with proper structure and build configuration.

## Quick Start

### Using winappCLI to Create a New Project

1. Navigate to the `winappCLI` directory:
```bash
cd winappCLI
```

2. Create a new Windows C++ project:
```bash
python3 winappCLI.py create MyFirstApp
```

3. Build and run your application:
```bash
cd MyFirstApp
mkdir build && cd build
cmake ..
cmake --build .
./bin/Debug/MyFirstApp.exe
```

## What's Included

### winappCLI Tool

A Python-based command-line tool that generates:
- Complete Windows C++ application structure
- CMake build configuration
- Basic Win32 window with message loop
- Project documentation

See the [winappCLI README](winappCLI/README.md) for detailed usage instructions.

### Generated Project Features

Projects created with winappCLI include:
- Win32 API-based window creation
- Event-driven message handling
- Clean project structure (src/, include/, build/)
- CMake-based build system
- Cross-compiler support (MSVC, MinGW, etc.)

## Prerequisites

To use winappCLI and build Windows applications:
- **Python 3.6+** (for running winappCLI)
- **CMake 3.10+** (for building projects)
- **C++ Compiler** with C++17 support (MSVC, MinGW-w64, Clang)
- **Windows SDK** (for Win32 API headers)

## Learning Path

1. **Start Here**: Use winappCLI to create your first project
2. **Explore the Code**: Examine the generated `main.cpp` to understand Win32 basics
3. **Modify and Extend**: Add buttons, menus, and other UI elements
4. **Build Something Cool**: Create your own Windows application!

## Repository Structure

```
winapp-cpp-tutorial/
├── winappCLI/           # CLI tool for project generation
│   ├── winappCLI.py    # Main CLI script
│   └── README.md       # Tool documentation
├── README.md           # This file
└── LICENSE             # License information
```

## Additional Resources

- [Win32 API Documentation](https://docs.microsoft.com/en-us/windows/win32/)
- [CMake Documentation](https://cmake.org/documentation/)
- [C++ Reference](https://en.cppreference.com/)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

See [LICENSE](LICENSE) file for details.
