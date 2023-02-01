#!/usr/bin/env python

# ref: https://github.com/pacellig/Keycloak-python-authorization/blob/master/src/services.py
"""
simple application that lets check if user is authn or not
"""
import json

from flask import Flask, Response
from flask_oidc import OpenIDConnect

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

oidc = OpenIDConnect(app)

@app.route('/private', methods=['GET'])
@oidc.require_login
def hello_private():
    return Response(status=200, response="User is authorized to access this endpoint")

@app.route('/public', methods=['GET'])
def hello_public():
    return Response(status=200, response="This endpoint is publicly accessible")

# from https://flask-oidc.readthedocs.io/en/latest/
# but i don know what is g
#@app.route('/api')
#@oidc.accept_token()
#def my_api():
#    return json.dumps('Welcome %s' % oidc.oidc_token_info['sub'])

if __name__ == '__main__':
    app.run(debug=True, port=9191)


