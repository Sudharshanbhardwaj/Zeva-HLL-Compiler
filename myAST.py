from dataclasses import dataclass
from typing import Any, List, Tuple, Union

class Node:
    pass

@dataclass
class Number(Node):
    value: int

@dataclass
class String(Node):
    value: str

@dataclass
class Id(Node):
    id: str 
    def __hash__(self):
      return hash(self.id)
    
@dataclass
class Bool(Node):
    value: bool

@dataclass
class Start:
    statement_list: List[Any]

@dataclass
class StatementList:
    statements: List[Tuple[str, Any]]

@dataclass
class Declaration:
    type: str
    
    identifier: Id
    assignment_operator: str
    value: Any
    def __post__init__(self):
      if self.type == "int" and not isinstance(self.value, Number):
          raise TypeError("Expected value of type Number for integer declaration")
      elif self.type == "str" and not isinstance(self.value, String):
          raise TypeError("Expected value of type String for string declaration")
      


@dataclass
class Assignment:
    identifier: Id
    assignment_operator: str
    value: Any

@dataclass
class CompoundTypes:
    compound_type: str
    identifier: str
    assignment_operator: str
    data: Tuple[Any]

@dataclass
class CompoundTypeAccess:
    
    identifier: str
    compound_type_access: Union[str, Tuple[str, Any], None]

    def __hash__(self):
        return hash((self.identifier, self.compound_type_access))


@dataclass
class FunctionDefinition:
    type : str
    identifier: str
    parameter_list: Union[Tuple[Tuple[str, str], Any], None]
    statement_list: List[Any]
    return_data: Any

@dataclass
class FunctionCall:
  
    identifier: str
    expression: Union[Tuple[Tuple[str, str], Any], None]

@dataclass
class ContainerAccess:
    identifier :str
    index: Any

@dataclass
class ParameterList:
    parameters: Tuple[Tuple[str, str], Any]

@dataclass
class OptionalParameterList:
    parameters: Union[Tuple[List[Tuple[str, Tuple[str, str]]], Any], None]

@dataclass
class Condition:
    left: Any
    comparison_operator: str
    right: Any

@dataclass
class IfStatement:
    condition: Any
    if_statement: List[Any]
    elif_statement: List[Tuple[Any, List[Any]]]
    else_statement: Union[List[Any]]

@dataclass
class WhileStatement:
    condition: Any
    statement_list: List[Any]

@dataclass
class Pexpression:
    value: List[Any]

@dataclass
class Expression:
    expression: Union[Tuple[Any, str, Any]]

    def __eq__(self, other):
      if isinstance(other, Expression):
          return self.expression == other.expression
      return False

    def __hash__(self):
      return hash(self.expression)
@dataclass
class BinaryOperator:
    operator: str

@dataclass
class Term:
    term: Union[Any, Tuple[Any, str]]

@dataclass
class UnaryOperator:
    operator: str

@dataclass
class Factor:
    factor: Union[str, int, Tuple[str, Any]]

@dataclass
class TryExcept:
    try_block: List[Any]
    except_block: List[Any]

@dataclass
class Print:
    value: Any

@dataclass
class Data:
    expressions: Tuple[Any]
