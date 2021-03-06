import logging
import json
import requests

from rbz_api.helpers.restplus import api
from flask_restplus import Resource
from rbz_api.helpers.serializers import movie, vote
from flask import request, abort, jsonify
from rbz_api.settings import APPKEY, SECONDS_TO_WAIT_FOR_RESPONSE, API_KEY_TMDB
from rbz_api.tasks.tasks import *
from rbz_api.database.db_functions import *
from flask import Response
from functools import wraps

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
ns = api.namespace('rbz/movies', description='Reddit Movie Thread')

# Decorator function to check if API-Key is valid
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') and request.headers.get('key') == APPKEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


@ns.route('/<string:push_id>/<int:show_more>')
class BotRequest(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.expect(movie, validate=False)
    @require_appkey
    def post(self, push_id, show_more):
        """
        Make a request to Movie Recommendation Server
        """
        data = request.json
        if show_more == 0:
            show_more_flag = False
        else:
            show_more_flag = True

        # Check if parent exists in database
        parentId, parentResponse = check_if_entry_exists(json.dumps(data))

        # Create new database entry and get entry id
        # If parent exists, the parentId and the parentResponse get set
        if parentResponse is None or parentResponse == "ERROR CALCULATING RECOMMENDATIONS!":
            parentId = None

        id = create_entry(json.dumps(data), parentResponse, parentId)
        # Check if response has to be calculated else return response
        if parentId is None:

            if(push_id == None):
                onesignal_id = ''
            else:
                onesignal_id = push_id

            CalculateAndSaveResponse.delay(id, json.dumps(data), onesignal_id, show_more_flag)

            # Check if response is calculated after 5 seconds
            # If true, return calculated response
            # else return id
            time.sleep(SECONDS_TO_WAIT_FOR_RESPONSE)
            modelObject = get_entry(id)

            if modelObject.response == None:
                return Response(response=str(id), mimetype='text/plain', status=202)
            else:
                data = {'id': id, 'response': modelObject.response}
                return Response(response=json.dumps(data), mimetype='text/plain', status=201)
        else:
            data = {'id': id, 'response':parentResponse}
            return Response(response=json.dumps(data), mimetype='text/plain', status=201)




@ns.route('/<int:id>')
class BotResponse(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.response(201, 'Object found, calculation finished')
    @api.response(404, 'Object not found.')
    @api.response(405, 'Calculation of response not finished.')
    @require_appkey
    def get(self, id):
        """
        Return a response with given ID.
        """
        # Get Object from database with id
        modelObject = get_entry(id)

        # Check if object in database
        if modelObject == None:
            return None, 404

        # Check if object response is set
        if modelObject.response == None:
            return None, 405
        else:
            return modelObject.response, 201


@ns.route('/genre/<string:text>')
class DatabaseGenre(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.response(201, 'Object found')
    @require_appkey
    def get(self, text):
        """
        Return a list of genres corresponding to the given text
        """
        # Get Object from database with id
        modelObject = get_genre(text)
        jsonResult  = json.dumps([dict(row) for row in modelObject])
        return jsonResult, 201

@ns.route('/movie/<string:text>')
class DatabaseMovie(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.response(201, 'Object found')
    @require_appkey
    def get(self, text):
        """
        Return a list of movies corresponding to the given text
        """
        # Get Object from database with id
        modelObject = get_movie(text)
        jsonResult  = json.dumps([dict(row) for row in modelObject])
        return jsonResult, 201

@ns.route('/person/<string:text>')
class DatabasePerson(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.response(201, 'Object found')
    @require_appkey
    def get(self, text):
        """
        Return a list of persons corresponding to the given text
        """

        # Get Object from database with id
        modelObject = get_person(text)
        jsonResult  = json.dumps([dict(row) for row in modelObject])
        return jsonResult, 201

@ns.route('/movie/details/<string:imdb_id>')
class DatabasePerson(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.response(201, 'Object found')
    @require_appkey
    def get(self, imdb_id):
        """
        Return a movie poster from TheMovieDB with a given IMDB-ID
        """
        LINK = 'https://api.themoviedb.org/3/find/' + imdb_id + '?api_key=' + API_KEY_TMDB + '&external_source=imdb_id'
        r = requests.get(LINK)
        return json.loads(r.text),201

@ns.route('/movie/vote')
class DatabaseUUID(Resource):
    @api.header('key', 'API-Key', required=True)
    @api.response(201, 'Vote inserted')
    @api.response(202, 'Vote updated')
    @api.expect(vote, validate=False)
    @require_appkey
    def post(self):
        """
        Insert new Device with given UUID
        """
        data = request.json
        uuid = data['device_uuid']
        username = data['username']
        recommendation_id = data['recommendation_id']
        movie_id = data['movie_id']
        vote = data['vote']

        modelObject = set_vote(uuid, username, recommendation_id, movie_id, vote)
        return "", modelObject