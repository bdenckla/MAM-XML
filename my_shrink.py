""" Exports shrink """


def shrink(parts):
    """ Coalesce (or "collapse") adjecent strings """
    acc = []
    for part in parts:
        if part == '':
            continue
        if acc:
            if isinstance(acc[-1], str) and isinstance(part, str):
                acc[-1] += part
                continue
        assert isinstance(part, (dict, str))
        acc.append(part)
    type_of_parts = type(parts)  # presumably list or tuple
    return type_of_parts(acc)
