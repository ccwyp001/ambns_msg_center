# -*- coding: utf-8 -*-

from .api.base import BaseDispatchApi
import inspect
import json
import requests
import logging
import xmltodict
import six

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseDispatchApi)


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


class BaseDispatchClient(object):
    API_BASE_URL = ''

    def __new__(cls, *args, **kwargs):
        self = super(BaseDispatchClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, timeout=None):
        self.timeout = timeout

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}

        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            return
            # raise WeChatClientException(
            #     errcode=None,
            #     errmsg=None,
            #     client=self,
            #     request=reqe.request,
            #     response=reqe.response
            # )

        return self._handle_result(
            res, method, url, result_processor, **kwargs
        )

    def _decode_result(self, res):
        try:
            xml = res.content
            result = xmltodict.parse(to_text(xml))['string']["#text"]
            result = json.loads(result, strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            logger.debug('Can not decode response as JSON', exc_info=True)
            return res
        return result

    def _handle_result(self, res, method=None, url=None,
                       result_processor=None, **kwargs):
        if not isinstance(res, dict):
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result


        if 'errcode' in result and result['isSucceed'] != True:
            errcode = result['errcode']
            errmsg = result.get('msg', errcode)
            raise Exception

        return result['resultData'] if not result_processor else result_processor(result)

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    _get = get

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    _post = post
