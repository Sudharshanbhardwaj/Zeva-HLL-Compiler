from dataclasses import dataclass
from typing import Any, List, Tuple, Union
import ply.yacc as yacc
from pprint import pprint
from ply import lex
import sys
from pprint import pprint


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
    'ADD',
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
    'add'  : 'ADD',
    'rear': 'REAR',
    'try': 'TRY',
    'except': 'EXCEPT',
    'true': 'TRUE',
    'false': 'FALSE'
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
    ('nonassoc','EQEQ','NOTEQ','GT','LT','GTEQ','LTEQ'),
    ('right','PLUSPLUS','MINUSMINUS')
    )
# Import the AST classes
from myAST import (
    Number, String, Bool, Start, StatementList, Declaration, Id, Assignment, CompoundTypes, CompoundTypeAccess,
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
    '''assignment :  ID ASSIGN L'''
    p[0] = Assignment(p[1], p[2], p[3])


def p_L(p):
    '''L : statement
         | ID LPAREN data RPAREN'''
    if len(p) == 5:
        p[0] = FunctionCall(p[1], p[3])
    else:
        p[0] = p[1]

def p_type(p):
    '''type : INT
            | BOOL
            | STR'''
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
       | ADD LPAREN factor RPAREN
       | REAR
       | SIZE
       | DELETE
       | SUBSTR LPAREN data RPAREN
       |  '''
  if len(p) == 5:
      if p[1] == 'con':
          p[0] = p[1], p[3]
      elif p[1] == 'add':
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
   p[0] = p[1], UnaryOperator(p[2])

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
                      |  '''
    if len(p) == 4:
        p[0] = ParameterList([(p[1], p[2])] + p[3])
    else :
      p[0]=None

def p_optional_parameter_list(p):
    '''optional_parameter_list : COMMA type ID optional_parameter_list
                               |  '''
    if len(p) == 5:
        p[0] = [(p[2], p[3])] + p[4]
    else:
        p[0] = []

def p_condition(p):
    '''condition : expression  comparison_operator  expression'''
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
        p[0] = bool(p[1])


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


class Scope:
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def put(self, name, symbol):
        self.dict[name] = symbol

    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        if self.parent == None:
            return None
        return self.parent.get(name)
    def push_scope(self):
      return Scope(self)

    def pop_scope(self):
      return self.parent

# Define symbol table and symbol classes
class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)


class FunctionSymbol(Symbol):
    def __init__(self, name,type, parameters):
        super().__init__(name, type)
        self.parameters = parameters

