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


#TODO check why if a change msg.value to another value -> error 
def test_get_all_projects(ethercrowd, accounts):
    # Init

    ethercrowd.createProject(10, "Your awesome project", "Your awesome slogan",
                             "https://yourAwesomeWebsiteUrl.org",
                             "https://yourAwesomeVideoUrl.org",
                             "https://yourAwesomeThumbnailUrl.org",
                             "Your awesome description", 1800, {
                                 'from': accounts[1],
                                 "value": 1
                             })

    ethercrowd.createProject(10, "His awesome project", "His awesome slogan",
                             "https://hisAwesomeWebsiteUrl.org",
                             "https://hisAwesomeVideoUrl.org",
                             "https://hisAwesomeThumbnailUrl.org",
                             "His awesome description", 900, {
                                 'from': accounts[2],
                                 "value": 1
                             })

    expected = 3

    project = None

    # Call
    projects = ethercrowd.getProjects()

    result = len(projects)

    # Assert
    assert expected == result