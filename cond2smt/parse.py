from enum import Enum
from typing import Dict, List
import tree_sitter

from . import languages, invariant

class Parser:
    class Language(Enum):
        C = 'c'
        CPP = 'cpp'
        JAVA = 'java'
        PYTHON = 'python'

    def __init__(self, language: 'Parser.Language', identifier_type: Dict[str, str] = dict()):
        self.language = tree_sitter.Language(getattr(languages, f'{language.value.upper()}_LANGUAGE'),Parser.Language.C.value)
        self.parser = tree_sitter.Parser()
        self.parser.set_language(self.language)
        self.identifier_type:Dict[str, invariant.DeclareFun] = dict()
        for identifier, id_type in identifier_type.items():
            if id_type not in ['Int', 'Bool', 'Real']:
                raise ValueError(f'Unsupported identifier type: {id_type}')
            self.identifier_type[identifier] = invariant.DeclareFun(identifier, id_type)

    def parse_ast(self, code: str):
        return self.parser.parse(bytes(code, "utf8")).root_node
    
    def _gen_inv(self, node: tree_sitter.Node):
        if node.type in ('translation_unit', 'expression_statement', 'parenthesized_expression'):
            return self._gen_inv(node.named_children[0])
        elif node.type == 'binary_expression':
            left = self._gen_inv(node.child_by_field_name('left'))
            op = node.value
            right = self._gen_inv(node.child_by_field_name('right'))
            return invariant.BinaryOp(op, left, right)
        elif node.type == 'unary_expression':
            op = node.value
            operand = self._gen_inv(node.child_by_field_name('argument'))
            return invariant.UnaryOp(op, operand)
        elif node.type == 'identifier':
            if node.value not in self.identifier_type:
                self.identifier_type[node.value] = invariant.DeclareFun(node.value, 'Int')
            return self.identifier_type[node.value]
        elif node.type == 'number_literal':
            return node.value
        else:
            raise ValueError(f'Unsupported node type: {node.type}')
            
    def generate_invariant(self, code: str) -> str:
        smt_code = '(set-logic QF_NIA)\n\n'

        root = self.parse_ast(code)
        expr = self._gen_inv(root)
        assertion = invariant.Assert(expr)

        for declare in self.identifier_type.values():
            smt_code += declare.declare() + '\n'
        smt_code += f'\n{assertion}\n(check-sat)\n(get-model)\n'
        return smt_code
        
