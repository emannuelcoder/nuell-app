def abv(number: int) -> str:
    suffixes = ["", "K", "M", "B", "T"]

    value = float(number)
    index = 0

    while value >= 1000 and index < len(suffixes) - 1:
        value /= 1000
        index += 1

    if index == 0:
        return str(int(value))
    
    text = f"{value:.1f}"

    if text.endswith(".0"):
        text = text[:-2]

    return f"{text}{suffixes[index]}"