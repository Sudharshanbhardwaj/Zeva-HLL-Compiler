
#tokens
from dataclasses import dataclass
import sys

EOF           = 'EOF'
ID            = 'ID'
NUMBER        = 'NUMBER'
LPAREN        = 'LPAREN'
RPAREN        = 'RPAREN'
SEMI          = 'SEMI'
COMMA         = 'COMMA'
LSPAREN       = 'LSPAREN'
RSPAREN       = 'RSPAREN'
DOT           = 'DOT'
QUOTATION     = 'QUOTATION'

# operators
ASSIGN        = 'ASSIGN'
PLUS          = 'PLUS'
PLUSPLUS      = 'PLUSPLUS'
MINUS         = 'Minus'
MINUSMINUS    = 'MINUSMINUS'
MUL           = 'MUL'
DIV           = 'DIV'
REM           = 'REM'
EQEQ          = 'EQEQ'
NOTEQ         = 'NOTEQ'
GT            = 'GT'
LT            = 'LT'
GTEQ          = 'GTEQ'
LTEQ          = 'LTEQ'
AND           = 'AND'
OR            = 'OR'


# keywords
VAR           = 'VAR'
INTEGER       = 'INT'
BOOLEAN       = 'BOOL'
BEGIN         = 'BEGIN'
END           = 'END'
IF            = 'IF'
EIF           = 'ELIF'
ELSE          = 'ELSE'
WHILE         = 'WHILE'
PRINT         = 'ZOUT'
STRING        = 'STR'
FUNCTION      = 'FUNC'
RETURN        = 'RETURN'
FOR           = 'FOR'
CON           = 'CON'
TUPLE         = 'TUPLE'
LIST          = 'LIST'
ADD           = 'ADD'
SIZE          = 'SIZE'
LIST          = 'LIST'
FRONT         = 'FRONT'
REAR          = 'REAR'
DELETE        = 'DELETE'
SIZE          = 'SIZE'
TRY           = 'TRY'
EXCEPT        = 'EXCEPT'

@dataclass
# class to store the token types and values
class Token:
    type: str
    value: object

    def __str__(self):
        return '({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'var': Token('VAR', 'var'),
    'int': Token('INT', 'int'),
    'bool': Token('BOOL', 'bool'),
    'begin': Token('BEGIN', 'begin'),
    'end': Token('END', 'end'),
    'for': Token('FOR', 'for'),
    'true': Token('TRUE', 'true'),
    'false': Token('FALSE', 'false'),
    'if': Token('IF', 'if'),
    'elif': Token('ELIF', 'elif'),
    'else': Token('ELSE', 'else'),
    'zout': Token('ZOUT', 'zout'),
    'while': Token('WHILE', 'while'),
    'str': Token('STR', 'str'),
    'func': Token('FUNC', 'func'),
    'return': Token('RETURN', 'return'),
    'try': Token('TRY', 'try'),
    'except': Token('EXCEPT', 'except'),
    'add': Token('ADD', 'add'),
    'size': Token('SIZE', 'size'),
    'list': Token('LIST', 'list'),
    'delete': Token('DELETE', 'delete'),
    'front': Token('FRONT', 'front'),
    'rear': Token('REAR', 'rear'),
    'con': Token('CON', 'con'),
    'tuple': Token('TUPLE', 'tuple')

}

