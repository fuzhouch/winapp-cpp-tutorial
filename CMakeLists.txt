cmake_minimum_required(VERSION 3.20)

project(winapp-cpp-tutorial LANGUAGES CXX)

# Configure C++ Standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Define the executable
add_executable(winapp-cpp-tutorial main.cpp)

# -----------------------------------------------------------------------------
# WinApp / Windows App SDK Setup
# -----------------------------------------------------------------------------

set(WINAPP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/.winapp")

if(NOT EXISTS "${WINAPP_ROOT}")
    message(WARNING "WinApp folder not found at ${WINAPP_ROOT}. Please run 'winapp init .'")
endif()

# Setup Include Paths
target_include_directories(winapp-cpp-tutorial PRIVATE
    "${WINAPP_ROOT}/include"
)

# Setup Library Paths
# Detect architecture (defaulting to x64 for typical dev environments)
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(WINAPP_LIB_DIR "${WINAPP_ROOT}/lib/x64")
else()
    set(WINAPP_LIB_DIR "${WINAPP_ROOT}/lib/x86")
endif()

target_link_directories(winapp-cpp-tutorial PRIVATE
    "${WINAPP_LIB_DIR}"
)

# MSVC Compiler Options for Modern Windows Apps / C++/WinRT
if(MSVC)
    target_compile_options(winapp-cpp-tutorial PRIVATE
        /std:c++20
        /permissive-
        /utf-8
        /EHsc
        /bigobj
    )

    # Optional: If you want to use precompiled headers for faster builds later
    # target_precompile_headers(winapp-cpp-tutorial PRIVATE "${WINAPP_ROOT}/include/winrt/Windows.Foundation.h")
endif()

# Link Libraries
target_link_libraries(winapp-cpp-tutorial PRIVATE
    # Windows App SDK Bootstrap (for unpackaged apps or dynamic dependency)
    Microsoft.WindowsAppRuntime.Bootstrap
    Microsoft.WindowsAppRuntime

    # Standard Windows Libraries if needed
    kernel32
    user32
)

# Copy necessary DLLs or assets if needed (Placeholder)
# winapp pack will handle packaging, but for local debugging we might need things in place.
