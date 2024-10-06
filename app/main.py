import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        error = False
        for i, line in enumerate(file):
            for c in line:
                if c in ['(',')']:
                    print(f"{'LEFT' if c=='(' else 'RIGHT'}_PAREN {c} null")
                if c in ['{','}']:
                    print(f"{'LEFT' if c=='{' else 'RIGHT'}_BRACE {c} null")
                if c=='*':
                    print("STAR * null")
                if c=='.':
                    print("DOT . null")
                if c==',':
                    print("COMMA , null")
                if c=='+':
                    print("PLUS + null")
                if c=='-':
                    print("MINUS - null")
                if c==';':
                    print("SEMICOLON ; null")
                
                else:
                    print(f"[line {i}] Error: Unexpected character: {c}", file=sys.stderr)
                    error = True

    print("EOF  null")
    if error:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
