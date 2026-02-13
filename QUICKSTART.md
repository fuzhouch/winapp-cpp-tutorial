# Quick Start Guide

This guide will walk you through creating your first Windows C++ application using winappCLI.

## Step 1: Prerequisites

Before you begin, ensure you have the following installed:

### For Running winappCLI
- Python 3.6 or higher

### For Building Windows Applications
- **CMake** (version 3.10 or higher)
  - Download from: https://cmake.org/download/
  
- **C++ Compiler** (choose one):
  - **Visual Studio** (Recommended for Windows)
    - Download Visual Studio Community (free) from: https://visualstudio.microsoft.com/
    - During installation, select "Desktop development with C++"
  
  - **MinGW-w64** (Alternative compiler)
    - Download from: https://sourceforge.net/projects/mingw-w64/
  
- **Windows SDK**
  - Included with Visual Studio
  - Or download separately from: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/

## Step 2: Create Your First Project

1. Open a command prompt or terminal

2. Navigate to where you want to create your project:
```bash
cd C:\Users\YourName\Projects
```

3. Run winappCLI to create a new project:
```bash
python path\to\winappCLI\winappCLI.py create MyFirstApp
```

This creates a complete Windows application structure:
```
MyFirstApp/
├── src/
│   └── main.cpp          # Your application code
├── include/              # For header files
├── CMakeLists.txt        # Build configuration
└── README.md            # Project documentation
```

## Step 3: Build Your Application

### Using Visual Studio Developer Command Prompt

1. Open "Developer Command Prompt for VS" (search in Start menu)

2. Navigate to your project:
```bash
cd MyFirstApp
```

3. Create and enter build directory:
```bash
mkdir build
cd build
```

4. Generate build files:
```bash
cmake ..
```

5. Build the project:
```bash
cmake --build .
```

### Using Regular Command Prompt with MinGW

1. Make sure MinGW is in your PATH

2. Navigate to your project and build:
```bash
cd MyFirstApp
mkdir build
cd build
cmake -G "MinGW Makefiles" ..
cmake --build .
```

## Step 4: Run Your Application

After building, your executable will be in the `build/bin/Debug` directory:

```bash
# From the build directory
.\bin\Debug\MyFirstApp.exe
```

You should see a window open with the title "MyFirstApp" and a welcome message!

## Step 5: Customize Your Application

Now you can edit `src/main.cpp` to add your own functionality:

- Add buttons, text boxes, and other controls
- Handle mouse and keyboard input
- Draw custom graphics
- Add menus and dialog boxes
- And much more!

### Example: Adding a Button

Here's a simple modification to add a button (replace the WM_PAINT section):

```cpp
case WM_CREATE:
{
    CreateWindow(
        L"BUTTON",                  // Predefined class
        L"Click Me!",               // Button text
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,  // Styles
        10, 40,                     // x, y position
        100, 30,                    // width, height
        hwnd,                       // Parent window
        (HMENU) 1,                  // Button ID
        (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE),
        NULL);
    return 0;
}

case WM_COMMAND:
{
    if (LOWORD(wParam) == 1) // Button ID
    {
        MessageBox(hwnd, L"Button clicked!", L"Message", MB_OK);
    }
    return 0;
}
```

After making changes, rebuild:
```bash
cd build
cmake --build .
```

## Troubleshooting

### CMake not found
- Make sure CMake is installed and added to your system PATH
- Restart your terminal after installation

### Compiler not found
- For Visual Studio: Use "Developer Command Prompt for VS"
- For MinGW: Make sure MinGW bin directory is in PATH

### Windows.h not found
- Install Windows SDK (included with Visual Studio)
- Or install Windows SDK separately

### Build errors
- Make sure you're using a C++17 compatible compiler
- Check that all prerequisites are properly installed
- Try cleaning the build directory: `rm -rf build` and rebuild

## Next Steps

- Read the [Win32 API Documentation](https://docs.microsoft.com/en-us/windows/win32/)
- Explore example projects online
- Join Windows development communities
- Build something awesome!

## Getting Help

If you encounter issues:
1. Check the project README for detailed information
2. Review the generated project's README.md
3. Search for error messages online
4. Ask in Windows development forums

Happy coding!
