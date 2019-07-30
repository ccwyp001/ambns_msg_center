# -*- coding: utf-8 -*-

from .base import BaseDispatchClient
from . import api
from flask import current_app


class DispatchClient(BaseDispatchClient):
    API_BASE_URL = ''

    member = api.DispatchMember()
    dispatch = api.DispatchApi()
    ambulance = api.DispatchAmbulance()

    def __init__(self, timeout=None):
        super(DispatchClient, self).__init__(
            timeout
        )
        self.API_BASE_URL = current_app.config['EXT_PARSER_URL']