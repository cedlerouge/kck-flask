from flask import Flask, url_for
from flask_saml2.sp import ServiceProvider
from flask_saml2.utils import certificate_from_file, private_key_from_file

class ExampleServiceProvider(ServiceProvider):
  def get_sp_entity_id(self):
    return self.get_sp_config().get('entity_id')

  def get_logout_return_url(self):
    return url_for('index', _external=True)

  def get_default_login_return_url(self):
    return url_for('index', _external=True)

sp = ExampleServiceProvider()
app = Flask(__name__)
app.debug = True
app.secret_key = 'tatatototutu'
app.config['SERVER_NAME'] = 'localhost.localdomain:8082'
app.config['SAML2_SP'] = {
  'entity_id': 'kck-saml-flask-test',
  'certificate': certificate_from_file('cert1.pem'),
  'private_key': private_key_from_file('key1.pem'),
}

app.config['SAML2_IDENTITY_PROVIDERS'] = [
  {
    'CLASS': 'flask_saml2.sp.idphandler.IdPHandler',
    'OPTIONS': {
      'display_name': 'KeyCloak',
      'entity_id': 'https://localhost:8181/auth/realms/Integration-interne',
      'sso_url': 'https://localhost:8181/auth/realms/Integration-interne/protocol/saml',
      'slo_url': 'https://localhost:8181/auth/realms/Integration-interne/protocol/saml',
      'certificate': certificate_from_file('cert2.pem'),
    },
  },
]

# index
@app.route('/')
def index():
  if sp.is_user_logged_in():
    auth_data = sp.get_auth_data_in_session()

    message = f'''
    <p>You are logged in as <strong>{auth_data.nameid}</strong>.
    The IdP sent back the following attributes:<p>
    '''
    print(auth_data.attributes.items())
    attrs = '<dl>{}</dl>'.format(''.join(
      f'<dt>{attr}</dt><dd>{value}</dd>'
      for attr, value in auth_data.attributes.items()))

    logout_url = url_for('flask_saml2_sp.logout')
    logout = f'<form action="{logout_url}" method="POST"><input type="submit" value="Log out"></form>'

    return message + attrs + logout
  else:
    message = '<p>You are logged out.</p>'

    login_url = url_for('flask_saml2_sp.login')
    link = f'<p><a href="{login_url}">Log in to continue</a></p>'

    return message + link

# Blueprint
app.register_blueprint(sp.create_blueprint(), url_prefix='/saml/')

# Setup
if __name__ == "__main__":
  app.run(port=8082)


