#!/usr/bin/env python3
"""
winappCLI - A command-line tool to initialize Windows C++ application projects.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path


class WinAppCLI:
    """Main CLI class for creating Windows C++ applications."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.templates_dir = self.script_dir / "templates"
    
    def create_project(self, project_name, output_dir="."):
        """
        Create a new Windows C++ application project.
        
        Args:
            project_name: Name of the project to create
            output_dir: Directory where the project will be created
        """
        output_path = Path(output_dir) / project_name
        
        if output_path.exists():
            print(f"Error: Directory '{output_path}' already exists!")
            return False
        
        print(f"Creating Windows C++ project: {project_name}")
        
        # Create project directory structure
        directories = [
            output_path,
            output_path / "src",
            output_path / "include",
            output_path / "build",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  Created directory: {directory.relative_to(Path(output_dir))}")
        
        # Copy template files
        self._copy_template_files(project_name, output_path)
        
        print(f"\n✓ Project '{project_name}' created successfully!")
        print(f"\nNext steps:")
        print(f"  cd {project_name}")
        print(f"  mkdir build && cd build")
        print(f"  cmake ..")
        print(f"  cmake --build .")
        
        return True
    
    def _copy_template_files(self, project_name, output_path):
        """Copy template files to the project directory."""
        
        # Main application source file
        main_cpp = output_path / "src" / "main.cpp"
        self._create_main_cpp(main_cpp, project_name)
        print(f"  Created file: src/main.cpp")
        
        # CMakeLists.txt
        cmake_file = output_path / "CMakeLists.txt"
        self._create_cmake_file(cmake_file, project_name)
        print(f"  Created file: CMakeLists.txt")
        
        # README.md
        readme_file = output_path / "README.md"
        self._create_readme(readme_file, project_name)
        print(f"  Created file: README.md")
    
    def _create_main_cpp(self, filepath, project_name):
        """Create the main.cpp file with Windows application template."""
        content = f"""#include <windows.h>
#include <string>

// Global variables
const wchar_t CLASS_NAME[] = L"{project_name}WindowClass";

// Forward declarations
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, 
                    PWSTR pCmdLine, int nCmdShow)
{{
    // Register the window class
    WNDCLASS wc = {{ }};
    
    wc.lpfnWndProc   = WindowProc;
    wc.hInstance     = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    
    RegisterClass(&wc);
    
    // Create the window
    HWND hwnd = CreateWindowEx(
        0,                              // Optional window styles
        CLASS_NAME,                     // Window class
        L"{project_name}",              // Window text
        WS_OVERLAPPEDWINDOW,            // Window style
        
        // Size and position
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        
        NULL,       // Parent window
        NULL,       // Menu
        hInstance,  // Instance handle
        NULL        // Additional application data
    );
    
    if (hwnd == NULL)
    {{
        return 0;
    }}
    
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);
    
    // Run the message loop
    MSG msg = {{ }};
    while (GetMessage(&msg, NULL, 0, 0))
    {{
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }}
    
    return (int)msg.wParam;
}}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{{
    switch (uMsg)
    {{
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
        
    case WM_PAINT:
        {{
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            
            // Fill the window with a solid color
            FillRect(hdc, &ps.rcPaint, (HBRUSH)(COLOR_WINDOW + 1));
            
            // Display welcome text
            const wchar_t* text = L"Welcome to {project_name}!";
            TextOut(hdc, 10, 10, text, wcslen(text));
            
            EndPaint(hwnd, &ps);
        }}
        return 0;
    }}
    
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_cmake_file(self, filepath, project_name):
        """Create the CMakeLists.txt file."""
        content = f"""cmake_minimum_required(VERSION 3.10)
project({project_name})

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add source files
file(GLOB SOURCES "src/*.cpp")

# Create executable
add_executable(${{PROJECT_NAME}} WIN32 ${{SOURCES}})

# Link Windows libraries
target_link_libraries(${{PROJECT_NAME}} PRIVATE user32 gdi32)

# Set output directory
set_target_properties(${{PROJECT_NAME}} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${{CMAKE_BINARY_DIR}}/bin"
)
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_readme(self, filepath, project_name):
        """Create the README.md file."""
        content = f"""# {project_name}

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
.\\bin\\Debug\\{project_name}.exe
```

## Project Structure

```
{project_name}/
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
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='winappCLI - Create Windows C++ application projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  winappCLI.py create MyApp              # Create project in ./MyApp
  winappCLI.py create MyApp -o projects  # Create project in ./projects/MyApp
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new Windows C++ project')
    create_parser.add_argument('project_name', help='Name of the project to create')
    create_parser.add_argument('-o', '--output', default='.', 
                              help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    cli = WinAppCLI()
    
    if args.command == 'create':
        success = cli.create_project(args.project_name, args.output)
        return 0 if success else 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
