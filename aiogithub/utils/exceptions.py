class GitHubRequestException(Exception):
    ''' Collect different kind of HTTP exceptions in on GitHub exception'''
    def __init__(self, *args, **kwargs):
        super(GitHubRequestException, self).__init__(*args, **kwargs)


class NonValidArtifcatException(Exception):
    ''' Is thrown when objects should be applied to GitHub which have not been derived from GitHubArtifcat'''

    def __init__(self, *args, **kwargs):
        super(NonValidArtifcatException, self).__init__(*args, **kwargs)