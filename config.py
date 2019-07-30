import datetime
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'AmbulanceMessageCenterLaLaLa'
    # JWT SETTING
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Ambulance'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(weeks=4)
    # RESTFUL SETTING
    ERROR_404_HELP = False
    PROPAGATE_EXCEPTIONS = False
    # SQLALCHEMY SETTING
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    # CELERY SETTING
    CELERYD_TASK_SOFT_TIME_LIMIT = 1800
    CELERYD_FORCE_EXECV = True  # ��ֹ����
    CELERYD_CONCURRENCY = 4  # ����worker��
    CELERYD_PREFETCH_MULTIPLIER = 2  # ÿ��ȡ������
    CELERYD_MAX_TASKS_PER_CHILD = 200  # ÿ��worker���ִ����200������ͻᱻ���٣��ɷ�ֹ�ڴ�й¶
    CELERY_DISABLE_RATE_LIMITS = True  # ���񷢳��󣬾���һ��ʱ�仹δ�յ�acknowledge , �ͽ��������½�������workerִ��
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_BROKER_URL = 'redis://localhost:6379/2'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
    # CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    CELERY_ANNOTATIONS = {'*': {'rate_limit': '10/s'}}  # ��������ÿ����ִ��Ƶ��
    # WECHAT SETTING
    WECHAT_BROKER_URL = 'redis://localhost:6379/1'
    WECHAT_SETTING = {
        'default': {
            'corp_id': '1'
        },
        'address_book': {
            'secret': '1',
        },
        'test1': {
            'agent_id': '1',
            'secret': '1'
        },
        'alarm': {
            'agent_id': '1',
            'secret': '1'
        }
    }

    # ExtParser SETTING
    EXT_PARSER_URL = '1'

    # ProcedureAggregate SETTING
    PROCEDURE_HOST = {
        'ip': '1',
        'port': '2',
        'instance': '3',
        'user': '4',
        'pswd': '5',
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_RECYCLE = 120
    SQLALCHEMY_POOL_TIMEOUT = 20


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY SETTING
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False


config = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
