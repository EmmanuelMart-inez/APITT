import os
from flask import g
from flask_oauthlib.client import OAuth

# Check below
from oauthlib.oauth2 import WebApplicationClient

oauth = OAuth()
"""
github = oauth.remote_app(
    'github',
    consumer_key=os.getenv("GITHUB_CONSUMER_KEY"),
    consumer_secret=os.getenv("GITHUB_CONSUMER_SECRET"),
    request_token_params={"scope": "user:email"},
    base_url="https://api.github.com/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize"
)
"""

facebook = oauth.remote_app(
    "facebook",
    base_url="https://graph.facebook.com/",
    request_token_url=None,
    access_token_url="/oauth/access_token",
    authorize_url="https://www.facebook.com/dialog/oauth",
    consumer_key=os.getenv("FACEBOOK_APP_ID"),
    consumer_secret=os.getenv("FACEBOOK_APP_SECRET"),
    request_token_params={"scope": "email"},
)
"""
github = oauth.remote_app('facebook',
    base_url='https://accounts.google.com/o/oauth2/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=os.getenv("FACEBOOK_APP_ID"),
    consumer_secret=os.getenv("FACEBOOK_APP_SECRET"),
    request_token_params={'scope': 'email'}
)
"""


@facebook.tokengetter
def get_facebook_token():
    if "access_token" in g:
        return g.access_token
