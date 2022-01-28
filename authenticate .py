import os
import yaml
import requests
import base64
import constants
from urllib.parse import quote_plus
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests


class Authenticate:
    is_authenticated = False

    # TODO: Implement a custom OAuth2 if needed
    # TODO: Implement robust caching of the token

    def __init__(self, env: str = ''):
        if os.getenv('ENCOMPASS_API_TOKEN'):
            access_token = os.getenv('ENCOMPASS_API_TOKEN')
            self.is_authenticated = True
            print('Using existing token')
        else:
            auth_url = f'{constants.BASE_URL}/{constants.OAUTH_ENDPOINT}'
            creds_path = os.getenv('ENCOMPASS_CREDS' if not env else env.upper() + '_ENCOMPASS_CREDS')

            with open(creds_path) as creds_file:
                creds_data = yaml.safe_load(creds_file)

            client_id = creds_data['partner_client_id']
            client_secret = creds_data['partner_client_key']
            header_auth_string = Authenticate.encode_base64(f'{client_id}:{client_secret}')

            payload = f'grant_type={creds_data["grant_type"]}&username={quote_plus(creds_data["username"])}' \
                      f'&password={quote_plus(creds_data["password"])}'

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f"Basic {header_auth_string}"
            }

            client = BackendApplicationClient(client_id=client_id)
            oauth_session = OAuth2Session(client=client)

            response = oauth_session.request(url=auth_url, method='POST', headers=headers, data=payload, auth=None)
            response_data = response.json()
            access_token = response_data['access_token']

            if response.status_code == 200:
                os.environ['ENCOMPASS_API_TOKEN'] = access_token
                self.is_authenticated = True
        self.__session = session = requests.Session()
        self.__session.headers = {"Authorization": f"Bearer {access_token}", 'Content-Type': 'application/json'}

    @property
    def session(self):
        return self.__session if self.is_authenticated else None

    @staticmethod
    def encode_base64(value: str) -> str:
        _bytes = value.encode('ascii')
        _base64_bytes = base64.b64encode(_bytes)
        _base64_string = _base64_bytes.decode('ascii')

        return _base64_string


if __name__ == "__main__":
    # auth = Authenticate()
    # response = auth.session.get("https://api.elliemae.com/encompass/v1/loans/00685b91-bc6d-472e-81e9-06aa2bcf8ff4")
    # #print(response.text)
    loanid="2d6acb8c-0396-4696-abab-b50c548314de"
    url = "https://api.elliemae.com/encompass/v1/loans/"+loanid+"/applications"
    auth = Authenticate()

    response = auth.session.get(url)
    print(response.text)
