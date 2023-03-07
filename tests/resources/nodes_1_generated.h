#pragma once
#include "generationIncludes.h"

auto schema_1(auto&& arg1)
{
    const auto notResult{ Binary::not(arg1) };

    struct OutS
    {
        decltype(notResult) out1;
    };
    return OutS(notResult);
}
