# -*- coding: utf-8 -*-

from flask import current_app
from spyne.protocol.soap import Soap11, Soap12
from spyne.protocol.json import JsonDocument
from spyne.model.primitive import Unicode, Integer, String
from spyne.model.complex import Iterable
from ...extensions import spyne
from suds.client import Client
from ...tasks import send_phone_call
import re


class SmsWebService(spyne.Service):
    __target_namespace__ = 'http://tempuri.org/'
    __service_url_path__ = '/msg/SmsWebService.asmx'
    __in_protocol__ = Soap11()
    __out_protocol__ = Soap11()

    # for c# soap client:
    # need patch in spyne/interface/wsdl/wsdl11.py:326 change message name to 'parameters'
    @spyne.srpc(Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def SendMessage(strLsh, strPhone, strNR, strPartID=''):
        strPhone = deal_phone_num(strPhone)
        strNR = re.sub(r'[0-9]{8,}', deal_context, strNR, count=1)
        sms_url = current_app.config['SMS_SOAP_URL']
        client = Client(sms_url)
        result = client.service.SendMessage(strLsh, strPhone, strNR, strPartID)
        send_phone_call.delay(strLsh, strPhone, strNR, strPartID)
        return result


def deal_phone_num(str_num):
    num = str(str_num)
    if num.startswith('01') and not num.startswith('010'):
        return num[1:]
    return num

def deal_context(matched):
    num = str(matched.group(0))
    if num.startswith('01') and not num.startswith('010'):
        return num[1:]
    return num