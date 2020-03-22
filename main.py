#!/usr/bin/python3
from settings import *
# Create Mastodon App
masto = Mastodon(
    client_id = f"{app_name}_cred.secret",
    api_base_url = instance_url
)
# Login to mastodon account
masto.log_in(
    email,
    password,
)
# Create empty listed for notifications, that have already been pushed to gotify
pushed_messages = []
# Start infinite loop
while True:
    # Fetch the notifications
    notifications = masto.notifications()
    # Get the number of notifications
    number_of_notifications = range(len(notifications))
    # Write the number to a file for further processing
    # (can be disabled)
    with open(path, 'w') as f:
        f.write(str(len(number_of_notifications)))
    # Iterate over the notifications
    for i in number_of_notifications:
        # Get the ID as a unique identifier
        notification_id = notifications[i]['id']
        # Check if it has already been pushed
        if notification_id in pushed_messages:
            continue
        # Get the notification type and issuer
        notification_type = notifications[i]['type']
        who = notifications[i]['account']['display_name']
        # Write message depending on the notificaiton type
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
        # Push the notification to the gotify server
        r = requests.post(
                f"{gotify_url}/message",
                headers=gotify_header,
                data={
                    'title': "Mastodon",
                    'message': msg,
                    'priority': 10})
        # Append the notification ID to the already pushed list
        pushed_messages.append(notification_id)
    # Wait 5 seconds
    time.sleep(5)
