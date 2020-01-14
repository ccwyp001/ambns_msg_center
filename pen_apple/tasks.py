# -*- coding: utf-8 -*-
import os
import json
import time
import uuid

import requests
from suds.client import Client
from flask import current_app
from .extensions import celery, db
from .models import TtsHistory
from hashlib import md5
from .commons.ExtParser import DispatchClient


def encrypt(t1, t2, t3):
    """

    :param t1: password
    :param t2: userCode
    :param t3: timestamp
    """
    md = md5()
    md.update(t1.encode())
    p1 = md.hexdigest()
    text2 = str(t2) + str(p1)
    md = md5()
    md.update(text2.encode())
    p2 = md.hexdigest()
    text3 = str(p2) + str(t3)
    md = md5()
    md.update(text3.encode())
    p3 = md.hexdigest()
    return p3


def phone_call_filter(lsh, phone, note):
    """

    :rtype : object
    """
    note = str(note)
    driver_no_need = current_app.config['TTS_DRIVER_NO_NEED']
    sj_list = []
    if driver_no_need:
        client = DispatchClient(timeout=10)
        result = client.ambulance.ambulance_info_by_lsh(lsh)
        sj_list = [_.get('SJ', 0).split('H')[1] for _ in result]
    filter = {
        note.startswith('您有新的急救任务'),
        phone not in sj_list,
    }
    if all(filter):
        return True


@celery.task
def send_phone_call(lsh, phone, note, strPartID):
    if not phone_call_filter(lsh, phone, note):
        print('no need to send phone call')
        return True

    url = current_app.config['TTS_SOAP_URL']
    user_code = current_app.config['TTS_USER_CODE']
    pwd = current_app.config['TTS_PWD']
    timestamp = int(time.time())
    voice_type = current_app.config['TTS_VOICE_TYPE']
    call_number = current_app.config['TTS_CALL_NUMBER']
    retry_num = current_app.config['TTS_RETRY_NUM']
    retry_interval = current_app.config['TTS_RETRY_INTERVAL']

    recv_number = [phone]
    recv_message = [note]

    try:
        client = Client(url)
        recvNumberArray = client.factory.create('ArrayOfString')
        recvNumberArray.string = recv_number
        recvMessageArray = client.factory.create('ArrayOfString')
        recvMessageArray.string = recv_message

        SelfTaskArg = [user_code, encrypt(pwd, user_code, timestamp), timestamp,
                       voice_type, call_number, recvNumberArray, recvMessageArray, retry_num,
                       retry_interval
                       ]
        response = client.service.CreateSelfTask(*SelfTaskArg)
        send_status = response.Success
        result_id = response.Result
    except Exception as e:
        print('post soap url error %s' % e)
        send_status = 0
        result_id = 0
    tts = TtsHistory.new(lsh, phone, note, send_status, result_id)
    try:
        db.session.add(tts)
        db.session.commit()
        if send_status:
            phone_result.apply_async(
                (tts.id,),
                countdown=30)
    except Exception as e:
        print('add data error %s' % e)
        db.session.rollback()

    if 'db' in locals():
        db.session.close()

    return True


@celery.task
def phone_result(tts_id):
    url = current_app.config['TTS_SOAP_URL']
    user_code = current_app.config['TTS_USER_CODE']
    pwd = current_app.config['TTS_PWD']
    res_timeout = current_app.config['TTS_RESULT_TIMEOUT']
    timestamp = int(time.time())
    page = 1
    size = 20

    tts = TtsHistory.query.get(tts_id)
    try:
        client = Client(url)
        GetResultArg = [user_code, encrypt(pwd, user_code, timestamp), timestamp,
                        tts.result_id, page, size
                        ]
        result = client.service.GetResult(*GetResultArg)
        response = result.Result.TaskResultEntity[0]
        accept_at = int(time.mktime(response.Time.timetuple()))
        accept_duration = response.Duration
        accept_reason = response.FailedReason
        accept_status = response.ResultCode

    except Exception as e:
        print('post soap url error %s' % e)
        accept_at = None
        accept_duration = None
        accept_status = 999
        accept_reason = '连接ws服务器异常'

    if timestamp - tts.send_at >= res_timeout:
        accept_at = timestamp
        accept_reason = '超过规定时长未获取到结果'
        accept_status = 1

    if not accept_at:
        phone_result.apply_async(
            (tts.id,),
            countdown=10)
    else:
        try:
            tts.accept_at = accept_at
            tts.accept_duration = accept_duration
            tts.accept_reason = accept_reason
            tts.accept_status = accept_status
            db.session.commit()
        except Exception as e:
            print('add data error %s' % e)
            db.session.rollback()

    if 'db' in locals():
        db.session.close()

    return True


def new_encrypt(t1, t2):
    md = md5()
    _ = t2 + ''.join(['%s%s' % (k, v) for k, v in sorted(t1.items())]) + t2
    # print(_)
    md.update(_.encode())
    p1 = md.hexdigest()

    return p1


@celery.task
def send_phone_call_new(lsh, phone, note, strPartID):
    if not phone_call_filter(lsh, phone, note):
        print('no need to send phone call')
        return True

    api_url = current_app.config['NEW_TTS_API_URL']
    appKey = current_app.config['NEW_TTS_USER_CODE']
    appSecret = current_app.config['NEW_TTS_PWD']
    templateId = current_app.config['NEW_TTS_VOICE_TEMP_ID']
    timeStamp = time.strftime('%Y%m%d%H%M%S')
    # reqId = uuid.uuid1().hex
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    def generate_voice_by_template(p, a, t):
        endpoint = '/restful/api/v2/voice/addVoiceByTemplate'
        reqId = uuid.uuid1().hex
        content = {
            'phone_num': p,
            'address': a,
            'text1': t,
            'text2': ''
        }
        data = {
            'appKey': appKey,
            'reqId': reqId,
            'timeStamp': timeStamp,
            'templateId': templateId,
            'content': json.dumps(content),
        }

        sign = new_encrypt(data, appSecret)
        data.update({'sign': sign})

        response = requests.post(api_url + endpoint, data=data, headers=headers, timeout=10)
        return response.json()

    def send_call(audioId, phone):
        endpoint = '/restful/api/v2/call'
        reqId = uuid.uuid1().hex
        data = {
            'appKey': appKey,
            'reqId': reqId,
            'timeStamp': timeStamp,
            'callType': 1,
            'audioIds': audioId,
            'phone': phone,
            'playTimes': 3,
        }
        sign = new_encrypt(data, appSecret)
        data.update({'sign': sign})
        response = requests.post(api_url + endpoint, data=data, headers=headers, timeout=10)
        return response.text

    try:
        client = DispatchClient(timeout=10)
        result = client.ambulance.ambulance_info_by_lsh(lsh)
        phone_num, address, text1 = [(_.get('LXDH', ''), _.get('YYMC', ''), _.get('HJYYBC', '')) for _ in result][0]
        audio_id = generate_voice_by_template(phone_num, address, text1).get('audioId')  # 生成语音文件
        if audio_id:
            print(send_call(audio_id, phone))
    except Exception as e:
        print('post api url error %s' % e)

    return True
