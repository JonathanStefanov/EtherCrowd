from brownie.test import given, strategy
from brownie import accounts, reverts
import pytest

@pytest.fixture(autouse=True)
def setup(fn_isolation, ethercrowd, accounts):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    goal_amount = 10
    title = "Test crowdsale"
    slogan = "Test slogan"
    website_url = "https://ethereum.org"
    video_url = website_url
    thumbnail_url = website_url
    description = "Test description"
    start_date = 10
    end_date = 20

    # Creating the crowdsale
    ethercrowd.createCrowdsale(
        goal_amount,
        title,
        slogan,
        website_url,
        video_url,
        thumbnail_url,
        description,
        start_date,
        end_date,
        {'from': accounts[0], "value": 1}
    )  # TODO: global test fee variable


def test_fund_existing_crowdsale(ethercrowd, accounts):
    # Init
    crowdId = 0
    expected = 10  # montant qui va etre mit

    # Call
    ethercrowd.fund(0, {'from': accounts[0], "value": 10})
    result = ethercrowd.getInvestedFunds(crowdId)  # montant qui a ete mit

    # Assert
    assert expected == result
    


def test_fund_existing_crowdsale_no_money(ethercrowd, accounts):
    # Init
    crowdId = 0
    expected = 0  # = #montant qui va etre mit

    # Call
    with reverts("No value sent."):
        ethercrowd.fund(crowdId, {'from': accounts[0], "value": 0})

    # resultInvestedCrowdsaleList # verifie si la crowd a été ajouté dans ses crowds investit
    result = ethercrowd.getInvestedFunds(crowdId)  # = #montant qui a ete mit

    # Assert
    assert expected == result


def test_fund_non_existing_crowdsale(ethercrowd, accounts):
    # Init
    crowdId = 404
    expected = 0  # = #montant qui va etre mit

    # Call
    with reverts("Crowd does not exist."):
        ethercrowd.fund(crowdId, {'from': accounts[0], "value": 10})


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


