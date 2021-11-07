from brownie import accounts, reverts
import pytest

@pytest.fixture(autouse=True)
def setup(fn_isolation, ethercrowd, accounts):
    goal_amount = 10
    title = "My awesome project"
    slogan = "My awesome slogan"
    website_url = "https://myAwesomeWebsiteUrl.org"
    video_url = "https://myAwesomeVideoUrl.org"
    thumbnail_url = "https://myAwesomeThumbnailUrl.org"
    description = "My awesome description"
    end_date = 1

    ethercrowd.createProject(goal_amount, title, slogan, website_url,
                             video_url, thumbnail_url, description, end_date, {
                                 'from': accounts[0],
                                 "value": 1
                             })
    
    ethercrowd.fund(0, {'from': accounts[0], "value": 5})
    ethercrowd.fund(0, {'from': accounts[1], "value": 10})
    ethercrowd.fund(0, {'from': accounts[2], "value": 15})
    ethercrowd.fund(0, {'from': accounts[3], "value": 20})


def test_refund_contributors(ethercrowd, accounts):
    # Init
    projectId = 0
    nbOfContributors = 4
    #project = ethercrowd.getProject(projectId)
    expected = [0,0,0,0]

    # Call
    ethercrowd.refund(projectId)

    result = []
    for i in range(nbOfContributors):
        investedAmounts = ethercrowd.getInvestedFunds(projectId, {'from': accounts[i]})
        result.append(investedAmounts)

    # Assert
    assert expected == result


#Est ce prcq je serais en train de modifier la copie du projet et pas le projet lui meme ?
'''
E       assert [0, 0, 0, 0] == [5, 10, 15, 20]
E         At index 0 diff: 0 != 5
E         Use -v to get the full diff

tests\EtherCrowd\test_refund_contributors.py:43: AssertionError
'''