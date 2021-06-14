from pushover import Client

from ..utility import now


class PushoverClient:
    def __init__(self, config, log):
        self.config = config
        self.log = log
        self.client = Client(self.config.user_key,
                             api_token=self.config.api_key)
        log.info('Created Pushover client.')

    def notify(self, tokens):
        for token in tokens:
            url = '{}/token/{}'.format(self.config.url, token.address)
            if token.name and token.symbol:
                title = '{} ({})'.format(token.name, token.symbol)
            elif token.name and not token.symbol:
                title = token.name
            else:
                title = 'Unknown token'
            if token.liquidity:
                liquidity = '${:,}'.format(int(token.liquidity))
            else:
                liquidity = 'N/A'
            messages = ['Current liquidity: {}'.format(liquidity)]
            self.client.send_message(title=title,
                                     message='\n'.join(messages),
                                     device=self.config.device,
                                     url=url,
                                     url_title='Uniswap',
                                     sound='cashregister')
            token.notified_at = now()
        if tokens:
            names = list(map(lambda token: token.name or 'N/A', tokens))
            self.log.info('Notified clients about %s tokens: %s', len(names),
                          ', '.join(names))
