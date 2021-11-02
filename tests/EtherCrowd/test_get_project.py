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


def test_get_existing_project(ethercrowd, accounts):
     # Init
    projectId = 0
    expected = True

    project = None

    # Call
    project = ethercrowd.getProject(projectId)

    result = project != None

    # Assert
    assert expected == result


def test_get_non_existing_project(ethercrowd, accounts):
     # Init
    projectId = 404
    expected = False

    project = None

    # Call
    with reverts("Project does not exist."):
        project = ethercrowd.getProject(projectId)

    result = project != None

    # Assert
    assert expected == result