auto code(auto&& arg1)
{
    const auto stretchResult{ stretch(arg1) };
    const auto [ Vec2x, Vec2y ]{ Vec2(stretchResult) };
    return { Vec2x, Vec2y };
}
