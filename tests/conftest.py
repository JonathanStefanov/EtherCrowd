from brownie import accounts, config, EtherCrowd
import pytest


@pytest.fixture(scope='module')
def owner():
    yield accounts[0]

@pytest.fixture(scope='module')
def ethercrowd(owner):
    yield EtherCrowd.deploy(
        1,
        {'from': owner},
    )

@pytest.fixture(autouse=True)
def setup(fn_isolation):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    pass