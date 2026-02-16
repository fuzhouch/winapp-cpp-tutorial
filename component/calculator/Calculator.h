#pragma once
#include "pch.h"
#include "WinAppTutorial/Calculator.g.h"

namespace winrt::WinAppTutorial::implementation
{
    struct Calculator : CalculatorT<Calculator>
    {
        Calculator() = default;
        int32_t Add(int32_t a, int32_t b);
    };
}
namespace winrt::WinAppTutorial::factory_implementation
{
    struct Calculator : CalculatorT<Calculator, implementation::Calculator>
    {
    };
}
