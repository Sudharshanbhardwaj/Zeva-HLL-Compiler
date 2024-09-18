from dataclasses import dataclass
from typing import Any, List, Tuple, Union
import ply.yacc as yacc
from pprint import pprint
from ply import lex
import sys


# Define tokens
tokens = [
    'ID',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    'LSPAREN',
    'RSPAREN',
    'DOT',
    'ASSIGN',
    'PLUS',
    'PLUSPLUS',
    'MINUS',
    'MUL',
    'DIV',
    'REM',
    'EQEQ',
    'NOTEQ',
    'GT',
    'LT',
    'SUBSTR',
    'GTEQ',
    'MINUSMINUS',
    'LTEQ',
    'STRING',
    'VAR',
    'INT',
    'BOOL',
    'BEGIN',
    'END',
    'IF',
    'ELIF',
    'ELSE',
    'WHILE',
    'ZOUT',
    'STR',
    'VOID',
    'RETURN',
    'CON',
    'TUPLE',
    'LIST',
    'SIZE',
    'DELETE',
    'FRONT',
    'REAR',
    'TRY',
    'EXCEPT',
    'TRUE',
    'FALSE',
    'ADDD',
]

# Define keywords and reserved words
keywords = {
    'var': 'VAR',
    'int': 'INT',
    'bool': 'BOOL',
    'begin': 'BEGIN',
    'end': 'END',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'zout': 'ZOUT',
    'str': 'STR',
    'return': 'RETURN',
    'con': 'CON',
    'tuple': 'TUPLE',
    'list': 'LIST',
    'substr':'SUBSTR',
    'size': 'SIZE',
    'delete': 'DELETE',
    'front': 'FRONT',
    'addd'  : 'ADDD',
    'rear': 'REAR',
    'try': 'TRY',
    'except': 'EXCEPT',
    'true': 'TRUE',
    'false': 'FALSE',
    'void' : 'VOID'
}

# Tokens with associated regular expressions
t_ignore = ' \t'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_LSPAREN = r'\['
t_RSPAREN = r'\]'
t_DOT = r'\.'
t_STRING = r'\".*?\"'

t_ASSIGN = r'='
t_PLUS = r'\+'
t_PLUSPLUS = r'\+\+'
t_MINUS = r'-'
t_MINUSMINUS = r'\--'
t_MUL = r'\*'
t_DIV = r'/'
t_REM = r'%'
t_EQEQ = r'=='
t_NOTEQ = r'!='
t_GT = r'>'
t_LT = r'<'
t_GTEQ = r'>='
t_LTEQ = r'<='


def t_NUMBER(t):
  r'-?\d+'
  t.value = int(t.value)
  return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'ID')
    return t

def t_COMMENT(t):
    r'@.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

precedence = (
    ('left','PLUS','MINUS'),
    ('left','MUL','DIV' ,'REM'),
    #('nonassoc','EQEQ','NOTEQ','GT','LT','GTEQ','LTEQ'),
    ('right','PLUSPLUS','MINUSMINUS'),
    ('left', 'ID'),
    ('left', 'LPAREN', 'LSPAREN')
    )
# Import the AST classes
from myAST import (
    Number, String, Bool, Start, StatementList, Declaration, Id, Assignment, ContainerAccess, CompoundTypes, CompoundTypeAccess,
    FunctionDefinition, FunctionCall, ParameterList, OptionalParameterList, Condition, IfStatement, WhileStatement,
    Expression, Pexpression, BinaryOperator, Term, UnaryOperator, TryExcept, Print, Data
)

# Tokens definition and other lexer rules...

# Grammar rules with actions constructing AST nodes
def p_start(p):
    'start : statement_list'
    p[0] = Start(p[1])

def p_statement_list(p):
  '''statement_list : statement_list statement SEMICOLON
                    |  '''
  if len(p) == 4:
      if isinstance(p[1], StatementList):
          p[0] = StatementList(p[1].statements + [p[2]])
      else:
          p[0] = StatementList([p[1]])
  else:
      p[0] = StatementList([])


def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_stmnt
                 | while_stmt
                 | function_definition
                 | expression
                 | compound_types
                 | compound_type_access
                 | try_except
                 | print'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : VAR type ID ASSIGN L'''
    p[0] = Declaration(p[2], p[3],p[4],p[5])

def p_assignment(p):
    '''assignment :  ID ASSIGN L
                  |  compound_type_access ASSIGN L'''
    if (p[1] == 'ID'):
        p[0] = Assignment(p[1], p[2], p[3])
    else :
        p[0] = Assignment(p[1], p[2], p[3])

