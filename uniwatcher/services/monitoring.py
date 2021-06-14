from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class UniswapSubgraphClient:

    eth_query = gql('''
        {
            bundle(id: "1" ) {
                ethPrice
            }
        }
        ''')

    token_query = gql('''
        query($ids: [ID!]!) {
            tokens(where: { id_in: $ids }) {
                id
                name
                symbol
                totalLiquidity
                derivedETH
            }
        }
        ''')

    def __init__(self, config, log):
        transport = AIOHTTPTransport(url=config.url)
        self.client = Client(transport=transport,
                             fetch_schema_from_transport=True)
        log.info('Created Uniswap Subgraph client.')
        self.log = log

    def update(self, tokens, step=100):
        ids = self._get_ids(tokens.values())
        if not ids:
            self.log.warning('Ignoring token update, no active tokens found.')
            return
        price_of_eth = self._fetch_eth_price()
        self.log.info('Fetching data for %s tokens ...', len(ids))
        for start in range(0, len(ids), step):
            end = min(start + step, len(ids))
            results = self._fetch_token_data(ids[start:end])
            self._update_tokens(tokens, results, price_of_eth)

    def _get_ids(self, tokens):
        return list(
            map(lambda token: token.address,
                filter(lambda token: not token.expired_at, tokens)))

    def _fetch_eth_price(self):
        result = self.client.execute(self.eth_query)
        return float(result['bundle']['ethPrice'])

    def _fetch_token_data(self, ids):
        params = {'ids': ids}
        result = self.client.execute(self.token_query, variable_values=params)
        self.log.debug('Received token data for %s tokens.',
                       len(result['tokens']))
        return result['tokens']

    def _update_tokens(self, tokens, results, price_of_eth):
        for result in results:
            token = tokens[result['id']]
            if not token.name:
                token.name = result['name']
            if not token.symbol:
                token.symbol = result['symbol']
            number_of_tokens = float(result['totalLiquidity'])
            eth_per_token = float(result['derivedETH'])
            token.liquidity = int(number_of_tokens * eth_per_token *
                                  price_of_eth)
