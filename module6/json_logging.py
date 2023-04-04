import logging
import json


format_data = json.dumps(
    {
        "time": "%(asctime)s",
        "level": "%(levelname)s",
        "message": "%(message)s"
    }
)
logging.basicConfig(level=logging.INFO, filename="skillbox_json_messages.log", format=format_data)


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = msg.replace("\"", "\'")
        return msg, kwargs


logger = JsonAdapter(logger=logging.getLogger('json_logger'), extra=None)

logger.info("wel\"co\"me")
logger.info('"_"_"_"')

if __name__ == "__main__":
    pass