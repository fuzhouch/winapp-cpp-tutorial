# Windows API Tutorial

This tutorial explains the key concepts and code patterns used in Windows applications created with winappCLI.

## Table of Contents

1. [Win32 API Overview](#win32-api-overview)
2. [Application Entry Point](#application-entry-point)
3. [Window Classes](#window-classes)
4. [Creating a Window](#creating-a-window)
5. [Message Loop](#message-loop)
6. [Window Procedure](#window-procedure)
7. [Common Messages](#common-messages)
8. [Next Steps](#next-steps)

## Win32 API Overview

The Win32 API is the core set of Windows APIs for creating desktop applications. It provides:
- Window management
- Message handling
- Graphics and drawing
- User input processing
- File and system operations

All Windows applications, regardless of which framework they use, ultimately rely on Win32 APIs.

## Application Entry Point

### wWinMain Function

```cpp
int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, 
                    PWSTR pCmdLine, int nCmdShow)
```

This is the entry point for Windows GUI applications:
- **hInstance**: Handle to the current instance of the application
- **hPrevInstance**: Always NULL (legacy parameter)
- **pCmdLine**: Command-line arguments as a Unicode string
- **nCmdShow**: How the window should be displayed (maximized, minimized, etc.)

### Why wWinMain instead of main?

- `wWinMain` is for GUI applications (no console window)
- The 'w' prefix indicates Unicode support
- Console applications use `wmain` or `main`

## Window Classes

Before creating a window, you must register a window class:

```cpp
WNDCLASS wc = { };
wc.lpfnWndProc   = WindowProc;      // Window procedure function
wc.hInstance     = hInstance;        // Application instance
wc.lpszClassName = CLASS_NAME;       // Class name
wc.hCursor       = LoadCursor(NULL, IDC_ARROW);  // Cursor
wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);   // Background color

RegisterClass(&wc);
```

### Key WNDCLASS Members:
- **lpfnWndProc**: Pointer to the window procedure that handles messages
- **hInstance**: Application instance handle
- **lpszClassName**: Unique name for this window class
- **hCursor**: Default cursor for the window
- **hbrBackground**: Background color brush

## Creating a Window

```cpp
HWND hwnd = CreateWindowEx(
    0,                          // Extended window style
    CLASS_NAME,                 // Window class name
    L"My App",                  // Window title
    WS_OVERLAPPEDWINDOW,        // Window style
    CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,  // Position and size
    NULL,                       // Parent window
    NULL,                       // Menu
    hInstance,                  // Instance handle
    NULL                        // Additional data
);
```

### Window Styles:
- **WS_OVERLAPPEDWINDOW**: Standard window with title bar, borders, and buttons
- **WS_POPUP**: Window with no border or title bar
- **WS_CHILD**: Child window (must have parent)

### Displaying the Window:

```cpp
ShowWindow(hwnd, nCmdShow);  // Make window visible
UpdateWindow(hwnd);          // Send WM_PAINT message
```

## Message Loop

The message loop is the heart of every Windows application:

```cpp
MSG msg = { };
while (GetMessage(&msg, NULL, 0, 0))
{
    TranslateMessage(&msg);  // Translate virtual-key messages
    DispatchMessage(&msg);   // Send message to window procedure
}
```

### How It Works:
1. **GetMessage**: Retrieves a message from the message queue
2. **TranslateMessage**: Converts keyboard input to character messages
3. **DispatchMessage**: Sends the message to the window procedure
4. Returns when GetMessage receives WM_QUIT

## Window Procedure

The window procedure processes all messages sent to the window:

```cpp
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, 
                            WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
        
    case WM_PAINT:
        // Handle painting
        return 0;
    }
    
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}
```

### Parameters:
- **hwnd**: Handle to the window
- **uMsg**: Message identifier (WM_PAINT, WM_DESTROY, etc.)
- **wParam**: Additional message data (varies by message)
- **lParam**: Additional message data (varies by message)

### Important:
Always call `DefWindowProc` for messages you don't handle!

## Common Messages

### WM_DESTROY
Sent when a window is being destroyed:
```cpp
case WM_DESTROY:
    PostQuitMessage(0);  // Exit the message loop
    return 0;
```

### WM_PAINT
Sent when the window needs to be redrawn:
```cpp
case WM_PAINT:
{
    PAINTSTRUCT ps;
    HDC hdc = BeginPaint(hwnd, &ps);
    
    // Drawing code here
    TextOut(hdc, 10, 10, L"Hello!", 6);
    
    EndPaint(hwnd, &ps);
    return 0;
}
```

### WM_SIZE
Sent when window size changes:
```cpp
case WM_SIZE:
{
    int width = LOWORD(lParam);
    int height = HIWORD(lParam);
    // Adjust layout based on new size
    return 0;
}
```

### WM_COMMAND
Sent when user interacts with menus or buttons:
```cpp
case WM_COMMAND:
{
    int wmId = LOWORD(wParam);
    switch (wmId)
    {
    case IDM_EXIT:
        DestroyWindow(hwnd);
        break;
    }
    return 0;
}
```

### WM_LBUTTONDOWN
Sent when left mouse button is pressed:
```cpp
case WM_LBUTTONDOWN:
{
    int x = LOWORD(lParam);
    int y = HIWORD(lParam);
    // Handle mouse click at (x, y)
    return 0;
}
```

### WM_KEYDOWN
Sent when a key is pressed:
```cpp
case WM_KEYDOWN:
{
    switch (wParam)
    {
    case VK_ESCAPE:
        PostQuitMessage(0);
        break;
    }
    return 0;
}
```

## Drawing and Graphics

### Device Context (HDC)
A device context is a handle that allows you to draw:

```cpp
HDC hdc = BeginPaint(hwnd, &ps);

// Drawing functions
TextOut(hdc, x, y, text, length);
Rectangle(hdc, left, top, right, bottom);
Ellipse(hdc, left, top, right, bottom);
LineTo(hdc, x, y);

EndPaint(hwnd, &ps);
```

### Colors and Brushes
```cpp
// Create colored brush
HBRUSH hBrush = CreateSolidBrush(RGB(255, 0, 0));  // Red
SelectObject(hdc, hBrush);

// Draw filled rectangle with brush
Rectangle(hdc, 10, 10, 100, 100);

DeleteObject(hBrush);
```

## Common Patterns

### Creating Controls (Buttons, Edit boxes, etc.)

```cpp
case WM_CREATE:
{
    // Create a button
    CreateWindow(
        L"BUTTON",              // Control class
        L"Click Me",            // Text
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
        10, 10, 100, 30,        // Position and size
        hwnd,                   // Parent
        (HMENU)ID_BUTTON,       // Control ID
        (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE),
        NULL);
    return 0;
}
```

### Message Boxes

```cpp
int result = MessageBox(
    hwnd,                       // Parent window
    L"Do you want to quit?",    // Message
    L"Confirmation",            // Title
    MB_YESNO | MB_ICONQUESTION  // Buttons and icon
);

if (result == IDYES)
{
    // User clicked Yes
}
```

### Timers

```cpp
// Set a timer (ID 1, 1000ms interval)
SetTimer(hwnd, 1, 1000, NULL);

// Handle timer messages
case WM_TIMER:
{
    if (wParam == 1)
    {
        // Timer fired
    }
    return 0;
}

// Kill timer when done
KillTimer(hwnd, 1);
```

## Best Practices

1. **Always call DefWindowProc** for unhandled messages
2. **Release resources**: Delete brushes, pens, fonts when done
3. **Use Unicode**: Prefer wide strings (L"text") and Unicode APIs
4. **Check return values**: Many Win32 functions return NULL/FALSE on error
5. **Handle WM_DESTROY**: Always call PostQuitMessage(0)
6. **Validate window handles**: Check if CreateWindowEx returned NULL

## Error Handling

```cpp
HWND hwnd = CreateWindowEx(...);
if (hwnd == NULL)
{
    DWORD error = GetLastError();
    // Handle error
    return 1;
}
```

## Next Steps

1. **Add controls**: Buttons, text boxes, list boxes
2. **Create menus**: LoadMenu, SetMenu
3. **Handle dialogs**: DialogBox, CreateDialog
4. **Add icons**: LoadIcon, SetClassLong
5. **Use resources**: RC files for icons, menus, dialogs
6. **Advanced graphics**: GDI+, Direct2D
7. **Multithreading**: CreateThread, synchronization

## Resources

- [Microsoft Win32 Documentation](https://docs.microsoft.com/en-us/windows/win32/)
- [Windows API Index](https://docs.microsoft.com/en-us/windows/win32/apiindex/windows-api-list)
- [Programming Windows by Charles Petzold](http://www.charlespetzold.com/pw5/) (classic book)
- [Win32 Programming Tutorial](https://www.winprog.org/tutorial/)

## Example Projects to Build

Start simple and gradually increase complexity:

1. **Hello World**: Display text in a window ✓ (already done!)
2. **Calculator**: Simple arithmetic with buttons
3. **Notepad Clone**: Text editor with file operations
4. **Drawing Program**: Paint-like application
5. **Game**: Simple 2D game using Win32 and GDI

Happy Windows programming!
