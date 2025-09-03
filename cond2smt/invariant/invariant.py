from typing import Union

from . import declare

class Assert:
    def __init__(self, expr: Union['UnaryOp', 'BinaryOp', declare.DeclareFun]):
        self.expr = expr

    def __str__(self):
        return f'(assert {self.expr})'
        
class UnaryOp:
    def __init__(self, op: str, operand: Union['UnaryOp', 'BinaryOp', declare.DeclareFun]):
        self.op = op
        self.operand = operand

    def __str__(self):
        return f'({self.op} {self.operand})'
        
class BinaryOp:
    def __init__(self, op: str, left: Union[UnaryOp, 'BinaryOp', declare.DeclareFun, str], right: Union[UnaryOp, 'BinaryOp', declare.DeclareFun, str]):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f'({self.op} {self.left} {self.right})'