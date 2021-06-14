import logging


def start_logging(config):
    level = logging.INFO
    if config.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level,
                        format='%(asctime)s # %(levelname)s: %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler(config.filename, mode='w')
                        ])
    log = logging.getLogger()
    log.info('Created logger.')
    return log


def stop_logging():
    logging.shutdown()
