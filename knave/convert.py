"""
Take text copied from a table in Knave and output it in a text file.
"""


import argparse


_NUMBERS = [str(x) for x in range(10)]


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="Knave Table Converter",
        description="Takes raw text copied from the knave pdf and converts"
                    " it into a single line of text, with each entry separated"
                    " by a comma.",
    )
    
    parser.add_argument(
        "input_filename",
        help="Raw text copied from the book (in .txt file)",
        
    )
    parser.add_argument(
        "output_filename",
        help="full filename of output file (include extension)",
    )
    
    return parser.parse_args()


def convert_file_to_list(filename: str) -> list:
    """Converts a specific kind of raw text file to a list."""
    file_contents = []
    with open(filename) as file:
        for line in file:
            line_items = _convert_line_to_list(line)
            file_contents.extend(line_items)
    return sorted(file_contents)        
            
            
def _convert_line_to_list(line: str) -> list:
    """Contains the real logic for properly extracting the file contents."""
    items = []
    inside_parenthesis = False
    previous_char_was_number = False
    
    current_item = ""
    for char in line:
        # First we check if this character is a number that's not inside parenthesis.
        if char in _NUMBERS and not inside_parenthesis:
            # If this is a new number, then it this is the start of a new item
            if not previous_char_was_number and current_item:
                items.append(current_item.strip())
                current_item = ""
            
            # If this isn't a new number, then the new item has already
            # started and we don't add numbers not inside parenthesis.
        
        # All other non-numbers or numbers inside parenthesis are added to
        # the current item.
        else:
            current_item += char
        
        # Finally we set the logic flags up for the next loop.
        if char == "(":
            inside_parenthesis = True
            
        elif char == ")":
            inside_parenthesis = False
        
        previous_char_was_number = True if char in _NUMBERS else False
    
    # For when we reach the EOL, append what we have as an item.
    if current_item:
        items.append(current_item.strip())
    
    return items
    

def write_list_to_file(content: str, filename: str) -> None:
    """Write the given string to a file."""
    with open(filename, 'w') as file:
        file.write(content)


def convert_list_to_string(items:  list) -> str:
    """Convert a list if items to a single line with all items separated
    by commas."""
    output = ""
    for thing in items:
        output += thing + ", "
    return output[:-2]


def main():
    args = parse_arguments()
    file_contents = convert_file_to_list(args.input_filename)
    text_to_write = convert_list_to_string(file_contents)
    write_list_to_file(text_to_write, args.output_filename)
    
    
if __name__ == "__main__":
    main()