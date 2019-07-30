# -*- coding: utf-8 -*-

from .base import BaseProParser
from . import api
from flask import current_app


class ProParser(BaseProParser):
    API_BASE_GUID = ''

    zit_mis_sys = api.ZIT_MIS_SYS_PKG()
    zit_statistics = api.ZIT_MIS_STATISTICS_PKG()

    def __init__(self, timeout=None):
        super(ProParser, self).__init__(
            timeout
        )
        self.API_BASE_GUID = (
            'ORCL',
            current_app.config['PROCEDURE_HOST']['ip'],
            current_app.config['PROCEDURE_HOST']['port'],
            current_app.config['PROCEDURE_HOST']['instance'],
            current_app.config['PROCEDURE_HOST']['user'],
            current_app.config['PROCEDURE_HOST']['pswd'],
        )
