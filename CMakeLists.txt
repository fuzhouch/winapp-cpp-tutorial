cmake_minimum_required(VERSION 3.20)

project(winapp-cpp-tutorial LANGUAGES CXX)

# Set binary and PDB output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_PDB_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

# Add component subdirectories
add_subdirectory(component/calculator)

# -----------------------------------------------------------------------------
# WinApp / Windows App SDK Setup
# -----------------------------------------------------------------------------

set(WINAPP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/.winapp")

if(NOT EXISTS "${WINAPP_ROOT}")
    message(WARNING "WinApp folder not found at ${WINAPP_ROOT}. Please run 'winapp init .'")
endif()

# To consume Calculator component, let's generate
# projection from calculator.winmd.
# Setup winapp package paths
set(WINAPP_PACKAGES_ROOT "$ENV{UserProfile}/.winapp/packages")
set(CPPWINRT_VERSION "2.0.250303.1")
set(SDK_CPP_VERSION "10.0.26100.7705")
file(TO_NATIVE_PATH "${WINAPP_PACKAGES_ROOT}/Microsoft.Windows.SDK.CPP.${SDK_CPP_VERSION}/c/References/10.0.26100.0" WINRT_METADATA_DIR)
file(TO_NATIVE_PATH "${CMAKE_CURRENT_BINARY_DIR}/GeneratedFiles" GENERATED_FILES_DIR)
file(TO_NATIVE_PATH "${GENERATED_FILES_DIR}/winrt/WinAppTutorial.h" GENERATED_HEADER)
file(TO_NATIVE_PATH "${WINAPP_PACKAGES_ROOT}/Microsoft.Windows.CppWinRT.${CPPWINRT_VERSION}/bin/cppwinrt.exe" CPPWINRT_EXE)
file(TO_NATIVE_PATH "${CMAKE_CURRENT_BINARY_DIR}/component/calculator/Calculator.winmd" WINMD_FILE)
add_custom_command(
    OUTPUT "${GENERATED_HEADER}"
    COMMAND "${CPPWINRT_EXE}"
            -input "${WINMD_FILE}"
            -output "${GENERATED_FILES_DIR}"
            -reference "${WINRT_METADATA_DIR}\\Windows.Foundation.FoundationContract.winmd"
    DEPENDS "${WINMD_FILE}"
    COMMENT "Generating C++/WinRT files from WinMD - Calculator"
)

# Define the executable
add_executable(${PROJECT_NAME} main.cpp "${GENERATED_HEADER}" "app.manifest")
# Though sounds strange, but VS_WINRT_COMPONENT
# must be set to FALSE. This is because CMake
# assumes that the target is an outdated, C++/CX
# based WinRT component. Thus, it always set /ZW
# option, which causes a conflict when using C++20.
#
# The C++/WinRT binding does not need /ZW build
# option anymore.
set_target_properties(${PROJECT_NAME} PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    VS_WINRT_COMPONENT FALSE
    WINDOWS_EXPORT_ALL_SYMBOLS TRUE)

# Add dependency on Calculator to ensure WinRT files are generated before main compilation
add_dependencies(${PROJECT_NAME} Calculator)

target_include_directories(${PROJECT_NAME} PRIVATE
    "${WINAPP_ROOT}/include"
    "${GENERATED_FILES_DIR}"
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
    # Default to x86 for x64/AMD64 and unknown architectures (for now to match build target)
    set(WINAPP_LIB_DIR "${WINAPP_ROOT}/lib/x64")
    if(NOT CMAKE_SYSTEM_PROCESSOR MATCHES "^(AMD64|amd64|x86_64|x64)$")
        message(STATUS "Unknown architecture ${CMAKE_SYSTEM_PROCESSOR}, defaulting to x64 anyway")
    endif()
endif()

target_link_directories(${PROJECT_NAME} PRIVATE "${WINAPP_LIB_DIR}")
target_link_options(${PROJECT_NAME} PRIVATE /WINMD)
set_target_properties(${PROJECT_NAME} PROPERTIES VS_WINRT_REFERENCES "${CMAKE_CURRENT_BINARY_DIR}/component/calculator/Calculator.winmd")

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
    RuntimeObject # See: https://github.com/microsoft/vcpkg/issues/15339
    Calculator
)

# Copy necessary DLLs or assets if needed (Placeholder)
# winapp pack will handle packaging, but for local debugging we might need things in place.
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${CMAKE_CURRENT_SOURCE_DIR}/appxmanifest.xml"
        "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/AppxManifest.xml"
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${CMAKE_CURRENT_SOURCE_DIR}/Assets"
        "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Assets"
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${WINMD_FILE}"
        "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Calculator.winmd"
    COMMENT "Copying AppxManifest.xml, Assets, and WinMD to output directory"
)
