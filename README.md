# Huey Prometheus Exporter
This project provides metrics about huey to prometheus

Latest Version: **0.0.1**

## Usage

#### Installation
Installation of the latest release:
```
pip install git+https://github.com/MarcoGlauser/huey-exporter.git@0.0.1
```
Installation of the master branch:
```
pip install git+https://github.com/MarcoGlauser/huey-exporter.git@master
```

The command `huey_exporter` will start a webserver (default port 9100) and serves the metrics.

#### Running
```
Usage: huey_exporter [OPTIONS]

Options:
  -c, --connection-string TEXT  Connection string to redis including database.
                                for example redis://localhost:6379/0
  -q, --queue-name TEXT         Name of the queue to monitor  [required]
  -p, --port TEXT               Port to expose the metrics on
  --help                        Show this message and exit.

```

Example:
```
huey_exporter -q test
```
The huey_exporter can also be configured by the environment variables `REDIS_CONNECTION_STRING`, `QUEUE_NAME` and `EXPORTER_PORT`
### Docker
[Image on dockerhub](https://hub.docker.com/r/mglauser/huey-exporter/)

The usage is the same as the non-docker.

Example:
```
docker run -e REDIS_CONNECTION_STRING=redis://somehost:6379/0 -e QUEUE_NAME=test mglauser/huey-exporter
```

## Exposed Metrics
All metrics have the labels *task name* and *queue name* attached.
#### huey_enqueued_tasks
Counter
#### huey_started_tasks
Counter

#### huey_finished_tasks
Counter

#### huey_error_tasks
Counter

#### huey_task_duration_seconds
Summary

### Example
Tasks started per Minute:
```
sum by (queue_name) (increase(huey_started_tasks[1m]))
```

Task Queue Length:
```
sum by (queue_name) (huey_enqueued_tasks - huey_started_tasks)
```

Average Task duration:
```
rate(huey_task_duration_seconds_sum[5m])/rate(huey_task_duration_seconds_count[5m])
```