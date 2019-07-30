from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import (
    APIException, ValidationError, ErrorDetail
)
from rest_framework.settings import api_settings

from galaxy_api.api.exceptions import exception_handler


def test_http_not_found():
    error = Http404()
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '404',
            'code': 'not_found',
            'title': 'Not found.',
        },
    ]


def test_http_permission_denied():
    error = PermissionDenied('Permission denied.')
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '403',
            'code': 'permission_denied',
            'title': 'You do not have permission to perform this action.',
        },
    ]


def test_api_exc_string():
    error = APIException()
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '500',
            'code': 'error',
            'title': 'A server error occurred.',
        },
    ]


def test_api_exc_string_w_message():
    error = APIException('Custom error message.')
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '500',
            'code': 'error',
            'title': 'A server error occurred.',
            'detail': 'Custom error message.'
        },
    ]


def test_api_exc_string_w_code():
    error = APIException(code='custom_code')
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '500',
            'code': 'custom_code',
            'title': 'A server error occurred.',
        },
    ]


def test_api_exc_list():
    error = APIException([
        'First error message.',
        'Second error message.',
    ])
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '500',
            'code': 'error',
            'title': 'A server error occurred.',
            'detail': 'First error message.',
        },
        {
            'status': '500',
            'code': 'error',
            'title': 'A server error occurred.',
            'detail': 'Second error message.',
        },
    ]


def test_validation_non_field_errors():
    error = ValidationError({
        api_settings.NON_FIELD_ERRORS_KEY: [
            'First error message.',
            'Second error message.',
        ]
    })
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '400',
            'code': 'invalid',
            'title': 'Invalid input.',
            'detail': 'First error message.',
        },
        {
            'status': '400',
            'code': 'invalid',
            'title': 'Invalid input.',
            'detail': 'Second error message.',
        },
    ]


def test_validation_field_errors():
    error = ValidationError({
        'name': ['Invalid name.'],
        'count': ['Invalid count.'],
    })
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '400',
            'code': 'invalid',
            'title': 'Invalid input.',
            'detail': 'Invalid name.',
            'source': {'parameter': 'name'},
        },
        {
            'status': '400',
            'code': 'invalid',
            'title': 'Invalid input.',
            'detail': 'Invalid count.',
            'source': {'parameter': 'count'},
        },
    ]


def test_validation_errors_complex():
    error = ValidationError({
        'foo': 'Foo error message.',
        'bar': [
            ErrorDetail('Bar conflict message.', code='conflict'),
            'Second bar message.'
        ],
        api_settings.NON_FIELD_ERRORS_KEY: ['Non field error message.'],

    })
    response = exception_handler(error, None)
    errors = response.data['errors']
    assert errors == [
        {
            'status': '400',
            'code': 'invalid',
            'title': 'Invalid input.',
            'detail': 'Foo error message.',
            'source': {'parameter': 'foo'},
        },
        {
            'status': '400',
            'code': 'conflict',
            'title': 'Invalid input.',
            'detail': 'Bar conflict message.',
            'source': {'parameter': 'bar'},
        },
        {
            'status': '400',
            'code': 'invalid',
            'title': 'Invalid input.',
            'detail': 'Second bar message.',
            'source': {'parameter': 'bar'},
        },
        {
            'status': '400',
            'code': 'invalid',
            'title': 'Invalid input.',
            'detail': 'Non field error message.',
        },
    ]
