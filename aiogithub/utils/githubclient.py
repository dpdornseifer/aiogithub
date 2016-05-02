import asyncio
from urllib.parse import urljoin
from aioauth_client import OAuth2Client
from aiohttp import ClientRequest, BasicAuth

class GitHubClient(object):
    ''' Client implementation using http basic auth '''

    def __init__(self, host, user, password):
        super(GitHubClient, self).__init__()
        self._base_url = 'https://{}/api/v3/'.format(host)
        self._user = user
        self._password = password
        self._auth = BasicAuth(user, password)


    @property
    def base_url(self):
        return self._base_url

    @property
    def username(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def auth(self):
        return self._auth

    def get_rest_endpoint(self, endpoint):
        return urljoin(self._base_url, endpoint)

    def request(self, method, url, params=None,  timeout=10, headers=None, **aio_kwargs):
        return asyncio.wait_for(
            ClientRequest(method, self._get_rest_enpoint(url), params=params, headers=headers, auth=self._auth, **aio_kwargs),
            timeout)


class GitHubEnterpriseClient(OAuth2Client):
    ''' Client implementation using OAuth2 auth '''

    def __init__(self, client_id, client_secret, host, ghtoken=None):
        super(GitHubEnterpriseClient, self).__init__(
            client_id=client_id,
            client_secret=client_secret,
            access_token_url='https://{}/login/oauth/access_token'.format(host),
            authorize_url='https://{}/login/oauth/authorize'.format(host),
            base_url='https://{}/api/v3/'.format(host),
            name='',
            user_info_url='https://{}/api/v3/user'.format(host),
            access_token=ghtoken
            )


