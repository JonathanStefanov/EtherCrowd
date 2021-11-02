from brownie.test import given, strategy
from brownie import accounts, reverts
import pytest

@pytest.fixture(autouse=True)
def setup(fn_isolation, ethercrowd, accounts):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    # Maybe define expected and result for more visibility
    goal_amount = 10
    title = "Test project"
    slogan = "Test slogan"
    website_url = "https://ethereum.org"
    video_url = website_url
    thumbnail_url = website_url
    description = "Test description"
    end_date = 120

    ethercrowd.createProject(
        goal_amount,
        title,
        slogan,
        website_url,
        video_url,
        thumbnail_url,
        description,
        end_date,
         {'from': accounts[0], "value": 1}) # TODO: global test fee variable


def test_fund_existing_project(ethercrowd, accounts):
    # Init
    projectId = 0
    expected = 10  # montant qui va etre mit

    # Call
    ethercrowd.fund(0, {'from': accounts[0], "value": 10})
    result = ethercrowd.getInvestedFunds(projectId)  # montant qui a ete mit

    # Assert
    assert expected == result
    


def test_fund_existing_project_no_money(ethercrowd, accounts):
    # Init
    projectId = 0
    expected = 0  # = #montant qui va etre mit

    # Call
    with reverts("No value sent."):
        ethercrowd.fund(projectId, {'from': accounts[0], "value": 0})

    # resultInvestedCrowdsaleList # verifie si la crowd a été ajouté dans ses crowds investit
    result = ethercrowd.getInvestedFunds(projectId)  # = #montant qui a ete mit

    # Assert
    assert expected == result


def test_fund_non_existing_project(ethercrowd, accounts):
    # Init
    projectId = 404
    expected = 0  # = #montant qui va etre mit

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


