def parse(value: str) -> int:
    v = value.lower().replace(",", "").strip()

    multipliers = {
        "kk": 1_000_000,
        "mi": 1_000_000,
        "m": 1_000_000,
        "k": 1_000,
        "bi": 1_000_000_000,
        "b": 1_000_000_000,
        "t": 1_000_000_000_000,
    }

    for suffix in sorted(multipliers, key=len, reverse=True):
        if v.endswith(suffix):
            num = v[:-len(suffix)]

            if not num.replace(".", "", 1).isdigit():
                raise ValueError

            return int(float(num) * multipliers[suffix])

    if not v.replace(".", "", 1).isdigit():
        raise ValueError

    return int(float(v))