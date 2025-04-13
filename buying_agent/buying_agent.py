from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
import dotenv
import os
from datetime import datetime
dotenv.load_dotenv()

# Create output directory if it doesn't exist
docs_dir = "grocery_purchase_results"
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
    Help purchase Fortune Basmati Rice 5kg by comparing prices on Flipkart Minutes and Amazon Fresh.
    
    Follow these steps:
    
    1. Open a new tab and go to Flipkart Grocery/Minutes (flipkart.com):
       - Search for "Fortune Basmati Rice 5kg"
       - Take a screenshot of the search results
       - Note the exact product name, price, and delivery fee/timeline
       - Check if there are any ongoing discounts or offers
       - Take a screenshot of the product details page
    
    2. Open another new tab and go to Amazon Fresh (amazon.in):
       - Search for "Fortune Basmati Rice 5kg"
       - Take a screenshot of the search results
       - Note the exact product name, price, and delivery fee/timeline
       - Check if there are any ongoing discounts or offers
       - Take a screenshot of the product details page
    
    3. Compare the prices and offers between both platforms:
       - Calculate the total price including delivery fees
       - Consider delivery time and any membership benefits
       - Determine which platform offers the better deal
    
    4. For the platform with the better price:
       - Add the Fortune Basmati Rice 5kg to the cart
       - Take a screenshot of the cart
       - Proceed to checkout
       - Take a screenshot of the checkout page
       - Stop at the payment selection page (do not enter any payment details)
    
    5. Compile a brief report with:
       - A comparison table showing prices on both platforms
       - The decision on which platform offers the better deal and why
       - Screenshots of the product pages, cart, and checkout process
    
    Save all screenshots to the 'grocery_purchase_results' folder with descriptive filenames.
    
    IMPORTANT: 
    - Use new tabs in the existing browser window
    - Do not actually complete any purchase
    - For Flipkart, try to use Flipkart Grocery or Flipkart Minutes if available
    - For Amazon, specifically look at Amazon Fresh products when available
    - If the exact 5kg package is not available, find the closest alternative
    """,
    llm=ChatOpenAI(model='gpt-4o'),
    browser=browser,
)

async def main():
    print(f"Starting grocery price comparison at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Agent is comparing Fortune Basmati Rice 5kg prices between Flipkart Minutes and Amazon Fresh...")
    
    result = await agent.run()
    
    print("\nGrocery comparison and cart process complete!")
    print(f"Results saved to the '{docs_dir}' directory")
    print("Summary of findings:")
    print(result)
    
    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())