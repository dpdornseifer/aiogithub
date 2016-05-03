import unittest
import asyncio
from aiohttp.web import Request
from aiogithub import AioGitHub
from aiogithub import githubartifacts

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
        self.aiogithub.ghartifacts = {"repo_name": "bug"}
        self.assertEqual(self.aiogithub.ghartifacts, {"repo_name": "bug"})

    def test_set_repoowner(self):
        self.aiogithub.repoowner = 'githubusername'
        self.assertEqual(self.aiogithub.repoowner, 'githubusername')

    def test_set_reponame(self):
        self.aiogithub.reponame = 'reponame'
        self.assertEqual(self.aiogithub.reponame, 'reponame')

    def test_add_github_artifact(self):
        self.githubrepository = githubartifacts.GitHubRepository('test_repository', 'my repo')
        self.githubfile = githubartifacts.GitHubFile('Readme.md', 'test_user', 'test_repository', '#My File \n', '')
        self.aiogithub.ghartifacts = [self.githubrepository, self.githubfile]
        self.assertEqual(self.aiogithub.ghartifacts, [self.githubrepository, self.githubfile])

    def test_check_if_github_artifacts_are_valid(self):
        self.githubrepository = githubartifacts.GitHubRepository('test_repository', 'my repo')
        self.githubfile = githubartifacts.GitHubFile('Readme.md', 'test_user', 'test_repository', '#My File \n', '')
        self.aiogithub.ghartifacts = [self.githubrepository, self.githubfile]
        self.assertTrue(self.aiogithub.artifactsvalid())
        self.aiogithub.addghartifact('my string artifact')
        self.assertFalse(self.aiogithub.artifactsvalid())

    def test_get_priority_dict(self):
        self.githubrepository = githubartifacts.GitHubRepository('test_repository', 'my repo')
        self.githubfile = githubartifacts.GitHubFile('Readme.md', 'test_user', 'test_repository', '#My File \n', '')
        self.aiogithub.ghartifacts = [self.githubrepository, self.githubfile]
        priority_dict = {1: [self.githubrepository], 2: [self.githubfile]}
        self.assertDictEqual(self.aiogithub.get_priority_dict(), priority_dict)

    def test_get_task_list(self):
        self.githubrepository = githubartifacts.GitHubRepository('test_repository', 'my repo')
        self.githubfile = githubartifacts.GitHubFile('Readme.md', 'test_user', 'test_repository', '#My File \n', '')
        self.aiogithub.ghartifacts = [self.githubrepository, self.githubfile]
        priority_dict = {1: [self.githubrepository], 2: [self.githubfile]}
        self.assertTrue(asyncio.iscoroutine(self.aiogithub.get_tasks(priority_dict[1])[0]))



    #def test_add_labels(self):
    #    self.aiogithub.addlabels({"bug": "f29513", "testing": "f29513"})
    #    self.assertEqual(self.aiogithub.getlabels('{"name":"bug", "color": "f29513"},'
    #                                              '{"name": "testing", "color": "f29513"}'))



if __name__ == "__main__":
    unittest.main()
