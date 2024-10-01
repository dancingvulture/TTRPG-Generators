def pluscommas(thing: str) -> str:
    now_with_commas = ''
    for char in thing:
        if char != ' ':
            now_with_commas += char
        else:
            now_with_commas += ', '
    
    return now_with_commas


def reformat(old_separators: tuple[str], new_separator: str) -> None:
    raw_text = ''
    with open("reformat.txt") as file:
        for line in file:
            raw_text += line

    entries = [raw_text]
    for separator in old_separators:
        temp = []
        while entries:
            text = entries.pop()
            for fragment in text.split(separator):
                temp.append(fragment)
        entries = temp

    stripped_entries = []
    for entry in entries:
        stripped_entry = entry.strip()
        if stripped_entry:  # If it's not whitespace.
            stripped_entries.append(stripped_entry)

    final_text = new_separator.join(sorted(set(stripped_entries)))
    print(final_text.lower())

