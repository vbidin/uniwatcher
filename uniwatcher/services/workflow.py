from .persistence import JsonStorage
from .discovery import EthereumClient
from .monitoring import UniswapSubgraphClient
from .filtering import UniswapTokenFilter
from .notification import PushoverClient
from .timing import Idler

from ..utility import now


class UniwatcherWorkflow:
    def __init__(self, version, config, log):
        self.version = version
        self.log = log

        log.info('Starting Uniwatcher v%s ...', version)
        self.storage = JsonStorage(config.storage, log)
        self.ethereum = EthereumClient(config.ethereum, log)
        self.uniswap = UniswapSubgraphClient(config.uniswap, log)
        self.filter = UniswapTokenFilter(config.filter, log)
        self.notifier = PushoverClient(config.pushover, log)
        self.idler = Idler(config.timestep, log)
        log.info('Finished Uniwatcher setup.')

    def start(self):
        self.log.info('Started Uniwatcher workflow!')
        self.state = self.storage.load()
        while True:
            self._step()

    def _step(self):
        start = now()

        # explore
        found_tokens, new_last_block = self.ethereum.poll(
            start=self.state.last_block)
        new_ids = []
        for address in found_tokens:
            if address not in self.state.tokens:
                self.state.tokens[address] = found_tokens[address]
                new_ids.append(address)
        if new_ids:
            self.log.info('Found %s new tokens: %s', len(new_ids),
                          ', '.join(new_ids))
        self.state.last_block = new_last_block

        # update
        self.uniswap.update(self.state.tokens)

        # filter
        interesting_tokens, expired_tokens = self.filter.check(
            self.state.tokens)

        # notify
        self.notifier.notify(interesting_tokens)

        # prune
        old_tokens = interesting_tokens + expired_tokens
        for token in old_tokens:
            token.expired_at = now()
        if expired_tokens:
            expired_names = list(
                map(lambda token: token.name or 'N/A', expired_tokens))
            self.log.info('Removed %s expired tokens: %s', len(expired_names),
                          ', '.join(expired_names))

        # wait
        end = now()
        duration = end - start
        self.idler.idle(duration)

    def stop(self):
        if hasattr(self, 'state'):
            self.storage.save(self.state)
        self.log.info('Stopped Uniwatcher workflow!')
