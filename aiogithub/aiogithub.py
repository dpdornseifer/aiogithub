import asyncio
import aiohttp
from .utils import githublogger


class AioGitHub:


    def __init__(self, ghhost, repoowner):
        self._githubhost = None
        self._githubclient = None
        self._loop = asyncio.get_event_loop()
        self._logger = githublogger.setup_github_logger('root')


        # repository specific
        self._repoowner = None
        self._reponame = None

        self._ghartifacts = []



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
        """ Creates a GitHub client object based on the authentication data """
        self._githubclient = githubclient

    @property
    def payload(self):
        return self._ghartifacts

    @payload.setter
    def payload(self, payload):
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



    def addghartifact(self,name, artifact):
        self._ghartifacts.append(artifact)

    def get_priority_dict(self):
        """ Returns a dict with lists containing the artifacts. Keys are the priorities """

        prio_dict = {}
        for ghartifact in self._ghartifacts:
            if ghartifact.prio in prio_dict.keys():
                prio_dict[ghartifact.prio].append(ghartifact)
            else:
                prio_dict[ghartifact.prio] = [ghartifact]

        return prio_dict


    async def create(self):
        ''' do single post requests '''
        # hashmap to keep track of the different responses
        response_dict = {}

        # get artifacts in priority order
        prio_dict = self.get_priority_dict()


        for prio in sorted(prio_dict.keys()):

            for artifact in prio_dict[prio]:


                response = await self.githubclient.request('POST', artifact.ghurl, artifact.getjsonpayload)
                response_dict[prio] = await response.json()



        # apply all objects / artifacts to the github platform

        # ghclient.request('POST', url, data=)
        # 1 get prio order
        # apply - blocking between prios

        #for all:
