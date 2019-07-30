# -*- coding: utf-8 -*-

from flask import current_app
from spyne.protocol.soap import Soap11, Soap12
from spyne.protocol.json import JsonDocument
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from ...extensions import spyne
from suds.client import Client
from ...tasks import send_phone_call

CustomUnicode = Unicode.customize(nullable=False, max_occurs="1")

class SmsWebService(spyne.Service):
    __service_url_path__ = '/msg/SmsWebService.asmx'
    __in_protocol__ = Soap12()
    __out_protocol__ = Soap12()

    @spyne.srpc(CustomUnicode, CustomUnicode, CustomUnicode, CustomUnicode, _returns=CustomUnicode)
    def SendMessage(strLsh, strPhone, strNR, strPartID=''):
        sms_url = current_app.config['SMS_SOAP_URL']
        client = Client(sms_url)
        result = client.service.SendMessage(strLsh, strPhone, strNR, strPartID)
        send_phone_call.delay(strLsh, strPhone, strNR, strPartID)
        return result
