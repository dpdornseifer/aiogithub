import unittest
import json
import aiogithub.githubartifacts as ghartifacts


class GitHubArtifactsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_user_repo_artifact(self):
        self.githubrepo = ghartifacts.GitHubRepository('test_repo', "My new repo")
        self.assertEqual(self.githubrepo.prio, 1)


    def test_create_orga_repo_artifact(self):
        self.githubrepo = ghartifacts.GitHubRepository('test_repo', "My new repo", 'true', 'GitHub')
        self.assertEqual(self.githubrepo.ghurl, 'orgs/GitHub/repos')

    def test_get_json_from_repo(self):
        jsonpayload = '{"has_wiki": "true", "description": "My new repo", "has_downloads": "true",' \
                      ' "private": "true", "auto_init": "false", "has_issues": "true", "licence_template": "None",' \
                      ' "homepage": "None", "name": "test_repo"}'

        self.githubrepo = ghartifacts.GitHubRepository('test_repo', "My new repo", 'true', 'GitHub')
        self.assertDictEqual(json.loads(self.githubrepo.getjsonpayload()), json.loads(jsonpayload))


if __name__ == "__main__":
    unittest.main()