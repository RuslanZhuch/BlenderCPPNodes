#pragma once
#include "generationIncludes.h"

auto schema_4(auto&& arg1)
{
    const auto xorResult{ Blocks::Binary::xor(arg1) };
    const auto notResult{ Blocks::Binary::not(xorResult) };
    const auto orResult{ Blocks::Binary::or(arg1) };
    const auto andResult{ Blocks::Binary::and(notResult, orResult) };

    struct OutS
    {
        decltype(andResult) out1;
        decltype(orResult) out2;
    };
    return OutS(andResult, orResult);
}
