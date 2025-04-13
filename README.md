# Browser Use Agent

A demonstration of browser automation using the Browser Use framework.

## Project Structure

- `browser_agent/`: Basic browser automation examples
  - `simple_agent.py`: Simple browser automation demo
  - `google_search_agent.py`: Google search automation
  - `agent.py`: Generic browser automation agent

- `jira_agent/`: Jira automation examples
  - `jira_agent.py`: Main Jira automation script
  - `jira_test_creation_agent.py`: Jira ticket creation automation
  - `Vikas_CV_1.pdf`: Sample CV for testing

- `job_search_agent/`: Job search automation
  - `read_apply_job.py`: Automated job application script

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

Each directory contains its own set of scripts. Navigate to the desired directory and run the script:

```bash
# For browser automation
cd browser_agent
python simple_agent.py

# For Jira automation
cd jira_agent
python jira_agent.py

# For job search automation
cd job_search_agent
python read_apply_job.py
```

## Features

- Browser automation using Browser Use framework
- Support for both OpenAI and Google Gemini models
- Real Chrome browser integration
- Automated web navigation
- Jira ticket management
- Automated job application
