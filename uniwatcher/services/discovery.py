import time

from web3 import Web3, WebsocketProvider
from web3.exceptions import BlockNotFound

from ..models import UniswapToken


class EthereumClient:
    def __init__(self, config, log):
        provider = WebsocketProvider(config.url,
                                     websocket_timeout=config.timeout)
        self.client = Web3(provider)
        if not self.client.isConnected():
            raise Exception('Failed to create Ethereum client.')
        self.contract = self.client.eth.contract(config.address,
                                                 abi=config.abi)
        log.info('Created Ethereum client.')
        self.log = log

    def poll(self, start=0, end='latest', step=1000):
        if end == 'latest':
            end = self.client.eth.getBlock(end).number
            self.log.debug('Latest block set to: %s', end)
        if start == end:
            self.log.warning('Ignoring poll: no new blocks to explore.')
            return set(), end
        if start > end:
            self.log.error('Starting block %s is greater than'\
                           'ending block %s.', start, end)
            return set(), end

        self.log.info('Exploring %s new blocks ...', end - start)
        all_tokens = dict()
        for index in range(start, end, step):
            entries = self._get_entries(index, min(index + step, end))
            tokens = self._get_tokens(entries)
            for address in tokens:
                if address not in all_tokens:
                    all_tokens[address] = tokens[address]
        self.log.debug('Found a total of %s unique tokens.', len(all_tokens))
        return all_tokens, end

    def _get_entries(self, start, end):
        self.log.debug('Searching for liquidity pairs between blocks'\
                       '%s and %s.', start, end)
        entries = self.contract.events.PairCreated.getLogs(fromBlock=start,
                                                           toBlock=end)
        self.log.debug('Found %s liquidity pairs.', len(entries))
        return entries

    def _get_tokens(self, entries):
        self.log.debug('Converting %s entries into tokens.', len(entries))
        tokens = dict()
        for entry in entries:
            block = self._get_block(entry['blockNumber'])
            addresses = [
                entry['args']['token0'].lower(),
                entry['args']['token1'].lower()
            ]
            for address in addresses:
                if address not in tokens:
                    tokens[address] = UniswapToken(address=address,
                                                   created_at=block.timestamp)
        self.log.debug('Found %s unique token addresses.', len(tokens))
        return tokens

    def _get_block(self, number, attempts=2, delay=10):
        for _ in range(attempts):
            try:
                return self.client.eth.getBlock(number)
            except BlockNotFound as e:
                self.log.error(str(e))
                time.sleep(delay)
