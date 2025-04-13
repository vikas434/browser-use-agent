import pytest
from buying_agent.buying_agent import BuyingAgent

@pytest.fixture
def agent():
    return BuyingAgent()

def test_agent_initialization(agent):
    assert agent is not None
    assert hasattr(agent, 'browser')
    assert hasattr(agent, 'search_product')
    assert hasattr(agent, 'monitor_price')

def test_search_product(agent):
    # Mock the search functionality
    results = agent.search_product("test product", max_price=100)
    assert isinstance(results, list)

def test_monitor_price(agent):
    # Mock the price monitoring
    success = agent.monitor_price(
        product_url="https://example.com/product",
        target_price=50
    )
    assert isinstance(success, bool) 