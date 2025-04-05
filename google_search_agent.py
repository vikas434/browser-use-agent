from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
import dotenv
dotenv.load_dotenv()

# Define the target URL
JIRA_URL = "https://knowledge-gain-ai.atlassian.net/jira/software/projects/MP/boards/2"

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless=False,
    )
)

# Create the agent with your configured browser
agent = Agent(
    task=f"Open a new tab and navigate to {JIRA_URL}",
    llm=ChatOpenAI(model='gpt-4'),
    browser=browser
)

async def main():
    try:
        result = await agent.run()
        print("Navigation completed!")
        print("Result:", result)
        
        input('Press Enter to close the browser tab...')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())