from .githubgitdatatools import *
from .exceptions import GitHubRequestException
from abc import abstractmethod

class GitHubFlow:

    @staticmethod
    @abstractmethod
    async def executeflow(self, *args, **kwargs):
        ''' Orchestrates the API calls for the specific GitHub artifact '''


class RepositoryFlow(GitHubFlow):

    @staticmethod
    async def executeflow(ghclient, githubrepository):

        try:
            repositoryflow_json = await ghrequest(ghclient=ghclient,
                                                  method='POST',
                                                  repo_url=githubrepository.ghurl,
                                                  payload=githubrepository.getjsonpayload())

        except GitHubRequestException as e:
            logger.error(" An exception occurred while processing the RepositoryFlow: {}".format(e))

        return repositoryflow_json



class FileFlow(GitHubFlow):

    def __init__(self, files):
        pass

    @staticmethod
    def executeflow(self, *args, **kwargs):
        pass






class LabelFlow(GitHubFlow):
    def __init__(self):
        pass

    @staticmethod
    def executeflow(self, *args, **kwargs):
        pass



class TeamFlow(GitHubFlow):

    def __init__(self):
        pass