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
        jump = 0
        for i, line in enumerate(file):
            for w, c in enumerate(line):
                if jump:
                    jump = jump - 1
                    continue
                if c in ['(',')']:
                    print(f"{'LEFT' if c=='(' else 'RIGHT'}_PAREN {c} null")
                elif c in ['{','}']:
                    print(f"{'LEFT' if c=='{' else 'RIGHT'}_BRACE {c} null")
                elif c=='*':
                    print("STAR * null")
                elif c=='.':
                    print("DOT . null")
                elif c==',':
                    print("COMMA , null")
                elif c=='+':
                    print("PLUS + null")
                elif c=='-':
                    print("MINUS - null")
                elif c==';':
                    print("SEMICOLON ; null")
                elif c=='=':
                    if line[w:w+2] == '==':
                        print("EQUAL_EQUAL == null")
                        jump = 1
                    else:
                        print("EQUAL = null")
                
                else:
                    print("[line %s] Error: Unexpected character: %s" % (i+1, c), file=sys.stderr)
                    error = True

    print("EOF  null")
    if error:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
