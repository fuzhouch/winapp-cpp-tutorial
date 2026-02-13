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
