# -*- coding: utf-8 -*-

from .api.base import BaseProApi
import inspect
import json
import requests
import logging
import xmltodict
import six
from ...extensions import mc
logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseProApi)


def to_text(value, encoding='utf-8'):
    """Convert value to unicode, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


class BaseProParser(object):
    API_BASE_GUID = ''

    def __new__(cls, *args, **kwargs):
        self = super(BaseProParser, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, timeout=None):
        self.timeout = timeout

    def call_proc(self, pro_name, **kwargs):
        api_base_guid = kwargs.pop('api_base_guid', self.API_BASE_GUID)
        pkg_name = kwargs.pop('pkg_name', '')
        if pkg_name:
            pro_full_name = '{pkg}.{pro}'.format(
                pkg=pkg_name,
                pro=pro_name
            )
        else:
            pro_full_name = pro_name

        if 'in_args' not in kwargs:
            kwargs['in_args'] = []
        if 'out_args' not in kwargs:
            kwargs['out_args'] = []

        with mc.pool.acquire(api_base_guid) as conn:
            _ = conn.call_procedure(pro_full_name, **kwargs)
        return _


    _call_proc = call_proc

