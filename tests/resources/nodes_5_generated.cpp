#include "generationIncludes.h"

auto schema_5(auto&& arg1)
{
    const auto stretchResult{ MultiOutput::stretch(arg1) };
    const auto [ Vec2x, Vec2y ]{ Types::Vec2(stretchResult) };
    return { Vec2x, Vec2y };
}
