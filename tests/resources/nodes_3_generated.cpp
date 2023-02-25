auto schema_3(auto&& arg1)
{
    const auto notResult{ not(arg1) };
    const auto andResult{ and(notResult, arg1) };
    return { andResult };
}
