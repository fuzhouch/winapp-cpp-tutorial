# CMakeLists.txt for Calculator WinRT Component
cmake_minimum_required(VERSION 3.20)

# Set the component name
set(COMPONENT_NAME "Calculator")

# Setup winapp package paths
set(WINAPP_PACKAGES_ROOT "$ENV{UserProfile}/.winapp/packages")
set(CPPWINRT_VERSION "2.0.250303.1")
set(SDK_CPP_VERSION "10.0.26100.7705")

# Define tool paths
# TO_NATIVE_PATH is used to convert paths to Windows format.
# This is required for midl.exe and cppwinrt.exe which expect Windows-style paths
# even when run in a Unix-like environment (e.g., WSL or Git Bash).
file(TO_NATIVE_PATH "${WINAPP_PACKAGES_ROOT}/Microsoft.Windows.CppWinRT.${CPPWINRT_VERSION}/bin/cppwinrt.exe" CPPWINRT_EXE)
file(TO_NATIVE_PATH "${WINAPP_PACKAGES_ROOT}/Microsoft.Windows.SDK.CPP.${SDK_CPP_VERSION}/c/bin/10.0.26100.0/x64/midl.exe" MIDL_EXE)
file(TO_NATIVE_PATH "${WINAPP_PACKAGES_ROOT}/Microsoft.Windows.SDK.CPP.${SDK_CPP_VERSION}/c/References/10.0.26100.0" WINRT_METADATA_DIR)

file(TO_NATIVE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/${COMPONENT_NAME}.idl" IDL_FILE)
file(TO_NATIVE_PATH "${CMAKE_CURRENT_BINARY_DIR}/${COMPONENT_NAME}.winmd" WINMD_FILE)
file(TO_NATIVE_PATH "${CMAKE_CURRENT_BINARY_DIR}" OUTPUT_DIR)

file(TO_NATIVE_PATH "${CMAKE_CURRENT_BINARY_DIR}/GeneratedFiles" GENERATED_FILES_DIR)
file(MAKE_DIRECTORY "${GENERATED_FILES_DIR}")
set(CPPWINRT_GENERATED_MODULE_CPP "${GENERATED_FILES_DIR}/module.g.cpp")

add_custom_command(
    OUTPUT "${WINMD_FILE}"
    COMMAND "${MIDL_EXE}" "${IDL_FILE}" /h "nul" /winrt /metadata_dir "${WINRT_METADATA_DIR}" /out "${OUTPUT_DIR}"
    DEPENDS "${IDL_FILE}"
    COMMENT "Compiling IDL file to WinMD"
)

# Generate C++/WinRT headers and sources from .winmd
# Option -optimize is required, or module.g.cpp will
# hardcode the header path, which causes compilation failure.
# REF:
# - https://github.com/microsoft/WindowsAppSDK/issues/3035
# - https://github.com/microsoft/cppwinrt/issues/1236 
add_custom_command(
    OUTPUT "${CPPWINRT_GENERATED_MODULE_CPP}" "${CPPWINRT_GENERATED_COMPONENT_CPP}"
    COMMAND "${CPPWINRT_EXE}" 
            -input "${WINMD_FILE}" 
            -output "${GENERATED_FILES_DIR}"
            -pch "."
            -component
            -optimize
            -name ${COMPONENT_NAME}
            -reference "${WINRT_METADATA_DIR}\\Windows.Foundation.FoundationContract.winmd"
    DEPENDS "${WINMD_FILE}"
    COMMENT "Generating C++/WinRT files from WinMD"
)

# Collect all generated source files
file(GLOB_RECURSE GENERATED_SOURCES
    "${GENERATED_FILES_DIR}/*.cpp"
    "${GENERATED_FILES_DIR}/*.h"
    )

# Create the WinRT component as a shared library
add_library(${COMPONENT_NAME} SHARED
    ${GENERATED_SOURCES}
    "${IDL_FILE}"
    "${WINMD_FILE}"
    Calculator.cpp
)

# Add custom target to ensure generation happens
add_custom_target(GenerateCalculatorFiles
    DEPENDS "${CPPWINRT_GENERATED_MODULE_CPP}"
)

add_dependencies(${COMPONENT_NAME} GenerateCalculatorFiles)

# Set target properties
set_target_properties(${COMPONENT_NAME} PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    VS_WINRT_COMPONENT TRUE
)

# Include directories
target_include_directories(${COMPONENT_NAME} PRIVATE
    "${GENERATED_FILES_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}"
)

# Link against required libraries
target_link_libraries(${COMPONENT_NAME} PRIVATE
    windowsapp
)

# Set the output directory
set_target_properties(${COMPONENT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)