#!/usr/bin/python3
from settings import *
masto = Mastodon(
    client_id = f"{app_name}_cred.secret",
    api_base_url = instance_url
)
masto.log_in(
    email,
    password,
)
pushed_messages = []
while True:
    notifications = masto.notifications()
    for i in range(len(notifications)):
        notification_id = notifications[i]['id']
        if notification_id in pushed_messages:
            continue
        notification_type = notifications[i]['type']
        who = notifications[i]['account']['display_name']
        if notification_type == 'mention':
            original_toot = notifications[i]['status']['content']
            msg = f"{who} mentioned you in:\n{original_toot}"
        if notification_type == 'reblog':
            original_toot = notifications[i]['status']['content']
            msg = f"{who} rebloged your status:\n{original_toot}"
        if notification_type == 'favourite':
            original_toot = notifications[i]['status']['content']
            msg = f"{who} favoured your status:\n{original_toot}"
        if notification_type == 'follow':
            msg = f"{who} started following you"
        r = requests.post(
                f"{gotify_url}/message",
                headers=gotify_header,
                data={
                    'title': "Mastodon",
                    'message': msg,
                    'priority': 10})
        pushed_messages.append(notification_id)
    time.sleep(5)
    # print(notifications)
    # print(notification_type)
    # print(msg)
    # print(r)
