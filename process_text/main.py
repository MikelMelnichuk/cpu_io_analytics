import re
import sys


def replace_citations(text: str) -> str:
    r"""
    Replace \cite{...} commands with sequential bracketed numbers.
    Multiple keys inside one \cite{...} become a comma‑separated list.
    The same citation key always gets the same number (first‑occurrence order).
    """
    # Pattern to match \cite{...} where braces contain any characters except '}'
    pattern = re.compile(r'\\cite\{([^}]*)\}')

    # Dictionary to store citation key -> number (1‑based)
    citation_map = {}
    # Counter for the next number to assign
    next_number = 1

    def repl(match: re.Match) -> str:
        nonlocal next_number
        # Extract content inside braces
        content = match.group(1).strip()
        if not content:
            return "[]"  # empty citation

        # Split by commas, trim whitespace, filter empty
        keys = [k.strip() for k in content.split(',') if k.strip()]

        # Assign numbers to new keys (preserving order within this cite)
        numbers = []
        for key in keys:
            if key not in citation_map:
                citation_map[key] = next_number
                next_number += 1
            numbers.append(str(citation_map[key]))

        # Format as [1, 2, 3] (with spaces after commas, as in the user's example)
        return "[" + ", ".join(numbers) + "]"

    return pattern.sub(repl, text)


def main():
    input_file = 'text.txt'

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        return

    modified = replace_citations(content)

    # Write to output file (or print to console)
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(modified)

    print(f"✅ Converted citations in '{input_file}'")


if __name__ == '__main__':
    main()