def p_L(p):
    '''L : statement
         | function_call
         | container_access
         | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None

def p_function_call(p):
    'function_call : ID LPAREN data RPAREN'
    p[0] = FunctionCall(p[1], p[3])

def p_container_access(p):
    'container_access : LPAREN ID LSPAREN factor RSPAREN RPAREN'
    p[0] = ContainerAccess(p[2], p[4])


def p_type(p):
    '''type : INT
            | BOOL
            | STR
            | VOID'''
    p[0] = p[1]

def p_compound_types(p):
    '''compound_types : A ID ASSIGN LPAREN data RPAREN'''
    p[0] = CompoundTypes(p[1], p[2], p[3], p[5])

def p_A(p):
    '''A : TUPLE
         | LIST'''


def p_data(p):
    '''data : expression hi
            | '''
    
    if(len(p)>1):
        p[0] = p[1], p[2]
    else :
        p[0]=None

def p_hi(p):
    '''hi : COMMA data
          | '''
    if(len(p)>1):
      if p[1] == ',':
        p[0] = p[2]
    else :
        p[0]=None
def p_compound_type_access(p):
    '''compound_type_access : ID DOT F 
                            | ID LSPAREN expression RSPAREN'''
    if p[2] == '.':
        p[0] = CompoundTypeAccess(p[1], p[3])
    else:
        p[0] = CompoundTypeAccess(p[1], p[3])

# Other grammar rules with actions constructing AST nodes
def p_F(p):
  '''F : CON LPAREN factor RPAREN
       | FRONT
       | ADDD
       | LPAREN factor RPAREN
       | REAR
       | SIZE
       | DELETE
       | SUBSTR LPAREN data RPAREN
       |  '''
  if len(p) == 5:
      if p[1] == 'con':
          p[0] = p[1], p[3]
      elif p[1] == 'addd':
          p[0] = p[1], p[3]
      else:
          p[0] = p[1]
  elif len(p) == 2:
      p[0] = '' + p[1].lower()
  elif len(p) == 7:
      p[0] = 'substr', p[3], p[5]
  else:
      p[0] = None  # Handle the case of empty production


def p_binary_operator(p):
   '''binary_operator : MINUS 
                   | MUL 
                   | PLUS
                   | DIV 
                   | REM '''
   p[0] = p[1]
def p_unary_operator(p):
  ''' unary_operator : PLUSPLUS 
                     | MINUSMINUS '''
  p[0] = p[1]

def p_term(p):
  '''term : factor
          | term unary_operator'''
  if len(p) == 2:
    p[0] = p[1]
  else:
   p[0] = p[1], p[2]

def p_if_stmnt(p):
    '''if_stmnt : IF LPAREN condition RPAREN  BEGIN  statement_list END T K'''
    p[0] = IfStatement(p[3], p[6], p[8], p[9])

def p_comparison_operator(p):
  '''comparison_operator : EQEQ 
                       | NOTEQ 
                       | LT 
                       | GT 
                       | LTEQ 
                       | GTEQ '''
  p[0] = p[1]

def p_T(p):
    '''T :  ELIF LPAREN condition RPAREN BEGIN  statement_list END T
         |   '''
    if len(p) == 9:
        p[0] = [(p[3], p[6])] + p[8]
    else:
        p[0] = []

def p_K(p):
    '''K : ELSE BEGIN statement_list END 
         |  '''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = []

def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN condition RPAREN BEGIN statement_list END'''
    p[0] = WhileStatement(p[3], p[6])

def p_function_definition(p):
    '''function_definition : type ID LPAREN parameter_list RPAREN BEGIN statement_list  RETURN L SEMICOLON END'''
    p[0] = FunctionDefinition(p[1],p[2], p[4], p[7], p[9])

def p_parameter_list(p):
    '''parameter_list : type ID optional_parameter_list
                      | A LSPAREN type RSPAREN ID LSPAREN RSPAREN optional_parameter_list 
                      |  '''
    if len(p) == 4:
        p[0] = ParameterList([(p[1], p[2])] + p[3])
    elif len(p) == 9:
        p[0] = ParameterList([(p[3], p[5])] + p[8])
    else :
      p[0] = None

def p_optional_parameter_list(p):
    '''optional_parameter_list : COMMA type ID optional_parameter_list
                               | COMMA A LSPAREN type RSPAREN ID LSPAREN RSPAREN optional_parameter_list 
                               |  '''
    if len(p) == 5:
        p[0] = [(p[2], p[3])] + p[4]
    elif len(p) == 9:
        p[0] = [(p[4], p[6])] + p[9]
    else:
        p[0] = []

def p_condition(p):
    '''condition : expression  comparison_operator  expression
                 | compound_type_access comparison_operator compound_type_access'''
    p[0] = Condition(p[1], p[2], p[3])

def p_expression(p):
  '''expression : expression binary_operator term
                | term'''
  if len(p) == 4:
      p[0] = Expression((p[1], BinaryOperator(p[2]), p[3]))
  else:
      p[0] = p[1]


def p_factor(p):
    ''' factor :  ID 
               | NUMBER 
               | STRING
               | TRUE
               | FALSE 
               | LPAREN expression RPAREN'''
    if len(p) == 4:
        p[0] = p[2]
    elif p.slice[1].type == 'ID':
        p[0] = Id(p[1])
    elif p.slice[1].type == 'NUMBER':
        p[0] = Number(p[1])
    elif p.slice[1].type == 'STRING':
        p[0] = String(p[1])
    else:
        p[0] = Bool(p[1])


def p_try_except(p):
    '''try_except : BEGIN TRY statement_list EXCEPT statement_list END'''
    p[0] = TryExcept(p[3], p[5])

def p_print(p):
    '''print : ZOUT LPAREN y RPAREN'''
    p[0] = Print(p[3])

def p_y_expression(p):
    '''y : expression'''
    p[0]=Expression(p[1])

def p_y_compound(p):
    '''y : compound_type_access'''
    p[0] = CompoundTypeAccess(p[1],None)

def find_column(input, p):
    line_start = input.rfind('\n', 0, p.lexpos) + 1
    return (p.lexpos - line_start) + 1


def p_error(p):
  if p is not None:
      column = find_column(text, p)        
      print("Found unexpected character '%s' at line '%s' and column '%s'" % (p.value, p.lineno, column))
  else:
      print("Unexpected end of input!Empty file or syntax error at EOF!")

# Build the parser
parser = yacc.yacc()


try:
    text = open("test_cases/test_ceasar.zeva", "r").read()
    ast = parser.parse(text)
    pprint(ast.__dict__)
except EOFError:
    print("File could not be opened!")
    
