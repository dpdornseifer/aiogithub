import asyncio
import aiohttp
from aiogithub.utils.exceptions import NonValidArtifcatException
from aiogithub.githubartifacts import GitHubArtifact
from .utils import githublogger


class AioGitHub:


    def __init__(self, ghhost, repoowner, logger=None):
        self._githubhost = None
        self._githubclient = None
        self._loop = asyncio.get_event_loop()

        # use default aiogithub logger if no other is given
        self._logger = githublogger.setup_github_logger('root') if logger is None else logger

        # repository specific
        self._repoowner = None
        self._reponame = None




        self._ghartifacts = []

        self._responses = {}

    @property
    def loop(self):
        return self._loop

    @property
    def githubhost(self):
        return self._githubhost

    @githubhost.setter
    def githubhost(self, githubhost):
        self._githubhost = githubhost

    @property
    def githubclient(self):
        return self._githubclient

    @githubclient.setter
    def githubclient(self, githubclient):
        ''' Creates a GitHub client object based on the authentication data '''
        self._githubclient = githubclient

    @property
    def ghartifacts(self):
        return self._ghartifacts

    @ghartifacts.setter
    def ghartifacts(self, payload):
        self._ghartifacts = payload

    @property
    def repoowner(self):
        return self._repoowner

    @repoowner.setter
    def repoowner(self, repoowner):
        self._repoowner = repoowner

    @property
    def reponame(self):
        return self._reponame

    @reponame.setter
    def reponame(self, reponame):
        self._reponame = reponame

    def addghartifact(self, artifact):
        self._ghartifacts.append(artifact)

    def artifactsvalid(self):
        ''' Check if all the objects in the artifcats list are inherited from GitHubArtifcat to make sure they can be applyed '''

        for artifact in self._ghartifacts:
            if not isinstance(artifact, GitHubArtifact):
                return False
        return True

    def get_priority_dict(self):
        ''' Returns a dict with lists containing the artifacts. Keys are the priorities '''

        prio_dict = {}
        for ghartifact in self._ghartifacts:
            if ghartifact.prio in prio_dict.keys():
                prio_dict[ghartifact.prio].append(ghartifact)
            else:
                prio_dict[ghartifact.prio] = [ghartifact]
        return prio_dict

    def get_tasks(self, artifacts):
        ''' Returns a list with asyncio tasks '''

        tasks = list()
        for artifact in artifacts:
            flow = artifact.flow
            tasks.append(flow.executeflow(self.githubclient, artifact))
        return tasks

    async def apply(self, commit_msg=None, branch='master'):
        ''' Apply all GitHub artifacts to the GitHub platform / to the destination repository '''

        if not self.artifactsvalid():
            raise NonValidArtifcatException()

        priority_dict = self.get_priority_dict()

        # iterate of the dict and execute the flows in the order of the priorities
        for key in sorted(priority_dict.keys()):
            # return asyncio tasks
            tasks = self.get_tasks(priority_dict[key])

            # execute the flows in parallel
            for response in await asyncio.ensure_future(tasks[0]):
                self._responses[key] = response

