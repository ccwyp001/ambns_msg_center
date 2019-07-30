# -*- coding: utf-8 -*-
from flask import Flask, make_response
import json
from werkzeug.utils import find_modules, import_string
from config import config
from .extensions import db, celery, SLBigInteger, LongText, spyne
from . import models  # use for migrate


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    app.url_map.strict_slashes = False
    db.init_app(app)
    spyne.init_app(app)
    celery.init_app(app)
    from .api import wsdl
    register_blueprints(app, 'v1', 'pen_apple.api.v1')

    return app


def register_blueprints(app, v, package):
    for module_name in find_modules(package):
        module = import_string(module_name)
        if hasattr(module, 'bp'):
            bp = module.bp
            api = module.api
            api.errors.update(api_errors())
            api.representations['application/json'] = output_json
            app.register_blueprint(bp, url_prefix='/api/{0}/{1}'.format(v, bp.name))


def output_json(data, code, headers=None):
    result = {}
    if code in (200, 201, 204):
        result['code'] = 10000
        result['result'] = data
    else:
        result['code'] = 44444
        result['message'] = data['message']
        result.update(data)
    response = make_response(json.dumps(result), code)
    response.headers.extend(headers or {})
    return response


def api_errors():
    errors = {
        'InvalidSignatureError': {
            'status': 401, 'message': 'Signature verification failed'
        },
        'DecodeError': {
            'status': 401, 'message': 'Not enough segments'
        },
        'NoAuthorizationError': {
            'status': 403, 'message': 'Missing Authorization Header'},
        'ExpiredSignatureError': {
            'status': 401, 'message': 'Signature has expired'},
    }
    from .commons.exceptions import BaseException
    errors.update(
        {cls.__name__: cls.__dict__ for cls in BaseException.__subclasses__()}
    )

    return errors
