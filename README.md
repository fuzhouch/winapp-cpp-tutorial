# Windows App C++ Tutorial with WinAppCLI

Learn how to develop modern Windows applications with C++ using Microsoft's **WinAppCLI** tool and CMake!

## Overview

This repository provides a comprehensive tutorial for creating Windows desktop applications using:
- **Microsoft WinAppCLI** - Official Windows app development CLI tool
- **C++ and CMake** - Modern C++ build system
- **Windows App SDK** - Modern Windows APIs

The WinAppCLI tool (from https://github.com/microsoft/WinAppCli) streamlines Windows app development by automating manifest creation, certificate management, SDK downloads, and project configuration—all from the command line, without requiring Visual Studio.

## What is WinAppCLI?

WinAppCLI is Microsoft's official command-line tool that simplifies Windows app development. It:
- **Bootstraps projects** with `winapp init` command
- **Manages manifests** (AppxManifest.xml) automatically
- **Handles certificates** for development signing
- **Downloads SDK packages** for your framework
- **Configures package identity** for debugging
- **Supports CMake** and various languages (C++, Rust, .NET, Electron, etc.)

## Prerequisites

Before you begin, ensure you have:

1. **Windows 10/11** - Required for Windows app development
2. **CMake** (3.10 or higher) - [Download](https://cmake.org/download/)
3. **C++ Compiler** - One of:
   - Visual Studio 2019/2022 with "Desktop development with C++" workload
   - Build Tools for Visual Studio
   - MinGW-w64 (for GCC)
4. **Windows SDK** - Typically installed with Visual Studio
5. **WinAppCLI** - Install using:
   ```bash
   winget install Microsoft.winappcli --source winget
   ```
   Or download from: https://github.com/microsoft/WinAppCli/releases

## Quick Start

### Step 1: Verify WinAppCLI Installation

```bash
winapp --version
```

### Step 2: Create a New C++ Project

Navigate to where you want to create your project:

```bash
mkdir MyWindowsApp
cd MyWindowsApp
```

### Step 3: Initialize with WinAppCLI

Run the initialization command:

```bash
winapp init
```

This command will:
- Prompt you for app configuration (name, publisher, version)
- Create an `AppxManifest.xml` file
- Download necessary SDK components
- Set up certificates for development signing
- Generate default assets and configuration

### Step 4: Create Your C++ Source Files

Create a basic project structure with your own source files and CMakeLists.txt.

### Step 5: Build with CMake

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

### Step 6: Run Your Application

```bash
./bin/Debug/MyWindowsApp.exe
```

Or use WinAppCLI to run with package identity:

```bash
winapp create-debug-identity MyWindowsApp.exe
```

## Key WinAppCLI Commands

### Initialize a Project
```bash
winapp init
```
Sets up a new Windows app project with manifest, certificates, and SDK components.

### Restore Environment
```bash
winapp restore
```
Reproduces the development environment on another machine using configuration files.

### Create Debug Identity
```bash
winapp create-debug-identity <yourapp.exe>
```
Injects package identity for debugging without full packaging.

## CMake Integration

WinAppCLI works seamlessly with CMake. A typical `CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyWindowsApp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add source files
file(GLOB SOURCES "src/*.cpp")

# Create executable
add_executable(${PROJECT_NAME} WIN32 ${SOURCES})

# Link Windows libraries
target_link_libraries(${PROJECT_NAME} PRIVATE 
    WindowsApp
    user32 
    gdi32
)
```

## Benefits of Using WinAppCLI

1. **No Visual Studio Required** - Build from command line
2. **Automated Setup** - No manual manifest editing
3. **Certificate Management** - Automatic dev certificate creation
4. **SDK Management** - Downloads only what you need
5. **CI/CD Friendly** - Perfect for automated builds
6. **Cross-Framework** - Works with C++, Rust, .NET, and more
7. **Package Identity** - Easy debugging with package APIs

## Additional Resources

- [WinAppCLI GitHub Repository](https://github.com/microsoft/WinAppCli)
- [Windows Developer Blog Announcement](https://blogs.windows.com/windowsdeveloper/2026/01/22/announcing-winapp-the-windows-app-development-cli/)
- [Windows App SDK Documentation](https://docs.microsoft.com/en-us/windows/apps/windows-app-sdk/)
- [CMake Documentation](https://cmake.org/documentation/)
- [C++ Windows Development](https://docs.microsoft.com/en-us/windows/dev-environment/cpp/)

## Contributing

Contributions are welcome! Feel free to:
- Add new example projects
- Improve documentation
- Share tips and best practices
- Report issues

## License

See [LICENSE](LICENSE) file for details.

---

**Note**: This tutorial focuses on using the official Microsoft WinAppCLI tool. For more information, visit the [official repository](https://github.com/microsoft/WinAppCli).
