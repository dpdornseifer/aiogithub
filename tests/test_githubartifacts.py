import unittest
import json
import aiogithub.githubartifacts as ghartifacts
from aiogithub.utils import githubdataflow


class GitHubArtifactsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_user_repo_artifact(self):
        self.githubrepo = ghartifacts.GitHubRepository('test_repo', "My new repo")
        self.assertEqual(self.githubrepo.prio, 1)
        self.assertEqual(self.githubrepo.flow, githubdataflow.RepositoryFlow)

    def test_create_orga_repo_artifact(self):
        self.githubrepo = ghartifacts.GitHubRepository('test_repo', "My new repo", 'true', 'GitHub')
        self.assertEqual(self.githubrepo.ghurl, 'orgs/GitHub/repos')

    def test_get_json_from_repo(self):
        #jsonpayload = '{"has_wiki": True, "description": "My new repo", "has_downloads": True,' \
        #              ' "private": True, "auto_init": False, "has_issues": True, "licence_template": "",' \
        #             ' "homepage": "", "name": "test_repo"}'

        jsonpayload = dict(has_wiki=True, description="My new repo", has_downloads=True,\
                      private=True, auto_init=False, has_issues=True, licence_template="",\
                      homepage="", name="test_repo")

        self.githubrepo = ghartifacts.GitHubRepository('test_repo', "My new repo", True, 'GitHub')
        self.assertDictEqual(json.loads(self.githubrepo.getjsonpayload()), jsonpayload)

    def test_get_file_artifact(self):
        self.githubfile = ghartifacts.GitHubFile('Readme.md', 'test_user', 'test_repo', '#My repo', '')
        self.assertEqual(self.githubfile.ghurl, 'repos/test_user/test_repo/git/blobs')
        self.assertEqual(self.githubfile.prio, 2)

    def test_get_json_from_file(self):
        jsonpayload = '{"Readme.md": {"Content": "#My repo", "Path": ""}}'
        self.githubfile = ghartifacts.GitHubFile('Readme.md', 'test_user', 'test_repo', '#My repo', '')
        self.assertDictEqual(json.loads(self.githubfile.getjsonpayload()), json.loads(jsonpayload))

    def test_get_label_artifact(self):
        self.githublabel = ghartifacts.GitHubLabel('test_user', 'test_repo', 'bug', 'f29513')
        self.assertEqual(self.githublabel.ghurl, 'repos/test_user/test_repo/labels')
        self.assertEqual(self.githublabel.prio, 2)

    def test_get_json_from_label(self):
        jsonpayload = '{"name": "bug", "color": "f29513"}'
        self.githublabel = ghartifacts.GitHubLabel('test_user', 'test_repo', 'bug', 'f29513')
        self.assertDictEqual(json.loads(self.githublabel.getjsonpayload()), json.loads(jsonpayload))


if __name__ == "__main__":
    unittest.main()
