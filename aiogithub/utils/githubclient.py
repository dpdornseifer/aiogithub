from aioauth_client import OAuth2Client
from aioauth_client import GithubClient
import configparser

# config management
config = configparser.ConfigParser()
config.read('settings.py')


class GitHubEnterpriseClient(OAuth2Client):
    def __init__(self, ghtoken=None):
        super(GitHubEnterpriseClient, self).__init__(
            client_id=config['GITHUB_APP']['ClientID'],
            client_secret=config['GITHUB_APP']['ClientSecret'],
            access_token_url='https://github.wdf.sap.corp/login/oauth/access_token',
            authorize_url='https://github.wdf.sap.corp/login/oauth/authorize',
            base_url='https://github.wdf.sap.corp/api/v3/',
            name='',
            user_info_url='https://github.wdf.sap.corp/api/v3/user',
            access_token=ghtoken
            )