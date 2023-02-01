# Discover Keycloak 

## oauthoidc_client

Simple application to request authenticated API: 
* a flask app to serve endpoints
* a keycloak containers to authenticate / authorize
* a client to request

### Ref: 
Thanks to those projects which allowed me to see things clearly

* https://python-keycloak.readthedocs.io/en/latest/
* https://flask-oidc.readthedocs.io/en/latest/
* https://github.com/pacellig/Keycloak-python-authorization
* https://github.com/curityio/example-python-openid-connect-client
* https://user.cscs.ch/storage/lts/rest_api_howto/

## saml_client

Simple application which display attributes returned by keycload with SAML protocol

### Ref
Thanks to those projects which allowed me to see things clearly

* https://wjw465150.gitbooks.io/keycloak-documentation/content/server_admin/topics/clients/client-saml.html
* https://docs.getunleash.io/how-to/how-to-add-sso-saml-keycloak
* https://xwf.medium.com/secure-flask-application-with-keycloak-and-saml-2-0-3c1986f47cd
* https://github.com/mx-moth/flask-saml2/blob/f22ab443137aee1934a73134e18a3113bbe74f11/flask_saml2/sp/sp.py
