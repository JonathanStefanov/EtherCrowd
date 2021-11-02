from brownie.test import given, strategy
from brownie import accounts
import pytest


def test_project_happy_path(ethercrowd, accounts):
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

    
    # Getting the crowdsale
    assert accounts[0] == ethercrowd.getProject(0)
    
    

