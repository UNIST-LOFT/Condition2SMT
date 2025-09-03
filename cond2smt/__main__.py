from .parse import Parser

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='cond2smt',description='Convert a condition to SMT-LIB format.')
    parser.add_argument('language', choices=['c'], help='Programming language of the input condition.')
    parser.add_argument('condition', help='The condition to be converted.')
    parser.add_argument('-i','--identifiers', nargs='*', help='List of identifier:type pairs, e.g., x:Int y:Bool z:Real')

    args = parser.parse_args()

    identifier_type = {}
    for item in args.identifiers:
        if ':' not in item:
            raise ValueError(f'Invalid identifier:type pair: {item}')
        identifier, id_type = item.split(':', 1)
        identifier_type[identifier] = id_type

    language = None
    if args.language == 'c':
        language = Parser.Language.C
    parser = Parser(Parser.Language(language), identifier_type)
    code:str = args.condition
    if not code.startswith('('):
        code = f'({code})'
    if not code.endswith(';'):
        code = f'{code};'
    smt_code = parser.generate_invariant(code)
    print(smt_code)