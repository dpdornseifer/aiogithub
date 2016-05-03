import json
from aiogithub.utils import githubdataflow


class GitHubArtifact:
    ''' Base clase for all objects on GitHub '''

    def __init__(self, ghurl=None, prio=None, flow=None):
        # the specific Rest endpoint for the artifact
        self._ghurl = ghurl

        # objects with a lower prio are executed first e.g. the repository before a label
        self._prio = prio

        # assigned flow for the specific object.
        self._flow = flow

        # keep all the necessary values
        self._payload = {}

    @property
    def ghurl(self):
        return self._ghurl

    @ghurl.setter
    def ghurl(self, url):
        self._ghurl = url

    @property
    def prio(self):
        return self._prio

    @prio.setter
    def prio(self, prio):
        self._prio = prio

    @property
    def flow(self):
        return self._flow

    @flow.setter
    def flow(self, flow):
        self._flow = flow

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload.update(payload)

    def getjsonpayload(self):
        ''' Returns the json representation of the payload of all non private values '''
        return json.dumps(self.payload)


class GitHubRepository(GitHubArtifact):
    ''' Class represents a repository on the GitHub platform '''

    def __init__(self, name, description, private=False, org=None):
        super(GitHubRepository, self).__init__(prio=1, flow=githubdataflow.RepositoryFlow)
        # distinguish between a user and a org repo
        url = 'user/repos' if org is None else 'orgs/{}/repos'.format(org)
        self.ghurl = url


        self.payload = {'name': name, 'description': description, 'private': private, 'homepage': '', 'has_issues':True,
                            'has_wiki': True, 'has_downloads': True, 'auto_init': False, 'licence_template': ''}



    """
    payload = {
        "name": "Test-World1",
        "description": "This is your first repository",
        "homepage": "https://github.com",
        "private": false,
        "has_issues": true,
        "has_wiki": true,
        "has_downloads": true,
        "auto_init": false,
        "license_template": "mit",

        "files": {
            "Readme.md": {
                "Content": "This is a test",
                "Path": ""
            },
            "Meeting_Minutes.md": {
                "Content": "Second test",
                "Path": ""
            },
            "Documents.md": {
                "Content": "Put your documents into this folder",
                "Path": "Documents/"
            },
            "Team.md": {
                "Content": "Our superb team",
                "Path": "Team/"
            }
        }
    }
    """


class GitHubFile(GitHubArtifact):
    ''' Representing a single file object on the GitHub platform'''
    def __init__(self, name, repo_owner, repo_name, content, path):
        super(GitHubFile, self).__init__()
        # file url
        url = 'repos/{}/{}/git/blobs'.format(repo_owner, repo_name)

        self.ghurl = url
        self.prio = 2

        self.payload = {name: {'Content': content, 'Path': path}}


class GitHubLabel(GitHubArtifact):
    ''' Representing a label object which is assigned to issues on the GitHub platform '''
    """
    payload = {"repo_owner": "",
               "repo_name": "",
               "labels": [
                   {
                       "name": "bug",
                       "color": "f29513"
                   },
                   {
                       "name": "testing",
                       "color": "f29513"
                   }
               ]
               }
    """
    def __init__(self, repo_owner, repo_name, name, color):
        super(GitHubLabel, self).__init__()
        # label url
        url = 'repos/{}/{}/labels'.format(repo_owner, repo_name)

        self.ghurl = url
        self.prio = 2

        self.payload = {"name": name, "color": color}



class GitHubIssue(GitHubArtifact):

    def __init__(self):
        pass



