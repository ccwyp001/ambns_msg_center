# -*- coding: utf-8 -*-

import json
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions

bp = Blueprint('auth_routes', __name__)
api = Api(bp)



@api.resource('/')
class AuthRouteApi(Resource):
    def get(self):
        return {'/form/advanced-form': { 'authority': ['admin', 'user'] }}
