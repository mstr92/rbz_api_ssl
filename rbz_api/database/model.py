from rbz_api.database import db


class DataModel(db.Model):
    __tablename__ = "rbz_api"
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    request = db.Column('Request', db.String)
    response = db.Column('Response', db.String)
    accessTime = db.Column('AccessTime', db.TIMESTAMP)
    parentId = db.Column('ParentId', db.Integer)

    def __init__(self, request, response, parentId):
        self.request = request
        self.response = response
        self.parentId = parentId


class DeviceModel(db.Model):
    __tablename__ = "device"
    uuid = db.Column('uuid', db.String, primary_key=True)

    def __init__(self, uuid):
        self.uuid = uuid



class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String)
    email = db.Column('email', db.String)
    password = db.Column('password', db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class BackupModel(db.Model):
    __tablename__ = "backup_data"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer)
    history = db.Column('history', db.String)
    rating = db.Column('rating', db.String)
    favourite = db.Column('favourite', db.String)
    history_last = db.Column('history_last', db.TIMESTAMP)
    rating_last = db.Column('rating_last', db.TIMESTAMP)
    favourite_last = db.Column('favourite_last', db.TIMESTAMP)

    def __init__(self, user_id, history, rating, favourite, favourite_last, rating_last, history_last):
        self.user_id = user_id
        self.history = history
        self.rating = rating
        self.favourite = favourite
        self.favourite_last = favourite_last
        self.rating_last = rating_last
        self.history_last = history_last

class VoteModel(db.Model):
    __tablename__ = "recommendation_votes"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer)
    device_uuid = db.Column('device_uuid', db.String)
    recommendation_id = db.Column('recommendation_id', db.Integer)
    movie_id = db.Column('movie_id', db.Integer)
    vote = db.Column('vote', db.Integer)

    def __init__(self, user_id, device_uuid, recommendation_id, movie_id, vote):
        self.user_id = user_id
        self.device_uuid = device_uuid
        self.recommendation_id = recommendation_id
        self.movie_id = movie_id
        self.vote = vote
