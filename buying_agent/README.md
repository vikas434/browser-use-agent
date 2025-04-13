# Buying Agent

A specialized agent for automating online shopping tasks using browser automation.

## Features

- Automated product search and comparison
- Price monitoring and alerts
- Shopping cart management
- Checkout automation
- Support for multiple e-commerce platforms

## Directory Structure

```
buying_agent/
├── __init__.py
├── buying_agent.py      # Main agent implementation
├── utils/              # Utility functions and helpers
│   └── __init__.py
└── tests/              # Test cases
    └── __init__.py
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

## Usage

```python
from buying_agent import BuyingAgent

# Initialize the agent
agent = BuyingAgent()

# Example: Search for a product
results = agent.search_product("laptop", max_price=1000)

# Example: Monitor price
agent.monitor_price(product_url="https://example.com/product", target_price=500)
```

## Testing

Run tests with:
```bash
pytest buying_agent/tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 