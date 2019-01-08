
import json
import requests
# https://github.com/mikaelm1/flask-api-boilerplate/edit/master/util/push_notifications.py

def notify_user(player_id, title, message, id):
    """
    Sends push notification to a single user.
    :param player_id: String - Signal One id of user
    :param title: String - title of notification
    :param message: String - body of notification
    :param subtitle: String - optional subtitle of notification
    :return: None
    """
    headers = {"Authorization": "Basic {}".format('NGEzMGYwMmYtYmNjOS00YWNhLWFkM2UtM2ZiNDEyMWQzYzRh'),
               'Content-Type': 'application/json; charset=utf-8'}
    body = {"include_player_ids": [player_id],
            "app_id": 'c61624bb-71b9-442f-85aa-ce0ae06c4f51',
            "contents": {"en": message},
            "headings": {"en": title},
            "data": {"id": id},
            "buttons": [{"id":"goto", "text": "Go To Result"}]}
    url = 'https://onesignal.com/api/v1/notifications'
    r = requests.post(url, headers=headers, data=json.dumps(body))
    res = r.json()
    return None