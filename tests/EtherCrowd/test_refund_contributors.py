from brownie import accounts, reverts
from brownie.network.state import Chain
import pytest

@pytest.fixture(autouse=True)
def setup(fn_isolation, ethercrowd, accounts):
    # Chain init
    chain = Chain()
    
    # Init
    goal_amount = 10
    title = "My awesome project"
    slogan = "My awesome slogan"
    website_url = "https://myAwesomeWebsiteUrl.org"
    video_url = "https://myAwesomeVideoUrl.org"
    thumbnail_url = "https://myAwesomeThumbnailUrl.org"
    description = "My awesome description"
    end_date = 86400

    ethercrowd.createProject(goal_amount, title, slogan, website_url,
                             video_url, thumbnail_url, description, end_date, {
                                 'from': accounts[0],
                                 "value": 1
                             })
    
    ethercrowd.fund(0, {'from': accounts[0], "value": 5})
    ethercrowd.fund(0, {'from': accounts[1], "value": 10})
    ethercrowd.fund(0, {'from': accounts[2], "value": 15})
    ethercrowd.fund(0, {'from': accounts[3], "value": 20})


def test_refund_contributors_success(chain, ethercrowd, accounts):
    # Init
    projectId = 0
    nbOfContributors = 4
    expected = [0,0,0,0]


    # Call
    
    print(chain.sleep(86400)) # Wait 1day
     
    ethercrowd.refund(projectId)

    result = []
    for i in range(nbOfContributors):
        investedAmounts = ethercrowd.getInvestedFunds(projectId, {'from': accounts[i]})
        result.append(investedAmounts)

    # Assert
    assert expected == result

def test_refund_contributors_error_not_yet_expired(chain, ethercrowd, accounts):
    # Init
    projectId = 0
    nbOfContributors = 4
    expected = [5,10,15,20]


    # Call
    
    print(chain.sleep(43200)) # Wait 1/2 day
     
    with reverts ("Project is not yet expired."):
        ethercrowd.refund(projectId)

    result = []
    for i in range(nbOfContributors):
        investedAmounts = ethercrowd.getInvestedFunds(projectId, {'from': accounts[i]})
        result.append(investedAmounts)

    # Assert
    assert expected == result