"""
Definisi Node AST (Abstract Syntax Tree) untuk bahasa Core.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Any


class ASTNode:
    """Kelas dasar untuk semua simpul (node) dalam AST."""
    pass


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


@dataclass
class VarDecl(ASTNode):
    name: str
    value_expr: ASTNode
    line: int


@dataclass
class AssignStmt(ASTNode):
    name: str
    value_expr: ASTNode
    line: int


@dataclass
class PrintStmt(ASTNode):
    expressions: List[ASTNode]
    line: int


@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_branch: Block
    elif_branches: List[Tuple[ASTNode, Block]]
    else_branch: Optional[Block]
    line: int


@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: Block
    line: int


@dataclass
class ForRangeStmt(ASTNode):
    var_name: str
    start_expr: ASTNode
    end_expr: ASTNode
    body: Block
    line: int


@dataclass
class ForInStmt(ASTNode):
    var_name: str
    iterable_expr: ASTNode
    body: Block
    line: int


@dataclass
class ListAppendStmt(ASTNode):
    target_name: str
    item_expr: ASTNode
    line: int


@dataclass
class ListRemoveStmt(ASTNode):
    target_name: str
    index_expr: ASTNode
    line: int


@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[str]
    body: Block
    line: int


@dataclass
class ReturnStmt(ASTNode):
    expr: Optional[ASTNode]
    line: int


@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]
    line: int


@dataclass
class InputExpr(ASTNode):
    prompt_expr: Optional[ASTNode]
    line: int


@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode]
    line: int


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    line: int


@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode
    line: int


@dataclass
class Literal(ASTNode):
    value: Any
    line: int


@dataclass
class Variable(ASTNode):
    name: str
    line: int
