import asyncio
from aiogithub import githubartifacts as ghartf
from aiogithub import githubclient as ghclient
from aiogithub import AioGitHub



async def main():
    # assemble aiogithub object
    public_gh_root = 'api.github.com'
    aiogh = AioGitHub(public_gh_root, '')
    client = ghclient.GitHubClient(public_gh_root, '', '')

    # ask github for user infos
    user_info = await client.request('GET', 'user')
    user_info_json = await user_info.json()
    print(user_info_json)

    # assign client object to githubartifact
    aiogh.githubclient = client

    # add a new gitubrepository object
    repo = ghartf.GitHubRepository('test', 'my test repo')
    aiogh.addghartifact(repo)

    # execute the flow
    #await aiogh.apply()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())