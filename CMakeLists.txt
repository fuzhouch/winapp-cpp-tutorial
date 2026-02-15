cmake_minimum_required(VERSION 3.20)

project(winapp-cpp-tutorial LANGUAGES CXX)

# Configure C++ Standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add component subdirectories
add_subdirectory(component/calculator)

# Define the executable
add_executable(${PROJECT_NAME} main.cpp)

# -----------------------------------------------------------------------------
# WinApp / Windows App SDK Setup
# -----------------------------------------------------------------------------

set(WINAPP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/.winapp")

if(NOT EXISTS "${WINAPP_ROOT}")
    message(WARNING "WinApp folder not found at ${WINAPP_ROOT}. Please run 'winapp init .'")
endif()

# Setup Include Paths
target_include_directories(${PROJECT_NAME} PRIVATE
    "${WINAPP_ROOT}/include"
)

# Setup Library Paths
# Detect architecture based on system processor
if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(x86|i386|i686|Win32)$" OR
   CMAKE_VS_PLATFORM_NAME STREQUAL "Win32" OR
   CMAKE_GENERATOR_PLATFORM STREQUAL "Win32")
    set(WINAPP_LIB_DIR "${WINAPP_ROOT}/lib/x86")
elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "^(ARM64|arm64|aarch64)$" OR
       CMAKE_VS_PLATFORM_NAME STREQUAL "ARM64" OR
       CMAKE_GENERATOR_PLATFORM STREQUAL "ARM64")
    set(WINAPP_LIB_DIR "${WINAPP_ROOT}/lib/arm64")
else()
    # Default to amd64 for x64/AMD64 and unknown architectures
    set(WINAPP_LIB_DIR "${WINAPP_ROOT}/lib/x64")
    if(NOT CMAKE_SYSTEM_PROCESSOR MATCHES "^(AMD64|amd64|x86_64|x64)$")
        message(STATUS "Unknown architecture ${CMAKE_SYSTEM_PROCESSOR}, defaulting to amd64")
    endif()
endif()

target_link_directories(${PROJECT_NAME} PRIVATE "${WINAPP_LIB_DIR}")

# MSVC Compiler Options for Modern Windows Apps / C++/WinRT
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE
        /std:c++20
        /permissive-
        /utf-8
        /EHsc
        /bigobj
    )

    # Optional: If you want to use precompiled headers for faster builds later
    # target_precompile_headers(${PROJECT_NAME} PRIVATE "${WINAPP_ROOT}/include/winrt/Windows.Foundation.h")
else()
    message(FATAL_ERROR "Non MSVC compiler is unsupported.")
endif()

# Link Libraries
target_link_libraries(${PROJECT_NAME} PRIVATE
    # Windows App SDK Bootstrap (for unpackaged apps or dynamic dependency)
    Microsoft.WindowsAppRuntime.Bootstrap
    Microsoft.WindowsAppRuntime

    # WinRT Components
    # AdderComponent

    # Standard Windows Libraries if needed
    kernel32
    user32
)

# Copy necessary DLLs or assets if needed (Placeholder)
# winapp pack will handle packaging, but for local debugging we might need things in place.
