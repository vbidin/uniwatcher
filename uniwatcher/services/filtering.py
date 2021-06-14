from ..utility import now


class UniswapTokenFilter:
    def __init__(self, config, log):
        self.config = config
        self.log = log
        log.info('Created token filter.')

    def check(self, tokens):
        interesting_tokens, expired_tokens = [], []
        for token in tokens.values():
            if token.expired_at:
                continue
            if token.name:
                name = token.name.lower()
                added = False
                for keyword in self.config.keywords:
                    if keyword in name:
                        interesting_tokens.append(token)
                        added = True
                        break
                if added:
                    continue
            if token.liquidity is not None and \
               token.liquidity >= self.config.liquidity:
                interesting_tokens.append(token)
                continue
            if now() - token.created_at >= self.config.age:
                expired_tokens.append(token)
                continue
        return interesting_tokens, expired_tokens
