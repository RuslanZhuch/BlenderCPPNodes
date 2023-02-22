auto code(auto&& arg1)
{
    const decltype(auto) notResult{ not(arg1) };
    const decltype(auto) andResult{ and(notResult, arg1) };
    return { andResult };
}
