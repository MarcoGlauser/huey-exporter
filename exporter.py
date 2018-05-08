import click
import redis
from prometheus_client import start_http_server

from EventQueue import EventQueue


@click.command()
@click.option('--connection-string', '-c',
              default='redis://localhost:6379',
              help='Connection string to redis including database. for example redis://localhost:6379/0'
              )
@click.option('--queue_name', '-q', required=True, help='Name of the queue to monitor')
def run_exporter(connection_string, queue_name):
    # Start up the server to expose the metrics.
    start_http_server(9100)
    connection_pool = redis.BlockingConnectionPool.from_url(
            connection_string,
            max_connections=5,
            timeout=10
    )
    queue = EventQueue(queue_name, connection_pool)
    queue.listen()


if __name__ == '__main__':
    run_exporter()
