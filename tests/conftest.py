from brownie import accounts, config, EtherCrowd
import pytest

# CONSTANTS TODO make it a separate file
FEE = 1
CHECK_INTERVAL = 86400 # nbr of seconds in a day

@pytest.fixture(scope='module')
def owner():
    yield accounts[0]

@pytest.fixture(scope='module')
def ethercrowd(owner):
    yield EtherCrowd.deploy(
        FEE,
        CHECK_INTERVAL,
        {'from': owner},
    )

@pytest.fixture(autouse=True)
def setup(fn_isolation):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    pass