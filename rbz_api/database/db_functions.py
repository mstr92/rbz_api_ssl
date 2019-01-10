##################################################################
# DATABASE
##################################################################
import time
import logging
from rbz_api.database import db
from rbz_api.database.model import DataModel, DeviceModel, UserModel, BackupModel, VoteModel
from datetime import datetime, timedelta
from sqlalchemy import exc, create_engine, MetaData, Table, Column, Integer, String, TIMESTAMP, text
from rbz_api.settings import SQLALCHEMY_DATABASE_URI, EXPIRE_DAYS, CRYPTO_KEY
from cryptography.fernet import Fernet
from rbz_api.helpers.push_notification import notify_user

###################################################################################
# API - Functions
###################################################################################
def create_entry(request, response, parentId):
    post = DataModel(request, response, parentId)
    db.session.add(post)
    db.session.flush()
    db.session.commit()
    return post.id


def check_if_entry_exists(data):
    try:
        d = DataModel.query.filter(DataModel.request == data,
                                   DataModel.parentId == None,
                                   DataModel.accessTime > datetime.today() - timedelta(days=EXPIRE_DAYS)).all()
        if len(d) == 0:
            return None, None
        else:
            return d[0].id, d[0].response

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None, None


def get_entry(id):
    try:
        db.session.commit()
        return DataModel.query.filter(DataModel.id == id).first()
    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None


def set_response(id, retval, retry, user_id):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        engine.execute("UPDATE rbz_api SET Response = %s WHERE Id = %s", (retval, str(id)))
        notify_user(user_id, 'Movie recommendation','Calculation for you recommendation is finished!', str(id))

    except exc.SQLAlchemyError(e):
        print("No entry in Database with ID: " + str(id))
        print(e)
        if retry:
            set_response(id, retval, False)


###################################################################################
# Movie and MetaData
###################################################################################
def get_movie(text):
    try:
        search_query = "%" + str(text) + "%"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute(
            "SELECT id, ttid, title, year FROM movie WHERE LOWER(title) LIKE LOWER(%s) ORDER BY rating_rank DESC LIMIT 5",
            search_query)
        return result

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None


def get_genre(text):
    try:
        search_query = "%" + str(text) + "%"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute("SELECT id,genrename FROM genre WHERE LOWER(genrename) LIKE LOWER(%s) LIMIT 5",
                                search_query)
        return result

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None


def get_person(text):
    try:
        search_query = "%" + str(text) + "%"
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute(
            "SELECT id, first_name, last_name FROM person WHERE CONCAT(LOWER(first_name),  ' ', LOWER(last_name)) LIKE LOWER(%s) OR CONCAT(LOWER(last_name),  ' ', LOWER(first_name)) LIKE LOWER(%s) LIMIT 5",
            (search_query, search_query))
        return result

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return None

def set_vote(device_uuid, username, recommendation_id, movie_id, vote):
    try:
        userModel = UserModel.query.filter(UserModel.username == username).first()
        id = None
        if userModel != None:
            id = userModel.id

        voteModel = VoteModel.query.filter(VoteModel.device_uuid == device_uuid).first()

        if voteModel == None:
            post = VoteModel(device_uuid, username, recommendation_id, movie_id, vote)
            db.session.add(post)
            db.session.flush()
            db.session.commit()
            return 201
        else:
            voteModel.vote = vote
            db.session.commit()
            return 202

    except exc.SQLAlchemyError:
        print("No entry in Database")
        return 401

###################################################################################
# General Functions
###################################################################################
def set_uuid(uuid):
    try:
        deviceModel = DeviceModel.query.filter(DeviceModel.uuid == uuid).first()
        if deviceModel == None:
            post = DeviceModel(uuid)
            db.session.add(post)
            db.session.flush()
            db.session.commit()
            return 201
        else:
            return 412

    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return 401


def set_user(username, email, password):
    try:
        userModel = UserModel.query.filter(UserModel.username == username).first()
        if userModel == None:
            cipher_suite = Fernet(CRYPTO_KEY)
            ciphered_password = cipher_suite.encrypt(password.encode())
            post = UserModel(username, email, ciphered_password)
            db.session.add(post)
            db.session.flush()
            db.session.commit()
            return 201
        else:
            return 410

    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return 401

def set_user_device_id(username, deviceId):
    try:
        userModel = UserModel.query.filter(UserModel.username == username).first()
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        if userModel == None:
           return 401
        else:
            if userModel.deviceID != None:
                splitUUID = userModel.deviceID.split(';')
                if len(filter(lambda x: x == deviceId, splitUUID)) > 0:
                    return 410
                else:
                    engine.execute("UPDATE user SET deviceID = CONCAT(IFNULL(deviceID,''), %s ) WHERE username = %s",
                                   (deviceId + ';', username))
                    return 201
            else:
                engine.execute("UPDATE user SET deviceID = CONCAT(IFNULL(deviceID,''), %s ) WHERE username = %s",
                               (deviceId + ';', username))
                return 201



    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return 401


def get_user(username):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = engine.execute(
            "SELECT id, username, email FROM user WHERE username = %s", username)
        return result
    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return None


def check_user_password(username, password):
    try:
        userObject = UserModel.query.filter(UserModel.username == username).first()
        cipher_suite = Fernet(CRYPTO_KEY)
        if(userObject != None):
            encrpyted_password = cipher_suite.decrypt(userObject.password.encode())
            if encrpyted_password == password:
                return 201
            else:
                return 410
        return 411
    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return None


def set_backup(user_id, history, rating, favourite):
    try:
        backupObject = BackupModel.query.filter(BackupModel.user_id == user_id).first()
        if backupObject == None:
            if history != '':
                post = BackupModel(user_id, history, rating, favourite, None, None,
                                   datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if rating != '':
                post = BackupModel(user_id, history, rating, favourite, None,
                                   datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None)
            if history != '':
                post = BackupModel(user_id, history, rating, favourite,
                                   datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, None)

            db.session.add(post)
            db.session.flush()
        else:
            if history != '':
                backupObject.history = history
                backupObject.history_last = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if rating != '':
                backupObject.rating = rating
                backupObject.rating_last = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if favourite != '':
                backupObject.favourite = favourite
                backupObject.favourite_last = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        return True

    except exc.SQLAlchemyError as e:
        print("No entry in Database")
        print(e)
        return False


def get_backup(user_id):
    try:
        db.session.commit()
        return BackupModel.query.filter(BackupModel.user_id == user_id).first()
    except exc.SQLAlchemyError:
        print("No entry in Database")
        return 401
