from brownie.test import given, strategy
from brownie import accounts
import pytest


def setup():
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


# @pytest.mark.parametrize('user', accounts[0:4])
def test_fund_existing_crowdsale(ethercrowd, accounts):
    # Init
    crowdId = 0
    expected = 10 #montant qui va etre mit

    # Call
    fund(0)
    result = ethercrowd.getFundRaise(crowdId) #montant qui a ete mit

    # Assert
    assert expected == result


# @pytest.mark.parametrize('user', accounts[0:4])
def test_fund_non_existing_crowdsale(ethercrowd, accounts):
    # Init
    crowdId = -404
    expected = 0 #= #montant qui va etre mit

    # Call
    fund(crowdId)

    resultInvestedCrowdsaleList # verifie si la crowd a été ajouté dans ses crowds investit
    result = ethercrowd.getFundRaise(crowdId)#= #montant qui a ete mit
    # Assert
    assert expected == result
    
    # @pytest.mark.parametrize('user', accounts[0:4])
def test_fund_existing_crowdsale_no_money(ethercrowd, accounts):
    # Init
    crowdId = 0
    expected = 0 #= #montant qui va etre mit

    # Call
    fund(crowdId)

    resultInvestedCrowdsaleList # verifie si la crowd a été ajouté dans ses crowds investit
    result = ethercrowd.getFundRaise(crowdId)#= #montant qui a ete mit
    # Assert
    assert expected == result