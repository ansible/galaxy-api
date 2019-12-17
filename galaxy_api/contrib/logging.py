"""Logging utils."""

import boto3
import watchtower
import logstash_formatter
import request_id.logging
from django.conf import settings


class CloudWatchHandler(watchtower.CloudWatchLogHandler):
    """Pre-configured CloudWatch handler."""

    def __init__(self):
        config = settings.CLOUD_WATCH_LOGGER
        boto3_session = boto3.Session(
            aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'],
            region_name=config['AWS_REGION_NAME'],
        )
        super().__init__(
            boto3_session=boto3_session,
            log_group=config['LOGGING_GROUP'],
            stream_name=config['LOGGING_STREAM_NAME'],
        )
        self.addFilter(request_id.logging.RequestIdFilter())
        self.setFormatter(logstash_formatter.LogstashFormatterV1())
