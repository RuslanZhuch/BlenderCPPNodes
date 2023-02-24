auto code(auto&& arg1)
{
    const auto xorResult{ xor(arg1) };
    const auto notResult{ not(xorResult) };
    const auto orResult{ or(arg1) };
    const auto andResult{ and(notResult, orResult) };
    return { andResult, orResult };
}
