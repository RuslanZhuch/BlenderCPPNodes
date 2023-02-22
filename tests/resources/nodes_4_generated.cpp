auto code(auto&& arg1)
{
    const decltype(auto) xorResult{ xor(arg1) };
    const decltype(auto) notResult{ not(xorResult) };
    const decltype(auto) orResult{ or(arg1) };
    const decltype(auto) andResult{ and(notResult, orResult) };
    return { andResult, orResult };
}
