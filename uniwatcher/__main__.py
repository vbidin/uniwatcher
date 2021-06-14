from . import __version__

from .utility import parse_configuration, start_logging, stop_logging
from .services import UniwatcherWorkflow


def main():
    config = parse_configuration()
    log = start_logging(config.logging)
    try:
        workflow = UniwatcherWorkflow(__version__, config, log)
        workflow.start()
    except KeyboardInterrupt:
        log.warning('Uniwatcher interrupted.')
    except:
        log.exception('Uniwatcher crashed!')
    finally:
        if 'workflow' in locals():
            workflow.stop()
        stop_logging()


if __name__ == '__main__':
    main()
