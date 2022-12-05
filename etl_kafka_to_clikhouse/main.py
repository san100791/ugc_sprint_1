import time

from src.kafka_reader import KafkaReader
from core.config import clickhouse_conf, kafka_conf
from src.clickhouse_writer import ClickHouseWriter
from core.log_writer import logger


def main():
    kafka = KafkaReader(kafka_conf)
    clickhouse = ClickHouseWriter(clickhouse_conf)
    messages = []
    start = time.time()
    for message in kafka.read_data():
        messages.append(message)
        if time.time() - start > clickhouse_conf.wait_time:
            clickhouse.write_messages(messages)
            logger.debug('%s rows inserted', len(messages))
            messages = []
            start = time.time()


if __name__ == '__main__':
    main()
