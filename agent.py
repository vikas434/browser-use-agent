from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
import dotenv
import os
from datetime import datetime
dotenv.load_dotenv()

# Create documentation directory if it doesn't exist
docs_dir = "website_documentation"
if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

# Create the agent with your configured browser
agent = Agent(
    task="""
    Explore and document the website at https://civic-info-frontend.vercel.app/ thoroughly.
    
    Follow these steps in your exploration:
    1. Start by visiting the homepage and capture a screenshot.
    2. Identify all main navigation elements (menu items, buttons, links).
    3. Systematically explore each section of the website by clicking on navigation elements.
    4. For each page you visit:
       - Take a screenshot
       - Record the page title and main headings
       - Document all interactive elements (buttons, forms, links)
       - Note the purpose and functionality of the page
    5. Test any forms or interactive elements you encounter (without submitting personal information).
    6. Document the user flow between pages.
    
    Generate comprehensive documentation that includes:
    - A site map showing the relationship between pages
    - Step-by-step instructions for common user journeys
    - Detailed descriptions of UI elements and their functions
    - Screenshots of each important page and feature
    
    Save all screenshots to the 'website_documentation' folder with descriptive filenames.
    
    Compile all findings into a markdown document that provides a complete user guide to the website.
    """,
    llm=ChatOpenAI(model='gpt-4o'),
    browser=browser,
)

async def main():
    print(f"Starting website documentation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target website: https://civic-info-frontend.vercel.app/")
    print("Agent is exploring the website and generating documentation...")
    
    result = await agent.run()
    
    print("\nDocumentation generation complete!")
    print(f"Results saved to the '{docs_dir}' directory")
    print("Summary of findings:")
    print(result)
    
    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())