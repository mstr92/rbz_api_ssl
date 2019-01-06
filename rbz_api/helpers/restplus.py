import logging

from flask_restplus import Api

log = logging.getLogger(__name__)
api = Api(version='1.0', title='rbz.io API', description='API for rbz.io')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not True:
        return {'message': message}, 500
