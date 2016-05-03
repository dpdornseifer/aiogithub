import unittest
from aiohttp import BasicAuth
from aiogithub.utils import githubclient

class GitHubClientTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_githubenterprise_client(self):
        # TODO already tested in aiohttp-oauth
        pass


    def test_create_github_client(self):
        host = 'github.com'
        username = 'testuser'
        password = 'mypassword'
        type = 'private'
        self.githubclient = githubclient.GitHubClient(host, username, password, 'private')

        self.assertEqual(self.githubclient.base_url, 'https://github.com/api/v3/')
        self.assertEqual(self.githubclient.username, 'testuser')
        self.assertEqual(self.githubclient.password, 'mypassword')
        self.assertEqual(self.githubclient.auth, BasicAuth('testuser', 'mypassword'))

    def test_github_client_build_url(self):
        host = 'githubenterprise.com'
        username = 'testuser'
        password = 'mypassword'
        type = 'private'
        self.githubclient = githubclient.GitHubClient(host, username, password, type)

        self.assertEqual(self.githubclient.get_rest_endpoint('user'),
                         'https://githubenterprise.com/api/v3/user')

    def test_github_client_url_switch(self):
        host = 'api.github.com'
        username = 'testuser'
        password = 'mypassword'

        self.githubclient = githubclient.GitHubClient(host, username, password)

        self.assertEqual(self.githubclient.get_rest_endpoint('user'),
                     'https://api.github.com/user')

    def test_github_client_requerst(self):
        # TODO implmente async test for request function - request also already tested in aiohttp
        pass

if __name__ == "__main__":
    unittest.main()
