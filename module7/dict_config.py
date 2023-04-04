import logging
import json
import re


class AsciiFilter(logging.Filter):

    def __init__(self, param):
        self.param = param

    def filter(self, record):
        if self.param is None:
            allow = True
        else:
            allow = self.param not in record.msg
        if allow:
            if record.msg.isascii:
                record.msg = re.sub(r'[^\x00-\x7F]+', ' ', record.msg)
            else:
                pass
        return allow


dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'ascii_filter': {
            '()': AsciiFilter,
            'param': 'noshow'
        },
    },
    'formatters': {
        'base': {
            'format': "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
        },
        'json_dumps': {
            'format': json.dumps({
                'script_name': 'calculator',
                'level': '%(levelname)s',
                'name': '%(name)s',
                'time': '%(asctime)s',
                'lineno': '%(lineno)d',
                'message': '%(message)s'
            })
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'base',
            'filters': ['ascii_filter'],
        },
        'error_to_file': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'base',
            'filters': ['ascii_filter'],
            'filename': 'calc_error.log',
            'mode': 'a'
        },
        'debug_to_file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'base',
            'filters': ['ascii_filter'],
            'filename': 'calc_debug.log',
            'mode': 'a'
        },
        'rotate_by_time': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'filters': ['ascii_filter'],
            'formatter': 'base',
            'filename': 'utils.log',
            'when': 'h',
            'interval': 1,
            'backupCount': 5,
        },
        'send_logs': {
            'class': 'logging.handlers.HTTPHandler',
            'level': 'DEBUG',
            'host': '127.0.0.1:5000',
            'url': '/save_log',
            'formatter': 'json_dumps',
            'method': 'POST',
        }
    },
    'loggers': {
        "module_logger": {
            'level': 'DEBUG',
            'handlers': ['error_to_file', 'debug_to_file', 'console']
        },
        "utils": {
            'level': 'ERROR',
            'handlers': ['error_to_file', 'console'],
            'propagate': True,
        },
        "app": {
            'level': 'INFO',
            'handlers': ['debug_to_file', 'console'],
            'propagate': True,
        },
        'utils.info_to_file': {
            'level': 'INFO',
            'handlers': ['rotate_by_time'],
            'propagate': True,
        },
        'app.save_logs': {
            'level': 'DEBUG',
            'handlers': ['send_logs'],
            'propagate': True,
        }
    },
}