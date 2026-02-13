# SampleApp

A Windows application created with winappCLI.

## Building the Project

### Prerequisites
- CMake (version 3.10 or higher)
- A C++ compiler that supports C++17 (e.g., MSVC, MinGW)
- Windows SDK

### Build Instructions

1. Create a build directory:
```bash
mkdir build
cd build
```

2. Generate build files:
```bash
cmake ..
```

3. Build the project:
```bash
cmake --build .
```

4. Run the application:
```bash
.\bin\Debug\SampleApp.exe
```

## Project Structure

```
SampleApp/
├── src/
│   └── main.cpp          # Main application source
├── include/              # Header files (if any)
├── build/                # Build directory (generated)
├── CMakeLists.txt        # CMake configuration
└── README.md            # This file
```

## Features

This is a basic Windows desktop application that:
- Creates a window with a title bar
- Displays a welcome message
- Handles basic Windows messages

## Next Steps

Extend this application by:
- Adding more UI elements (buttons, text boxes, menus)
- Implementing custom window procedures
- Adding application-specific functionality
