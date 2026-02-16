#include "pch.h"
#include <iostream>
#include <winrt/Windows.Foundation.h>
#include "winrt/WinAppTutorial.h"

int main() {
    try {
        winrt::init_apartment();

        // Use direct constructor approach
        winrt::WinAppTutorial::Calculator calculator;
        int result = calculator.Add(3, 5);
        std::cout << "Result of 3 + 5 = " << result << std::endl;
    } catch (const winrt::hresult_error& ex) {
        std::wcout << L"WinRT Error: 0x" << std::hex <<ex.code() << std::dec << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
