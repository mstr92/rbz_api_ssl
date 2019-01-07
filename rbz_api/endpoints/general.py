import logging
import json
import requests

from rbz_api.helpers.restplus import api
from flask_restplus import Resource
from rbz_api.helpers.serializers import movie, backup, user, device_user
from flask import request, abort, jsonify
from rbz_api.settings import APPKEY, SECONDS_TO_WAIT_FOR_RESPONSE, API_KEY_TMDB
from rbz_api.tasks.tasks import *
from rbz_api.database.db_functions import *
from flask import Response
from functools import wraps

log = logging.getLogger(__name__)
ns = api.namespace('rbz/general', description='General Functions')


# Decorator function to check if API-Key is valid
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') and request.headers.get('key') == APPKEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


@ns.route('/uuid/<string:uuid>')
class DatabaseUUID(Resource):

    @api.response(201, 'UUID inserted')
    @api.response(412, 'UUID already in database')
    @require_appkey
    def post(self, uuid):
        """
        Insert new Device with given UUID
        """
        modelObject = set_uuid(uuid)
        return "", modelObject


@ns.route('/user')
class DatabaseUser(Resource):

    @api.expect(user, validate=False)
    @api.response(201, 'User registered in database')
    @api.response(401, 'Error: User not registered!')
    @api.response(410, 'Error: Username already in use!')
    @require_appkey
    def post(self):
        """
        Insert new User
        """
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']

        modelObject = set_user(username, email, password)
        return "", modelObject

@ns.route('/user/deviceId')
class DatabaseUser(Resource):

    @api.expect(device_user, validate=False)
    @api.response(201, 'User registered in database')
    @api.response(401, 'Error: User not registered!')
    @api.response(410, 'Error: Username already in use!')
    @require_appkey
    def post(self):
        """
        Insert new User
        """
        data = request.json
        username = data['username']
        deviceId = data['deviceId']

        modelObject = set_user_device_id(username, deviceId)
        return "", modelObject

@ns.route('/user/<string:username>')
class DatabaseUser(Resource):

    @api.response(201, 'User registered in database')
    @api.response(401, 'Error: User not registered!')
    @require_appkey
    def get(self, username):
        """
        Get User
        """
        modelObject = get_user(username)
        jsonResult = json.dumps([dict(row) for row in modelObject])
        if modelObject != None:
            return jsonResult, 201
        else:
            return "", 401


@ns.route('/password/<string:username>/<string:password>')
class DatabaseUser(Resource):
    @api.response(201, 'Password correct!')
    @api.response(410, 'Password incorrect!')
    @api.response(411, 'User does not exist')
    @require_appkey
    def get(self, username, password):
        """
        Check Password
        """
        modelObject = check_user_password(username, password)
        if modelObject != None:
            return "" , modelObject
        else:
            return "", 401

@ns.route('/backup')
class DatabaseUser(Resource):

    @api.expect(backup, validate=False)
    @api.response(201, 'User registered in database')
    @api.response(401, 'Error: User not registered!')
    @require_appkey
    def post(self):
        """
        Insert Backup Objects for user
        """
        data = request.json

        modelObject = set_backup(data['user_id'], data['history'], data['rating'], data['favourite'])
        if modelObject:
            return 201
        else:
            return 401

@ns.route('/backup/history/<int:user_id>')
class DatabaseUser(Resource):
    @api.response(201, 'Entry exists')
    @require_appkey
    def get(self, user_id):
        modelObject = get_backup(user_id)
        if modelObject != None:
            return modelObject.history, 201
        else:
            return "", 401


@ns.route('/backup/favourite/<int:user_id>')
class DatabaseUser(Resource):
    @api.response(201, 'Entry exists')
    @require_appkey
    def get(self, user_id):
        modelObject = get_backup(user_id)
        if modelObject != None:
            return modelObject.favourite, 201
        else:
            return "", 401


@ns.route('/backup/rating/<int:user_id>')
class DatabaseUser(Resource):
    @api.response(201, 'Entry exists')
    @require_appkey
    def get(self, user_id):
        modelObject = get_backup(user_id)
        if modelObject != None:
            return modelObject.rating, 201
        else:
            return "", 401


@ns.route('/backup/dates/<int:user_id>')
class DatabaseUser(Resource):
    @api.response(201, 'Entry exists')
    @require_appkey
    def get(self, user_id):
        modelObject = get_backup(user_id)
        if modelObject != None:
            return str(modelObject.rating_last)+"," +str(modelObject.history_last)+","+str(modelObject.favourite_last), 201

        else:
            return "", 401