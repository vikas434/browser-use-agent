from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")
URL = "https://civic-info-frontend.vercel.app/"

api_key = os.getenv("GEMINI_API_KEY")

# Initialize the model
llm_gemini = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))


browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    )
)

async def main():
    agent = Agent(
        task="Open this https://civic-info-frontend.vercel.app/ and once page is loaded search for Donald Trump",
        llm=llm_gemini,
        browser=browser
    )
    result = await agent.run()
    print(result)

asyncio.run(main())