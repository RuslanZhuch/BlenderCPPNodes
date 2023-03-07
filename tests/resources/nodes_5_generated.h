#pragma once
#include "generationIncludes.h"

auto schema_5(auto&& arg1)
{
    const auto stretchResult{ MultiOutput::stretch(arg1) };
    const auto [ Vec2x, Vec2y ]{ Types::Vec2(stretchResult) };

    struct OutS
    {
        decltype(Vec2x) out1;
        decltype(Vec2y) out2;
    };
    return OutS(Vec2x, Vec2y);
}