class SymbolTable():
    def __init__(self):
        self.symbols = {}
        self.current_scope = Scope()

    def add_symbol(self, name, symbol):
        if name in self.symbols:
            raise Exception(f"Duplicate symbol found: {name}")
        else:
          self.symbols[name] = symbol

    def lookup(self, name):
        return self.symbols.get(name)


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = Scope()

    def visit_Number(self, node):
        return VariableSymbol(node.value, "int")

    def visit_String(self, node):
      return VariableSymbol(node.value, "str")

    def visit_bool(self,node):
      return VariableSymbol(None, "bool")

    def visit_BinaryOperator(self, node):
       pass

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
      method_name = f'visit_{type(node).__name__}'  # Use __name__ instead of _name_
      visitor = getattr(self, method_name, self.generic_visit)
      return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_Start(self, node):
        self.visit(node.statement_list)

    def visit_StatementList(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Declaration(self, node):
        type = node.type
        identifier = node.identifier
        self.symbol_table.add_symbol(identifier, VariableSymbol(identifier, type))
        if(isinstance(node.value,FunctionCall)):
          lier=self.symbol_table.lookup(node.value.identifier)
          if lier.type!=type:
            raise Exception(f"function type not matching")
        #self.visit(node.value)
        kieee=self.visit(node.value)
        if kieee is not None:
          if type!=kieee.type:
           raise Exception(f" type not matching")
        

    def visit_Id(self, node):
     symbol = self.symbol_table.lookup(node.id)  # Lookup the symbol directly by identifier
     if symbol is None:
        raise Exception(f"Variable '{node.id}' not found in symbol table")
     return symbol

    def visit_Assignment(self, node):
      identifier = node.identifier  # Extract the identifier from the node
      symbol = self.symbol_table.lookup(identifier)
      if symbol is None:
        raise Exception(f"Variable '{identifier}' not found in symbol table")
      symbol = VariableSymbol(identifier, self.visit(identifier).type)  # Create a VariableSymbol instance
      value=self.visit(node.value)
      if value.type!=symbol.type:
        raise Exception(f"type not matching")
      self.current_scope.put(identifier, symbol)  # Add the symbol to the current scope
      self.visit(node.value)  # Visit the assignment value


    def visit_FunctionDefinition(self, node):
      name = node.identifier
      type_ = node.type
      self.current_scope = self.current_scope.push_scope()
      parameters=None
      if node.parameter_list!=None:
        parameters = node.parameter_list.parameters
        for param_type, param_name in parameters:
          self.symbol_table.add_symbol(param_name, VariableSymbol(param_name, param_type))
      # Push a new scope for the function
      

      # Add function parameters to the symbol table
      
      self.symbol_table.add_symbol(name, FunctionSymbol(name, type_, parameters))
      # Visit the function body
      self.visit(node.statement_list)
      self.visit(node.return_data)
      if node.return_data == None:
       if type_!='void':
        raise Exception(f"return type and the function type not matching")
       
      elif isinstance(node.return_data,FunctionCall):
        kier=self.symbol_table.lookup(node.return_data.identifier)
        if kier.type!=type_:
           raise Exception(f"return type and the function type not matching")
      elif '+' or  '-' or  '*' or  '/' or  '%' in node.return_data:
        if type_!='int':
          raise Exception(f"return type and the function type not matching")
      else :
         hier=self.symbol_table.lookup(node.return_data)
         if hier.type!=type_:
           raise Exception(f"return type and the function type not matching")
      # Pop the function scope
      if parameters is not None:
        for i in parameters:
            self.symbol_table.symbols.pop(i[1], None)
      self.current_scope = self.current_scope.pop_scope()

      # Add the function symbol to the symbol table
      #self.symbol_table.add_symbol(name, FunctionSymbol(name, type_, parameters))

    def visit_FunctionCall(self, node):
      name = node.identifier
      symbol = self.symbol_table.lookup(name)
      if symbol is None:
          raise Exception(f"Function '{name}' not declared")
      parameters = symbol.parameters
      if parameters!=None:
        a=node.expression[1]
        length=1
        while a!=None:
          length=length+1
          a=a[1]
        k=node.expression
        if len(parameters) != length:
          raise Exception(f"Function '{name}' expects {len(parameters)} arguments, but {length} provided")
        else:
         for i in parameters:
          t=self.visit(k[0])
          if i[0]!=t.type:
            raise Exception(f"parameters type is not matching")
          else:
            k=k[1]
    def visit_Expression(self, node):
        if isinstance(node.expression, tuple):
          left = self.visit(node.expression[0])
          #print(left.type)
          operator = node.expression[1]
          right = self.visit(node.expression[2])
          #print(right.type)
          if not isinstance(left, VariableSymbol) or not isinstance(right, VariableSymbol):
            pass
          if operator.operator in {'+', '-', '*', '/', '%'}:
              if left.type !='int' or right.type!='int':
                raise Exception(f"Operands of arithmetic operator '{operator}' must be of type 'int'")
            # Assign the result type of the arithmetic expression as 'int'
              return VariableSymbol(None, 'int')

          elif operator in {'==', '!=', '<', '<=', '>', '>='}:
              if left.type != right.type:
               raise Exception(f"Operands of comparison operator '{operator}' must have the same type")
            # Assign the result type of the comparison expression as 'bool'
              return VariableSymbol(None, 'bool')

          elif operator in {'and', 'or', 'not'}:
              if left.type != 'bool' or right.type != 'bool':
                raise Exception(f"Operands of boolean operator '{operator}' must be of type 'bool'")
            # Assign the result type of the boolean expression as 'bool'
              return VariableSymbol(None, 'bool')
          elif operator in {'++', '--'}:
            pass
          
        else:
        
         if isinstance(node.expression, Id):
            return self.visit_Id(node.expression)
         elif isinstance(node.expression, Number):
            return self.visit_Number(node.expression)
         elif isinstance(node.expression, String):
            return self.visit_String(node.expression)
         elif isinstance(node.expression, BinaryOperator):
            return self.visit_BinaryOperator(node.expression)
         else :
           return self.visit(node.expression)
    def visit_tuple(self, node):
      # Handle logic for visiting tuple nodes
      # For example, you can recursively visit each element of the tuple
      for element in node:
          self.visit(element)
    def visit_NoneType(self, node):
      pass
    def visit_Factor(self, node):
      if isinstance(node, tuple):
          # Handle tuple nodes separately
          factor_type = node[0]
          if factor_type == 'identifier':
              symbol = self.symbol_table.lookup(node[1])
              if symbol is None:
                  raise Exception(f"Variable '{node[1]}' not declared")
              return symbol
          elif factor_type == 'number':
              return VariableSymbol(None, 'int')
          elif factor_type == 'string':
              return VariableSymbol(None, 'str')
          elif factor_type == 'true' or factor_type == 'false':
              return VariableSymbol(None, 'bool')
      else:
          # Handle single nodes
          if isinstance(node, Id):
              return self.visit_Id(node)
          elif isinstance(node, Number):
              return self.visit_Number(node)
          elif isinstance(node, String):
              return self.visit_String(node)
          elif isinstance(node, Bool):
              return self.visit_bool(node)
    def visit_str(self, node):
      # Handle logic for visiting string nodes
      # For example, you can validate the string or perform any necessary checks
      # In this example, we'll simply return 'str' as the type of the string node
      return VariableSymbol(None, 'str')


    def visit_Condition(self, node):
        left_type = self.visit(node.left).type
        right_type = self.visit(node.right).type

        if left_type != right_type:
            raise Exception("Type mismatch in condition: Left and right operands must have the same type")

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.if_statement)
        for condition, statement_list in node.elif_statement:
            self.visit(condition)
            self.visit(statement_list)
        if node.else_statement:
            self.visit(node.else_statement)

    def visit_WhileStatement(self, node):
        self.visit(node.condition)
        self.visit(node.statement_list)

    def visit_TryExcept(self, node):
        self.visit(node.try_block)
        self.visit(node.except_block)

    def visit_Print(self, node):
        self.visit(node.value)

    def visit_CompoundTypes(self, node):
        identifier=node.identifier
        self.symbol_table.add_symbol(identifier, VariableSymbol(identifier, type))

    def visit_CompoundTypeAccess(self, node):
      identifier = node.identifier
      compound_type_access = node.compound_type_access

      # Check if the compound type access is a string or another CompoundTypeAccess node
      if isinstance(compound_type_access, str):
          # Lookup the symbol in the symbol table
          compound_symbol = self.symbol_table.lookup(identifier)
          if compound_symbol is None:
              raise Exception(f"Compound type '{identifier}' not declared")
      elif isinstance(compound_type_access, CompoundTypeAccess):
          # Recursively visit the compound type access node
          self.visit_CompoundTypeAccess(compound_type_access)


parser = yacc.yacc()

try:
    text = open("test_cases/test0.zeva", "r").read()
    ast = parser.parse(text)
    pprint(ast)

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(ast)
except EOFError:
    print("File could not be opened!")
