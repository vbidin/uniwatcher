from .token import UniswapToken


class UniwatcherState:
    def __init__(self, data=None):
        self.tokens = dict()
        if data is None:
            self.last_block = 0
            return
        self.last_block = data['last_block']
        for key, values in data['tokens'].items():
            self.tokens[key] = UniswapToken(**values)
