counter = 0
class node_stack:
    def __init__(self, symbol, terminal):
        global counter
        self.id = counter
        self.symbol = symbol
        self.is_terminal = terminal
        counter += 1

class node_parser:
    def __init__(self, symbol, lexeme = None, children = [], father = None, line = None):
        self.symbol = symbol
        self.lexeme = lexeme
        self.line = line
        self.children = children
        self.father = father
        self.type = None