class Lexer(object):
    def __init__(self, text):

        self.text = text                        # stream of input
        self.pos = 0                            # current position in the stream
        self.lineNum = 1                        # line number in code
        self.curLinePos = 0                     # current position in current line of program
        self.indicator = 0

        if text == "":
            print("Empty Program")
            self.curChar = None

        else:
            self.curChar = self.text[self.pos]      # current character in the stream
        self.curLine = self.curChar             # current line of program read till now


    def error(self):
        print("Current Character", self.curChar)
        sys.exit('Invalid character')

    def nextChar(self):                         # advances the pos pointer
        self.pos += 1
        self.curLinePos += 1

        if self.pos > len(self.text) - 1:       # end of input stream
            self.curChar = None                 
        else:
            self.curChar = self.text[self.pos]
            self.curLine += self.curChar
            if self.curChar == '\n':
                self.lineNum+=1
                self.curLine=""
                self.curLinePos=0


    def peek(self):                             # returns the lookahead character
        if self.pos + 1 > len(self.text) - 1:
            return None
        else:
            return self.text[self.pos + 1]

    def skipSpaces(self):                       # to skip white spacses
        while self.curChar is not None and self.curChar.isspace():
            # if self.curChar == '\n':
            #     self.lineNum+=1
            #     self.curLine=""
            #     self.curLinePos=0
            self.nextChar()

    def skipComments(self):
        
        if self.curChar == '@':
            self.nextChar()
            if self.curChar == '*':
                # Multi-line comment
                self.nextChar()  # Skip '*'
                while self.curChar is not None and not (self.curChar == '*' and self.text[self.pos + 1] == '@'):
                    self.nextChar()
                self.nextChar()  # Skip '*'
                self.nextChar()  # Skip '@'
            else:
                # Single-line comment
                while self.curChar is not None and self.curChar != '\n':
                    self.nextChar()

    def number(self):                           
        # Consume all the consecutive digits and decimal if present.
        result = ''
        while self.curChar is not None and self.curChar.isdigit():
            result += self.curChar
            self.nextChar()

        if self.curChar == '.':
            result += self.curChar
            self.nextChar()

            while (
                self.curChar is not None and
                self.curChar.isdigit()
            ):
                result += self.curChar
                self.nextChar()

            token = Token('REAL_CONST', float(result))
        else:
            token = Token(NUMBER, int(result))

        return token

    def _id(self):
        # Handles identifiers and reserved keywords
        result = ''
        while self.curChar is not None and self.curChar.isalnum():
            result += self.curChar
            self.nextChar()
            
        token = KEYWORDS.get(result, Token(ID, result))
        return token
    
                     
    def Stringlex(self):
        # Handles strings
        result = ''
        while self.curChar != '"':
            result += self.curChar
            self.nextChar()

        token = Token(STRING, result)
        return token

    def get_token(self):
        # returns the token and token type
        while self.curChar is not None:

            if self.curChar.isspace():
                self.skipSpaces()
                continue

            if self.curChar == '@':
                self.skipComments()
                continue

            if self.curChar.isalpha():
                return self._id()

            if self.curChar.isdigit():
                return self.number()

            
            if self.curChar == '=':
                if self.peek() == '=':
                    self.nextChar()
                    self.nextChar()
                    return Token(EQEQ, '==')
                else:
                    self.nextChar()
                    return Token(ASSIGN, '=') 

            if self.curChar == "|":
                if self.peek() == "|":
                    self.nextChar()
                    self.nextChar()
                    return Token(OR, "||")


            if self.curChar == "&":
                if self.peek() == "&":
                    self.nextChar()
                    self.nextChar()
                    return Token(AND, "&&")

            if self.curChar == '>':
                if self.peek() == '=':
                    self.nextChar()
                    self.nextChar()
                    return Token(GTEQ, '>=')
                else:
                    self.nextChar()
                    return Token(GT, '>')

            if self.curChar == '<':
                if self.peek() == '=':
                    self.nextChar()
                    self.nextChar()
                    return Token(LTEQ, '<=')
                elif self.peek() == '>':
                    self.nextChar()
                    self.nextChar()
                    return Token(NOTEQ, '!=') # <>
                else:
                    self.nextChar()
                    return Token(LT, '<')

            if self.curChar == '*':                 
                self.nextChar()
                return Token(MUL, '*')

            if self.curChar == "%":
                self.nextChar()
                return Token(REM, '%')

            if self.curChar == '+':
                if self.peek() == '+':
                    self.nextChar()
                    self.nextChar()
                    return Token(PLUSPLUS, '++')
                else:
                    return Token(PLUS, '+')

            if self.curChar == '-':
                self.nextChar()
                return Token(MINUS, '-')

            if self.curChar == '/':  
              self.nextChar()
              return Token(DIV, '/')

            if self.curChar == '(':
                self.nextChar()
                return Token(LPAREN, '(')

            if self.curChar == ')':
                self.nextChar()
                return Token(RPAREN, ')')

            if self.curChar == ';':
                self.nextChar()
                return Token(SEMI, ';')

            if self.curChar == ',':
                self.nextChar()
                return Token(COMMA, ',')
            
            
            if ((self.curChar == '"') and (self.indicator == 0 or self.indicator == 2)):
                self.indicator += 1
                if(self.indicator == 3): 
                    self.nextChar()
                    self.indicator = 0
                return Token(QUOTATION, ' /" ')
            
            if self.curChar == '"':
                self.nextChar()
                self.indicator += 1
                return self.Stringlex()  

            if self.curChar == '[':
                self.nextChar()
                return Token(LSPAREN, '[')   

            if self.curChar == ']':
                self.nextChar()
                return Token(RSPAREN, ']')
            
            if self.curChar == '.':
                self.nextChar()
                return Token(DOT, '.')
            
            self.error()

        return Token(EOF, None)

