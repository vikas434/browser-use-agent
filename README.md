# Browser Use Agent

A demonstration of browser automation using the Browser Use framework.

## Setup

1. Clone the repository:
```bash
git clone git@github.com:vikas434/browser-use-agent.git
cd browser-use-agent
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

4. Create a `.env` file with your API keys:
```bash
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here  # Optional, if using Gemini
```

## Usage

Run the simple agent:
```bash
python simple_agent.py
```

## Features

- Browser automation using Browser Use framework
- Support for both OpenAI and Google Gemini models
- Real Chrome browser integration
- Automated web navigation
