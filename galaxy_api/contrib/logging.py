"""Logging utils."""

import logging

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


class RequestLogMiddleware:
    """Logs django requests."""

    LOGGER_NAME = "galaxy_api.request"
    META_FIELDS = [
        'HTTP_REFERRER',
        'HTTP_USER_AGENT',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
        'QUERY_STRING',
        'REMOTE_ADDR',
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(self.LOGGER_NAME)

    def __call__(self, request):
        args = {
            'method': request.method,
            'path': request.path,
            'full_path': request.get_full_path(),
            'client_addr': get_remote_ip(request),
        }

        for field in self.META_FIELDS:
            args[field.lower()] = request.META.get(field, '')

        response = self.get_response(request)

        args['status_code'] = response.status_code

        message = "{method} {path} {status_code}".format(**args)

        self.logger.info(message, extra=args)

        return response


def get_remote_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')
