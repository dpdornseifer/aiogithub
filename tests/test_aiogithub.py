import unittest
import asyncio
from aiohttp.web import Request
from aiogithub import AioGitHub


class AioGitHubTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.aiogithub = AioGitHub('github.com', 'me')

    def tearDown(self):
        self.aiogithub = AioGitHub('github.com', 'me')

    def test_get_event_loop(self):
        self.assertEqual(self.aiogithub.loop, asyncio.get_event_loop())

    def test_set_github_host(self):
        self.aiogithub.githubhost = 'github.com'
        self.assertEqual(self.aiogithub.githubhost, 'github.com')

    def test_set_github_client(self):
        self.aiogithub.githubclient = 'github_client_object'
        self.assertEqual(self.aiogithub.githubclient, 'github_client_object')

    def test_set_payload(self):
        self.aiogithub.payload = {"repo_name": "bug"}
        self.assertEqual(self.aiogithub.payload, {"repo_name": "bug"})

    def test_set_repoowner(self):
        self.aiogithub.repoowner = 'githubusername'
        self.assertEqual(self.aiogithub.repoowner, 'githubusername')

    def test_set_reponame(self):
        self.aiogithub.reponame = 'reponame'
        self.assertEqual(self.aiogithub.reponame, 'reponame')




    #def test_add_labels(self):
    #    self.aiogithub.addlabels({"bug": "f29513", "testing": "f29513"})
    #    self.assertEqual(self.aiogithub.getlabels('{"name":"bug", "color": "f29513"},'
    #                                              '{"name": "testing", "color": "f29513"}'))



if __name__ == "__main__":
    unittest.main()
