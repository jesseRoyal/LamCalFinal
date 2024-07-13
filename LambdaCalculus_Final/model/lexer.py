import ply.lex as lex

tokens = (
    'LAMBDA',   # Token for the lambda symbol
    'DOT',      # Token for the dot symbol
    'VAR',      # Token for variables (a-z)
    'NUMBER',   # Token for numbers (0-9)
    'LPAREN',   # Token for left parenthesis
    'RPAREN',   # Token for right parenthesis
)

# Regular expressions for tokens
t_LAMBDA = r'\#'      # The lambda symbol (#)
t_DOT = r'\.'         # The dot symbol (.)
t_LPAREN = r'\('      # Left parenthesis
t_RPAREN = r'\)'      # Right parenthesis

def t_NUMBER(t):
    r'\d+'  # Regex to match one or more digits
    t.value = int(t.value)  # Convert the string of digits to an integer
    return t

def t_VAR(t):
    r'[a-z]'  # Regex to match a single lowercase letter a-z
    return t

# A string containing ignored characters (spaces, tabs, and newlines)
t_ignore = ' \t\n'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Usage example
if __name__ == "__main__":
    data = "((((# f . (# g . (# x . (f x (g x))))) (# m . (# n . (n m)))) (# n . z)) p)"
    lexer.input(data)
    for tok in lexer:
        print(tok)
