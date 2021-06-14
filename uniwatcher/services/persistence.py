import json
import os

from ..models import UniwatcherState


class JsonStorage:
    def __init__(self, config, log):
        self.config = config
        self.log = log
        log.info('Created storage manager.')

    def save(self, state):
        self.log.info('Saving application state ...')
        with open(self.config.filename, 'w') as f:
            f.write(
                json.dumps(state,
                           default=lambda o: o.__dict__,
                           sort_keys=True,
                           indent=4))
        self.log.info('Saved %s tokens.', len(state.tokens))

    def load(self):
        self.log.info('Loading application state ...')
        if not os.path.isfile(self.config.filename):
            self.log.warning('Database does not exist, using empty state.')
            return UniwatcherState()
        with open(self.config.filename, 'r') as f:
            state = UniwatcherState(json.loads(f.read()))
        active_token_count = len(
            list(
                filter(lambda token: not token.expired_at,
                       state.tokens.values())))
        self.log.info('Loaded %s tokens (%s active).', len(state.tokens),
                      active_token_count)
        return state
