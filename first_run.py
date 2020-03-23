#!/usr/bin/python3
from settings import *
Mastodon.create_app(
     app_name,
     api_base_url = instance_url,
     to_file = f"{app_name}_cred.secret"
)
