#include "generationIncludes.h"

auto schema_1(auto&& arg1)
{
    const auto notResult{ Binary::not(arg1) };
    return { notResult };
}
