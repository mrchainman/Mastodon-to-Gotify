#!/usr/bin/python3
from settings import *
masto = Mastodon(
    client_id = f"{app_name}_cred.secret",
    api_base_url = instance_url
)
masto.log_in(
    email,
    password,
    to_file = f"{app_name}_user_cred.secret"
)
masto.notifications()
