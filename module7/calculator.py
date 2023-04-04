import sys
import logging.config
from dict_config import dict_config
logging.config.dictConfig(dict_config)

utils = logging.getLogger('utils')

info_to_file = logging.getLogger('utils.info_to_file')

app = logging.getLogger('app')

save_logs = logging.getLogger('app.save_logs')

from logging_tree import printout
console = sys.stdout
sys.stdout = open('logging_tree.txt', 'w')
printout()
sys.stdout = console

# formatter = logging.Formatter("%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s")

# app = logging.getLogger('app')
# handler_app = logging.StreamHandler(sys.stdout)
# handler_app.setFormatter(formatter)
# app.addHandler(handler_app)
# app.setLevel('INFO')
#
# utils = logging.getLogger('utils')
# handler_utils = logging.FileHandler('calc_debug.log')
# handler_utils.setFormatter(formatter)
# utils.addHandler(handler_utils)
# utils.setLevel('DEBUG')


def main(a: int, b: int):
    utils.error('Start summing')
    app.info(f"Sum: {a + b}")
    utils.error('Start minus')
    app.info(f"Minus: {a - b}")
    utils.error('Start multiplying')
    app.info(f"Multiple: {a * b}")
    utils.error('Start division')
    app.info(f"Division: {a / b}")


if __name__ == "__main__":
    save_logs.debug(f'start_calculating {sys.argv[1]} and {sys.argv[2]}')
    info_to_file.info('start_calculating')
    info_to_file.info('ÎŒØ∏‡°⁄·°€йцукен_ltail')
    utils.error('Start calculating')
    main(int(sys.argv[1]), int(sys.argv[2]))
    utils.error('End calculating')
    info_to_file.info('end_calculating')
