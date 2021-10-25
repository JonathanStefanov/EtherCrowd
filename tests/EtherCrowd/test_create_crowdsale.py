from brownie.test import given, strategy
from brownie import accounts
import pytest

#@pytest.mark.parametrize('user', accounts[0:4])
def test_crowdsale_happy_path(ethercrowd, accounts):
    # Maybe define expected and result for more visibility
    goal_amount = 10
    title = "Test crowdsale"
    slogan = "Test slogan"
    website_url = "https://ethereum.org"
    video_url = website_url
    thumbnail_url = website_url
    description = "Test description"
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
        end_date,
         {'from': accounts[0], "value": 1}) # TODO: global test fee variable

    
    # Getting the crowdsale
    assert accounts[0] == ethercrowd.getCrowdsale(0)

