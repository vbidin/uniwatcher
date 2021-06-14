import time


class Idler:
    def __init__(self, timestep, log):
        self.timestep = timestep
        self.log = log
        log.info('Created idler.')

    def idle(self, duration):
        if self.timestep == 0:
            return

        remaining = self.timestep - duration
        if remaining > 0:
            self.log.info('Idling for %s seconds...', remaining)
            time.sleep(remaining)
        else:
            self.log.warning('Step execution took %s seconds (max is %s).',
                             duration, self.timestep)
