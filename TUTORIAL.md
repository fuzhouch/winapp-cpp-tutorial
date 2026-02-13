# Step-by-Step Tutorial: Creating a Windows C++ App with WinAppCLI

This tutorial walks you through creating a complete Windows C++ application using Microsoft's WinAppCLI tool and CMake.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Project Initialization](#project-initialization)
3. [Creating the C++ Application](#creating-the-c-application)
4. [Building the Project](#building-the-project)
5. [Running and Debugging](#running-and-debugging)
6. [Advanced Features](#advanced-features)

## Environment Setup

### Install Required Tools

#### 1. Install WinAppCLI

Using winget (recommended):
```bash
winget install Microsoft.winappcli --source winget
```

Or download from GitHub releases:
https://github.com/microsoft/WinAppCli/releases

Verify installation:
```bash
winapp --version
```

#### 2. Install CMake

```bash
winget install Kitware.CMake
```

Or download from: https://cmake.org/download/

#### 3. Install C++ Build Tools

Option A: Visual Studio (recommended)
- Download Visual Studio Community 2022 (free)
- During installation, select "Desktop development with C++"
- This includes Windows SDK and MSVC compiler

Option B: Build Tools for Visual Studio
- Download from: https://visualstudio.microsoft.com/downloads/
- Select "Build Tools for Visual Studio"
- Install "C++ build tools" workload

## Project Initialization

### Step 1: Create Project Directory

```bash
mkdir HelloWindowsApp
cd HelloWindowsApp
```

### Step 2: Initialize with WinAppCLI

Run the initialization command:

```bash
winapp init
```

You'll be prompted for:
- **App Name**: Enter "HelloWindowsApp"
- **Publisher**: Enter your publisher name (e.g., "CN=YourName")
- **Version**: Keep default "1.0.0.0"
- **Target Framework**: Select "C++" or "Native C++"
- **Package Identity**: Confirm to create one

This creates:
- `AppxManifest.xml` - App package manifest
- `Assets/` directory - App icons and splash screens
- Development certificate for signing
- SDK package references

### Step 3: Verify Generated Files

```bash
ls -la
```

You should see:
```
HelloWindowsApp/
├── AppxManifest.xml
├── Assets/
│   ├── Square150x150Logo.png
│   ├── Square44x44Logo.png
│   ├── SplashScreen.png
│   └── ...
└── (certificate files)
```

## Creating the C++ Application

### Step 1: Create Source Directory

```bash
mkdir src
mkdir include
```

### Step 2: Create main.cpp

Create `src/main.cpp`:

```cpp
#include <windows.h>
#include <string>

// Window procedure
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
        
    case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            
            // Draw text
            const wchar_t* text = L"Hello from WinAppCLI!";
            TextOut(hdc, 10, 10, text, wcslen(text));
            
            EndPaint(hwnd, &ps);
        }
        return 0;
    }
    
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                    PWSTR pCmdLine, int nCmdShow)
{
    // Register window class
    const wchar_t CLASS_NAME[] = L"HelloWindowClass";
    
    WNDCLASS wc = { };
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    
    if (!RegisterClass(&wc))
    {
        MessageBox(NULL, L"Window Registration Failed!", L"Error", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }
    
    // Create window
    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        L"Hello Windows App",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL,
        NULL,
        hInstance,
        NULL
    );
    
    if (hwnd == NULL)
    {
        MessageBox(NULL, L"Window Creation Failed!", L"Error", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }
    
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);
    
    // Message loop
    MSG msg = { };
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    return (int)msg.wParam;
}
```

### Step 3: Create CMakeLists.txt

Create `CMakeLists.txt` in the project root:

```cmake
cmake_minimum_required(VERSION 3.10)
project(HelloWindowsApp)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Collect source files
file(GLOB SOURCES "src/*.cpp")
file(GLOB HEADERS "include/*.h")

# Create executable
add_executable(${PROJECT_NAME} WIN32 ${SOURCES} ${HEADERS})

# Link Windows libraries
target_link_libraries(${PROJECT_NAME} PRIVATE 
    user32 
    gdi32
)

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE include)

# Set output directory
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
```

### Step 4: Create Project README

Create `PROJECT_README.md`:

```markdown
# Hello Windows App

A simple Windows application created with WinAppCLI and CMake.

## Building

1. Generate build files:
   ```bash
   mkdir build && cd build
   cmake ..
   ```

2. Build the project:
   ```bash
   cmake --build .
   ```

3. Run the application:
   ```bash
   ./bin/Debug/HelloWindowsApp.exe
   ```

## Features

- Basic Windows window with title bar
- Custom window procedure
- Message loop for event handling
- Initialized with WinAppCLI for package identity
```

## Building the Project

### Step 1: Generate Build Files

Open "Developer Command Prompt for VS" or a regular terminal:

```bash
mkdir build
cd build
cmake ..
```

For MinGW:
```bash
cmake -G "MinGW Makefiles" ..
```

### Step 2: Build the Application

```bash
cmake --build .
```

Or specify configuration:
```bash
cmake --build . --config Release
```

### Step 3: Verify Build Output

```bash
ls bin/Debug/
```

You should see `HelloWindowsApp.exe`.

## Running and Debugging

### Option 1: Run Directly

```bash
./bin/Debug/HelloWindowsApp.exe
```

### Option 2: Run with Package Identity

Use WinAppCLI to inject package identity for debugging:

```bash
cd ..
winapp create-debug-identity build/bin/Debug/HelloWindowsApp.exe
```

This allows your app to:
- Use Windows APIs that require package identity
- Access system features requiring permissions
- Test packaging behavior

### Debugging Tips

1. **Check WinAppCLI logs**:
   ```bash
   winapp logs
   ```

2. **Verify certificate**:
   ```bash
   winapp certificate list
   ```

3. **Update manifest**:
   ```bash
   winapp manifest update
   ```

## Advanced Features

### Adding Windows App SDK

To use modern Windows APIs:

1. Update CMakeLists.txt:
   ```cmake
   find_package(WindowsAppSDK REQUIRED)
   target_link_libraries(${PROJECT_NAME} PRIVATE WindowsAppSDK::WindowsAppSDK)
   ```

2. Install SDK packages:
   ```bash
   winapp restore
   ```

### Using WinUI 3

For modern UI controls:

1. Initialize with WinUI support:
   ```bash
   winapp init --framework WinUI3
   ```

2. Add WinUI references to CMakeLists.txt

### Packaging for Distribution

1. Update manifest with your details:
   ```bash
   winapp manifest update
   ```

2. Build release version:
   ```bash
   cmake --build build --config Release
   ```

3. Create MSIX package:
   ```bash
   winapp package create
   ```

### CI/CD Integration

For GitHub Actions:

```yaml
- name: Install WinAppCLI
  run: winget install Microsoft.winappcli

- name: Restore environment
  run: winapp restore

- name: Build
  run: |
    cmake -B build
    cmake --build build
```

## Troubleshooting

### Problem: winapp command not found

**Solution**: Ensure WinAppCLI is installed and in PATH:
```bash
winget install Microsoft.winappcli --source winget
```
Restart your terminal after installation.

### Problem: Certificate errors

**Solution**: Regenerate certificate:
```bash
winapp certificate create --force
```

### Problem: CMake can't find Windows SDK

**Solution**: Install Windows SDK:
- Via Visual Studio Installer
- Or standalone: https://developer.microsoft.com/windows/downloads/windows-sdk/

### Problem: Build fails with "WindowsApp" not found

**Solution**: Make sure you have Windows App SDK installed:
```bash
winapp restore
```

## Next Steps

1. **Add UI Controls**: Buttons, text boxes, menus
2. **Implement Features**: File I/O, networking, databases
3. **Use Windows APIs**: Notifications, file pickers, etc.
4. **Package and Deploy**: Create MSIX package for distribution
5. **Publish to Store**: Submit to Microsoft Store

## Resources

- [WinAppCLI Documentation](https://github.com/microsoft/WinAppCli)
- [Windows App SDK](https://docs.microsoft.com/windows/apps/windows-app-sdk/)
- [CMake Documentation](https://cmake.org/documentation/)
- [Win32 API Reference](https://docs.microsoft.com/windows/win32/)

Happy coding!
