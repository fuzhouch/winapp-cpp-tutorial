#include "pch.h"
#include "Calculator.h"

namespace winrt { namespace WinAppTutorial { namespace implementation {

int32_t Calculator::Add(int32_t a, int32_t b)
{
    return a + b;
}

}}}

#include "WinAppTutorial/Calculator.g.cpp"
