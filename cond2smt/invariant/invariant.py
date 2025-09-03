from typing import Union

from . import declare

class Assert:
    def __init__(self, expr: Union['UnaryOp', 'BinaryOp', declare.DeclareFun]):
        self.expr = expr

    def __str__(self):
        return f'(assert {self.expr})'
        
class UnaryOp:
    def __init__(self, op: str, operand: Union['UnaryOp', 'BinaryOp', declare.DeclareFun]):
        if op == '!':
            self.op = 'not'
        else:
            self.op = op
        self.operand = operand

    def __str__(self):
        return f'({self.op} {self.operand})'
        
class BinaryOp:
    def __init__(self, op: str, left: Union[UnaryOp, 'BinaryOp', declare.DeclareFun, str], right: Union[UnaryOp, 'BinaryOp', declare.DeclareFun, str]):
        if op == '&&':
            self.op = 'and'
        elif op == '||':
            self.op = 'or'
        elif op == '==':
            self.op = '='
        elif op == '!=':
            self.op = 'distinct'
        else:
            self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f'({self.op} {self.left} {self.right})'