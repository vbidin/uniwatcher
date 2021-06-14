class UniswapToken:
    def __init__(self,
                 address,
                 name=None,
                 symbol=None,
                 liquidity=None,
                 created_at=None,
                 notified_at=None,
                 expired_at=None):
        self.address = address
        self.name = name
        self.symbol = symbol
        self.liquidity = liquidity
        self.created_at = created_at
        self.notified_at = notified_at
        self.expired_at = expired_at

    def __str__(self):
        if self.name and self.symbol:
            name = f'{self.name} ({self.symbol})'
        elif self.name:
            name = self.name
        else:
            name = self.address
        return name
