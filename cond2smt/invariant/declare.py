from typing import List, Tuple


class DeclareFun:
    def __init__(self, name: str, ret_type: str, params: List[Tuple[str, str]] = []):
        self.name = name
        self.ret_type = ret_type
        self.params = params

    def declare(self):
        param_str = ', '.join([f'{ptype} {pname}' for ptype, pname in self.params])
        return f'(declare-fun {self.name} ({param_str}) {self.ret_type})'
    
    def __str__(self):
        return self.name