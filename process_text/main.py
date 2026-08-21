import re


def replace_citations(text: str) -> str:
    r"""
    Replace every occurrence of \cite{...} with [n] where n is the
    occurrence order (1‑based).
    """
    # Match \cite{...} – the braces may contain any characters except '}'
    pattern = re.compile(r'\\cite\{([^}]*)\}')

    # Counter for occurrence number
    counter = 1

    def repl(match: re.Match) -> str:
        nonlocal counter
        replacement = f'[{counter}]'
        counter += 1
        return replacement

    return pattern.sub(repl, text)


def main():
    input_file = 'text.txt'
    # output_file = 'text_with_citations.txt'   # optional

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        return

    modified = replace_citations(content)

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(modified)


if __name__ == '__main__':
    import sys
    main()
