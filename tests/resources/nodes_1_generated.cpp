auto code(auto&& arg1)
{
    const decltype(auto) notResult{ not(arg1) };
    return { notResult };
}