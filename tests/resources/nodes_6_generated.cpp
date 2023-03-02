#include "generationIncludes.h"

auto schema_6(auto&& arg1)
{
    const auto not_001Result{ Binary::not_001(arg1) };
    const auto not_002Result{ Binary::not_002(not_001Result) };
    return { not_002Result };
}
