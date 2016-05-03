import logging
import json
from .exceptions import GitHubRequestException


logger = logging.getLogger('root')

async def ghrequest(ghclient, method, repo_url, payload):
    ''' do a simple post request '''
    try:
        response = await ghclient.request(method=method, url=repo_url, data=payload)
        if response.status == 200:
            ghrequest_jsonresponse = await response.json()
        else:
            ghrequest_jsonresponse = 'An error occurred'

    except TimeoutError as te:
        logger.error(" An TimeoutError occurred while processing a {} request: {}".format(method, te))
        raise GitHubRequestException(te)

    except Exception as e:
        logger.error(" An exception occurred while processing a {} request: {}".format(method, e))
        raise GitHubRequestException(e)

    logger.info(" The POST request response looks like: {}".format(ghrequest_jsonresponse))
    return ghrequest_jsonresponse


async def gethead(ghclient, repo_owner, repo_name):
    ''' get reference to HEAD '''

    head_url = 'repos/{!s}/{!s}/git/refs/heads/master'.format(repo_owner, repo_name)
    head_response = await ghclient.request('GET', head_url)
    head_jsonresponse = await head_response.json()

    logger.info(" The Head ref for the rew repo is: {}".format(head_jsonresponse))
    return head_jsonresponse


async def getcommitobject(ghclient, head_jsonresponse):
    ''' get the commit object '''

    commitobject_url = head_jsonresponse['object']['url']
    commitobject_response = await ghclient.request('GET', commitobject_url)
    commitobject_jsonresponse = await commitobject_response.json()

    logger.info(" The commit object for the new repo is: {}".format(commitobject_jsonresponse))
    return commitobject_jsonresponse


def assembleblobs(files):
    ''' assemble the blobs '''
    blobs = {}
    for key, value in files.items():
        blobs[key] = value["Content"]

    logger.info(" List of blobs has been assembled {!r}".format(blobs))
    return blobs


async def uploadblobs(ghclient, blobs, repo_owner, repo_name, blobs_payload):
    ''' upload the blobs to the github platform and '''
    blobs_url = 'repos/{!s}/{!s}/git/blobs'.format(repo_owner, repo_name)
    # TODO parallel execution (for loop)
    blobs_responses = {}
    for key, value in blobs.items():

        # build individual payload for each blob
        blobs_payload = {"encoding": "utf-8"}
        blobs_payload.update({"content": value})
        logger.info(" Blobs payload: {!r}".format(blobs_payload))

        blob_response = await ghclient.request('POST', blobs_url, data=blobs_payload)
        blob_jsonresponse = await blob_response.json()

        # blobs responses necessary to attach files to tree later
        blobs_responses.update({key: blob_jsonresponse})

    logger.info(" Json response for POST blob request: {!r}".format(str(blobs_responses)))
    return blobs_responses


async def gettree(ghclient, commitobject_jsonresponse):
    ''' get the tree object for the 'HEAD' commit '''
    tree_url = commitobject_jsonresponse['tree']['url']
    tree_response = await ghclient.request('GET', tree_url)
    tree_jsonresponse = await tree_response.json()

    logger.info(" The treeobject for the 'HEAD' commit is: {!r}".format(tree_jsonresponse))
    return tree_jsonresponse


def assemblenewtree(tree_jsonresponse, blobs_responses, files):
    ''' assemble a new tree object containing the files '''

    newtree = {'base_tree': tree_jsonresponse['sha']}
    newtree_array = []

    for key, value in blobs_responses.items():
        newtree_object = {'path': files[key]['Path'] + key,
                          'mode': "100644",
                          'type': "blob",
                          'sha': value['sha']
                          }
        newtree_array.append(newtree_object)

    # put together the final tree
    newtree.update({'tree': newtree_array})

    logger.info(" The tree object looks like {!r}".format(str(newtree)))
    return newtree


async def uploadnewtree(ghclient, repo_owner, repo_name, newtree):
    ''' upload the new tree '''

    newtree_url = 'repos/' + repo_owner + '/' + repo_name + '/git/trees'
    newtree_response = await ghclient.request('POST', newtree_url, data=newtree)
    newtree_jsonresponse = await newtree_response.json()

    logger.info(" A new tree has been posted: {!r}".format(newtree_jsonresponse))
    return newtree_jsonresponse


def assemblenewcommit(commitobject_jsonresponse, newtree_jsonresponse):
    ''' assemble a new commit object in '''

    newcommit = {'message': "Project template",
                 'parents': [commitobject_jsonresponse['sha']],
                 'tree': newtree_jsonresponse['sha']
                 }

    logger.info(" The new commit object created: {!r}".format(str(newcommit)))
    return newcommit

async def uploadnewcommit(ghclient, repo_owner, repo_name, newcommit):
    ''' post the new commit object to the server '''

    newcommit_url = 'repos/{!s}/{!s}/git/commits'.format(repo_owner, repo_name)
    newcommit_response = await ghclient.request('POST', newcommit_url, data=newcommit)
    newcommit_jsonresponse = await newcommit_response.json()

    logger.info(" A new commit has been posted: {!r}".format(newcommit_jsonresponse))
    return newcommit_jsonresponse


async def executeheadupdate(ghclient, head_url, newcommit_jsonresponse):
    ''' update the HEAD reference on GitHub to point to the new commit '''

    headupdate_url = head_url
    headupdate = json.dumps({'sha': newcommit_jsonresponse['sha'],
                  'force': "true"})

    # patch the reference on GitHub with the new commit
    headupdate_response = await ghclient.request('PATCH', headupdate_url, data=headupdate)
    headupdate_jsonresponse = await headupdate_response.json()

    logger.info(" A new reference update was posted: {!r}".format(headupdate_jsonresponse))
    return headupdate_jsonresponse


async def createnewbranch(ghclient, repo_owner, repo_name, branch_name, head_jsonresponse):
    ''' create a new branch on the github repository'''

    newbranch_url = 'repos/{!s}/{!s}/git/refs'.format(repo_owner, repo_name)
    newbranch = {'ref': 'refs/heads/{}'.format(branch_name),
                 'sha': head_jsonresponse['object']['sha']
                 }
    newbranch_response = await ghclient.request('POST', newbranch_url, data=json.dumps(newbranch))
    newbranch_jsonresponse = await newbranch_response.json()

    logger.info("A new branch has been created: {!r}".format(newbranch_jsonresponse))
    return newbranch_jsonresponse
