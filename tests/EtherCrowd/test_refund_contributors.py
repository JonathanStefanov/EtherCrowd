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
    
    ethercrowd.fund(0, {'from': accounts[0], "value": 5})
    ethercrowd.fund(0, {'from': accounts[1], "value": 10})
    ethercrowd.fund(0, {'from': accounts[2], "value": 15})
    ethercrowd.fund(0, {'from': accounts[3], "value": 20})


def test_refund_contributors(ethercrowd, accounts):
    # Init
    projectId = 0
    nbOfContributors = 4
    expected = 0

    # Call
    ethercrowd.refund(0)
    result = True
     
    # add a for loop for()
    ethercrowd.getInvestedFunds(projectId, {'from': account})  # montant qui a ete mit

    # Assert
    assert expected == result
