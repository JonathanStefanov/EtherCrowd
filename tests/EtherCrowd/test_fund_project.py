from brownie.test import given, strategy
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
    end_date = 3600

    ethercrowd.createProject(goal_amount, title, slogan, website_url,
                             video_url, thumbnail_url, description, end_date, {
                                 'from': accounts[0],
                                 "value": 1
                             })


def test_fund_existing_project(ethercrowd, accounts):
    # Init
    projectId = 0
    expectedProjectFunds = 10
    expectedContributorAdded = True

    expectedInvestedFunds = 10
    expectedContributedProject = [projectId]


    # Call
    ethercrowd.fund(0, {'from': accounts[0], "value": 10})

    resultProjectFunds = ethercrowd.getProjectFunds(projectId)

    # NOT WORKING WHY ???
    #contributors = ethercrowd.getProjectContributors[0]
    #resultContributorAdded = accounts[0].address == contributors[0]

    resultContributedProject = ethercrowd.getContributedProject()
    resultInvestedFunds = ethercrowd.getInvestedFunds(projectId)


    # Asserts
    assert expectedProjectFunds == resultProjectFunds
    #assert expectedContributorAdded == resultContributorAdded
    assert expectedContributedProject == resultContributedProject
    assert expectedInvestedFunds == resultInvestedFunds 
    


def test_fund_existing_project_no_money(ethercrowd, accounts):
    # Init
    projectId = 0
    expectedInvestedFunds = 0
    expectedProjectFunds = 0
    expectedContributorAdded = False
    expectedContributedProject = []

    # Call
    with reverts("No value sent."):
        ethercrowd.fund(projectId, {'from': accounts[0], "value": 0})
    
    resultProjectFunds = ethercrowd.getProjectFunds(projectId)

    # NOT WORKING WHY ???
    #contributors = ethercrowd.getProjectContributors[0]
    #resultContributorAdded = accounts[0].address == contributors[0]

    resultContributedProject = ethercrowd.getContributedProject()
    resultInvestedFunds = ethercrowd.getInvestedFunds(projectId)

    # Asserts
    assert expectedProjectFunds == resultProjectFunds
    #assert expectedContributorAdded == resultContributorAdded
    assert expectedContributedProject == resultContributedProject
    assert expectedInvestedFunds == resultInvestedFunds 



def test_fund_non_existing_project(ethercrowd, accounts):
    # Init
    projectId = 404
    expected = 0

    # Call
    with reverts("Project does not exist."):
        ethercrowd.fund(projectId, {'from': accounts[0], "value": 10})


# TODO when Jona will finish the isActive implementation
"""
def test_fund_non_active_crowdsale(ethercrowd, accounts):
    # Init
    crowdId = 1
    expected = 0 #= #montant qui va etre mit

    # Call
    with reverts("Crowd is not active."):
        ethercrowd.fund(crowdId, {'from': accounts[0], "value": 10})

    #resultInvestedCrowdsaleList # verifie si la crowd a été ajouté dans ses crowds investit
    result = ethercrowd.getInvestedFunds(crowdId)#= #montant qui a ete mit
    
    # Assert
    assert expected == result
"""


