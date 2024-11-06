import sys
from enum import Enum

class TokenType(Enum):
    PAREN = 1
    BRACE = 2
    STAR = 3
    STRING = 4
    NUMBER = 5
    IDENTIFIER = 6
    UNARY = 7
    EQUAL = 8
    SEMI = 9

    EOF = 99

class Token:
    def __init__(self, type, value):
        self.token_type = type
        self.value = value


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    commands = ["parse", "tokenize"]
    if command not in commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    tokens = []
    keywords = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]
    with open(filename) as file:
        error = False
        jump = 0
        for i, line in enumerate(file):
            for w, c in enumerate(line):
                if jump:
                    jump = jump - 1
                    continue
                if c in ['(',')']:
                    tokens.append(Token(TokenType.PAREN, c))
                    if command == "tokenize": print(f"{'LEFT' if c=='(' else 'RIGHT'}_PAREN {c} null")
                elif c in ['{','}']:
                    tokens.append(Token(TokenType.BRACE, c))
                    if command == "tokenize": print(f"{'LEFT' if c=='{' else 'RIGHT'}_BRACE {c} null")
                elif c=='*':
                    tokens.append(Token(TokenType.STAR, "null"))
                    if command == "tokenize": print("STAR * null")
                elif c=='.':
                    if command == "tokenize": print("DOT . null")
                elif c==',':
                    if command == "tokenize": print("COMMA , null")
                elif c=='+':
                    if command == "tokenize": print("PLUS + null")
                elif c=='-':
                    if command == "tokenize": print("MINUS - null")
                elif c==';':
                    tokens.append(Token(TokenType.SEMI, "null"))
                    if command == "tokenize": print("SEMICOLON ; null")
                elif c==' ' or c=='\t' or c=='\n':
                    continue
                elif c=='=':
                    if line[w:w+2] == '==':
                        if command == "tokenize": print("EQUAL_EQUAL == null")
                        jump = 1
                    else:
                        if command == "tokenize": print("EQUAL = null")
                elif c=='"':
                    string = ""
                    unterminated = True
                    for j in range(w+1, len(line)):
                        if line[j] == '"':
                            jump = j - w
                            unterminated = False
                            break
                        else:
                            string = string + line[j]
                    if unterminated:
                        if command == "tokenize": print("[line %s] Error: Unterminated string." % (i+1), file=sys.stderr)
                        error = True
                        break
                    else:
                        tokens.append(Token(TokenType.STRING, string))
                        if command == "tokenize": print(f'STRING "{string}" {string}')
                elif c=='!':
                    if line[w:w+2] == '!=':
                        if command == "tokenize": print("BANG_EQUAL != null")
                        jump = 1
                    else:
                        if command == "tokenize": print("BANG ! null")
                elif c=='<':
                    if line[w:w+2] == '<=':
                        if command == "tokenize": print("LESS_EQUAL <= null")
                        jump = 1
                    else:
                        if command == "tokenize": print("LESS < null")
                elif c=='>':
                    if line[w:w+2] == '>=':
                        if command == "tokenize": print("GREATER_EQUAL >= null")
                        jump = 1
                    else:
                        if command == "tokenize": print("GREATER > null")
                elif c=='/':
                    if line[w:w+2] == '//':
                        break
                    else:
                        if command == "tokenize": print("SLASH / null")
                elif c in map(lambda s: str(s) ,list(range(10))):
                    for j in range(w+1, len(line)):
                        if line[j] in map(lambda s: str(s) ,list(range(10))) or line[j] == '.':
                            jump += 1
                        else:
                            break
                    tokens.append(Token(TokenType.NUMBER, float(line[w:w+jump+1])))
                    if command == "tokenize": print(f'NUMBER {line[w:w+jump+1]} {float(line[w:w+jump+1])}')
                elif c.isalpha() or c=='_':
                    for j in range(w+1, len(line)):
                        if line[j].isalnum() or line[j]=='_':
                            jump += 1
                        else:
                            break
                    kw = line[w:w+jump+1]
                    if kw in keywords:
                        tokens.append(Token(TokenType.IDENTIFIER, kw))
                        if command == "tokenize": print(f"{kw.upper()} {kw} null")
                    else: 
                        if command == "tokenize": print(f"IDENTIFIER {kw} null")
                
                else:
                    if command == "tokenize": print("[line %s] Error: Unexpected character: %s" % (i+1, c), file=sys.stderr)
                    error = True

    if command == "tokenize": print("EOF  null")
    tokens.append(Token(TokenType.EOF, "null"))

    if command == "parse":
        for i in range(len(tokens)-1):
            print(tokens[i].value, end='')
            if tokens[i].token_type == TokenType.PAREN and tokens[i].value == '(':
                print("group", end=' ')

    if error:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
