from flask_restplus import fields
from rbz_api.helpers.restplus import api
from rbz_api.settings import MAX_YEAR, MIN_YEAR

movie = api.model('Movies', {
    'neg_entity': fields.List(fields.String(description='List of negative entities')),
    'pos_entity': fields.List(fields.String(description='List of positive entities')),
    'neg_movie': fields.List(fields.String(description='List of negative movies')),
    'pos_movie': fields.List(fields.String(description='List of positive movies')),
    'neg_actor': fields.List(fields.String(description='List of negative actors')),
    'pos_actor': fields.List(fields.String(description='List of positive actors')),
    'neg_genre': fields.List(fields.String(description='List of negative genres')),
    'pos_genre': fields.List(fields.String(description='List of positive genres')),
    'neg_keyword': fields.List(fields.String(description='List of negative keywords')),
    'pos_keyword': fields.List(fields.String(description='List of positive keywords')),
    'neg_year_from': fields.List(fields.Integer(min=MIN_YEAR, max=MAX_YEAR, description='List of negative years from')),
    'pos_year_from': fields.List(fields.Integer(min=MIN_YEAR, max=MAX_YEAR, description='List of positive years from')),
    'neg_year_to': fields.List(fields.Integer(min=MIN_YEAR, max=MAX_YEAR, description='List of negative years to')),
    'pos_year_to': fields.List(fields.Integer(min=MIN_YEAR, max=MAX_YEAR, description='List of positive years to')),
    'length': fields.Integer(description='Total number of results'),
    'user_id': fields.String(description='OneSignal User Id'),
    # 'approach': fields.Integer(description='Total number of results'),
})

user = api.model('User', {
    'username': fields.String(description='Username'),
    'email': fields.String(description='Email adress'),
    'password': fields.String(description='Password')
})

backup = api.model('Backup', {
    'user_id': fields.Integer(description='UserID'),
    'history': fields.String(description='JSON string with history movie objects'),
    'rating': fields.String(description='JSON string with rating movie objects'),
    'favourite': fields.String(description='JSON string with favourite movie objects')
})

device_user = api.model('Device_User', {
    'username': fields.String(description='Username'),
    'deviceId': fields.String(description='deviceId')
})
