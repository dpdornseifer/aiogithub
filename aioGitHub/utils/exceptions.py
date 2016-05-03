class GitHubRequestException(Exception):

    def __init__(self, *args, **kwargs):
        super(GitHubRequestException, self).__init__(*args, **kwargs)


class NonValidArtifcatException(Exception):

    def __init__(self, *args, **kwargs):
        super(NonValidArtifcatException, self).__init__(*args, **kwargs)