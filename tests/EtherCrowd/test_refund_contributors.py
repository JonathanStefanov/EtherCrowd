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
    print("BALANCE BEFORE " + str(accounts[0].balance()))
    ethercrowd.fund(0, {'from': accounts[0], "value": 5})
    print(accounts[0].balance())

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

