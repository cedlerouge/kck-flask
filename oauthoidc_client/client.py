#!/usr/bin/env python

import sys
from tkinter import W
import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs

from keycloak import KeycloakOpenID

from config import Config
from tools import print_json

def print_debug(name, obj):
    if debug:
        print("name => %s" % name)
        print(obj)
        print(dir(obj))

def load_config():
    """
    Load config from the default file (settings.json)
    :return:
    """
    filename = 'settings.json'
    config = Config(filename)

    return config.load_config()

# https://github.com/pacellig/Keycloak-python-authorization
# this is done by keycloak_openid.token
def get_user_token(config):
    """
    Retrieve the access token for the user from the dedicated client.
    :return: access_token
    """
    url = config['auth_uri'] + "realms/" + config['realm_name'] + "/protocol/openid-connect/token"
    payload = "grant_type=authorization_code&client_id=" + config['client_id'] + "&username=" + \
                config['username'] + "&password=" + config['password']
    print(payload)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response)

    return True
    #return response.json()['access_token']


if __name__ == '__main__':
    """
    Load config, then use config to request access token 
    and finally use token to request the api
    """
    _config = load_config()

    debug = _config['debug'] = 'debug' in _config and _config['debug']

    if debug:
        print_json(_config)

    # Configure client
    keycloak_openid = KeycloakOpenID(server_url=_config['auth_uri'],  
                    client_id=_config['client_id'],
                    client_secret_key=_config['client_secret'],
                    realm_name=_config['realm_name'])   
    print_debug("keycloak_openid", keycloak_openid)

    print_debug("keycloak_openid.auth_url", keycloak_openid.auth_url)
    print_debug("keycloak_openid.userinfo", keycloak_openid.userinfo)
    print_debug("keycloak_openid.logout", keycloak_openid.logout)
    print_debug("keycloak_openid.authorization", keycloak_openid.authorization)

    # Get WellKnow
    config_well_known = keycloak_openid.well_known()
    print_debug("config_well_known", config_well_known)
    # print_json(config_well_known)

    priv = requests.request("GET", "http://localhost:9191/private")
    parsed_url = urlparse(priv.url)
    captured_value = parse_qs(parsed_url.query)['state'][0]

    print(captured_value)

    token = keycloak_openid.token(username=_config['username'], password=_config['password'])
    print_debug("token", token)
    print(token)

    headers = {
        'Authorization': "Bearer " + token['access_token']
    }

    # Get Code With Oauth Authorization Request
    auth_url = keycloak_openid.auth_url(
        redirect_uri=_config['redirect_uri'],
        scope=_config['scope'],
        state=captured_value)
    print_debug("auth_url", auth_url)
    print(auth_url)

    auth = requests.request("GET", auth_url, headers=headers)
    print_debug("auth", auth)
    print_debug("auth.url", auth.url)
    print_debug("auth.content", auth.content)
    print_debug("auth.is_redirect", auth.is_redirect)

    

    response = requests.request("GET", "http://localhost:9191/public")
    print("http://localhost:9191/public => {}  - {}".format(response.status_code, response.text))

    response = requests.request("GET", "http://localhost:9191/private", headers=headers)
    print(response.request)
    print(response.headers)
    print("http://localhost:9191/private => {}  - {}".format(response.status_code, response.text))
    
    #response = requests.request("GET", "http://localhost:9191/api", headers=headers)
    #print(response)