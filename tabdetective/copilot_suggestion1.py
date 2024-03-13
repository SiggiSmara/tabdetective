# copilot_suggestion1.pyimport re


def detect_tabular_data(filename, delimiters=None, line_endings="\n", min_rows=3):
    # Default delimiters
    if delimiters is None:
        delimiters = [",", "\t", "|", ";"]

    # Compile regex patterns for delimiters
    patterns = [re.compile(re.escape(d)) for d in delimiters]

    potential_tables = []
    with open(filename, "r") as file:
        lines = file.read().split(line_endings)
        for i, line in enumerate(lines):
            for pattern in patterns:
                # Split line by delimiter
                columns = pattern.split(line)
                # Check if next few lines have the same number of columns
                for j in range(i + 1, min(i + min_rows, len(lines))):
                    if len(pattern.split(lines[j])) != len(columns):
                        break
                else:
                    # If we haven't hit a 'break', we found a potential table
                    potential_tables.append((i, pattern.pattern))

    return potential_tables


# Usage
tables = detect_tabular_data("myfile.txt")
for start_line, delimiter in tables:
    print(f"Potential table found at line {start_line} with delimiter '{delimiter}'")
