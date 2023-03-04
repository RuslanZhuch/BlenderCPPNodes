#include "generationIncludes.h"

auto schema_3(auto&& arg1)
{
    const auto notResult{ Binary::not(arg1) };
    const auto andResult{ Binary::and(notResult, arg1) };

    struct OutS
    {
        decltype(andResult) out1;
    };
    return OutS(andResult);
}
