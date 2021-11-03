from brownie.test import given, strategy
from brownie import accounts, reverts
import pytest

def test_create_project(ethercrowd, accounts):
    # Init
    ## call variables
    goal_amount = 10
    title = "My awesome project"
    slogan = "My awesome slogan"
    website_url = "https://myAwesomeWebsiteUrl.org"
    video_url = "https://myAwesomeVideoUrl.org"
    thumbnail_url = "https://myAwesomeThumbnailUrl.org"
    description = "My awesome description"
    end_date = 3600

    ## assert variables
    projectId = 0
    expected = 1

    # Call
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

    
    result = ethercrowd.nbOfProjects()

    # Assert
    assert expected == result



def test_create_project_goal_amout_null(ethercrowd, accounts):
    # Init
    goal_amount = 0
    title = "My awesome project"
    slogan = "My awesome slogan"
    website_url = "https://myAwesomeWebsiteUrl.org"
    video_url = "https://myAwesomeVideoUrl.org"
    thumbnail_url = "https://myAwesomeThumbnailUrl.org"
    description = "My awesome description"
    end_date = 3600

    # Call and Assert
    with reverts("Goal amount must be greater than zero."):
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



def test_create_project_end_date_null(ethercrowd, accounts):
    # Init
    goal_amount = 10
    title = "My awesome project"
    slogan = "My awesome slogan"
    website_url = "https://myAwesomeWebsiteUrl.org"
    video_url = "https://myAwesomeVideoUrl.org"
    thumbnail_url = "https://myAwesomeThumbnailUrl.org"
    description = "My awesome description"
    end_date = 0

    # Call and Assert
    with reverts("End date has to be after start date."):
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