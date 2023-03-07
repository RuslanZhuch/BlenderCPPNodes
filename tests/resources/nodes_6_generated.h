#pragma once
#include "generationIncludes.h"

auto schema_6(auto&& arg1)
{
    const auto not_001Result{ Binary::not_001(arg1) };
    const auto not_002Result{ Binary::not_002(not_001Result) };

    struct OutS
    {
        decltype(not_002Result) out1;
    };
    return OutS(not_002Result);
}
