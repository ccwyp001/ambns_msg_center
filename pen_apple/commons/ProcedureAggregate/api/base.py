# -*- coding: utf-8 -*-

class BaseProApi(object):

    def __init__(self, parser=None):
        self._parser = parser

    def _call_proc(self, name, **kwargs):
        if getattr(self, 'API_BASE_GUID', None):
            kwargs['api_base_guid'] = self.API_BASE_GUID
        if getattr(self, 'PKG_NAME', None):
            kwargs['pkg_name'] = self.PKG_NAME
        return self._parser.call_proc(name, **kwargs)