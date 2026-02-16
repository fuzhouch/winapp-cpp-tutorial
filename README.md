# winapp-cpp-tutorial
Learn how to develop Windows app with winappCLI and vibe coding!

## How to build

### Install Prerequisites

1. Install Visual Studio 2022 Community Edition:
   ```powershell
   winget install Microsoft.VisualStudio.2022.Community
   ```

2. Install WinApp CLI:
   ```powershell
   winget install Microsoft.winappcli --source winget
   ```

### Build the Project

1. Initialize dependencies and generate development certificate:
   ```powershell
   winapp init . --no-prompt
   ```
   > **Note**: The `winapp init` command is required to generate the `devcert.pfx` file, which is used for signing the package during development. This certificate contains a private key and should **not** be checked into version control (it is added to `.gitignore` automatically).

2. Build with CMake:
   ```powershell
   cmake -S . -B build
   cmake --build build
   ```

## Configure App Package

### Package Layout

After building the project, the output directory (`build/bin`) contains the following structure, which adheres to the required package layout for Windows apps:

```text
build/bin/
├── winapp-cpp-tutorial.exe   # Main executable
├── Calculator.dll            # WinRT Component
├── Calculator.winmd          # Windows Metadata for the component
├── AppxManifest.xml          # Package manifest (copied from appxmanifest.xml)
└── Assets/                   # Image assets
```

### Registration-Free WinRT Activation

To allow the executable to load the custom WinRT component (`Calculator.dll`) without installing it via MSIX (Side-loading), we use a **Side-by-Side Manifest** (`app.manifest`).

*   **`app.manifest`**: This file contains a `<file>` element with an `<activatableClass>` tag. It tells the OS that `WinAppTutorial.Calculator` is implemented in `Calculator.dll`.
*   **Compilation**: CMake is configured to embed `app.manifest` into `winapp-cpp-tutorial.exe` as a resource (RT_MANIFEST). This means you do not need to distribute `app.manifest` separately; it is part of the binary.

### MSIX Packaging (`appxmanifest.xml`)

The `appxmanifest.xml` file is used when packaging the app as an MSIX bundle.

*   **In-Process Server Limitation**: Standard `appxmanifest.xml` validation for Packaged Classic Apps (`runFullTrust`) often rejects `windows.activatableClass.inProcessServer` extensions.
*   **Solution**: By using the embedded `app.manifest` (Reg-Free WinRT), the application handles component activation internally, bypassing the need to declare the ActivatableClass in `appxmanifest.xml` for the desktop bridge scenario.
