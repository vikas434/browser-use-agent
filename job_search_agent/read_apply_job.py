"""
Goal: Searches for job listings, evaluates relevance based on a CV, and applies

@dev You need to add OPENAI_API_KEY to your environment variables.
Also you have to install PyPDF2 to read pdf files: pip install PyPDF2
"""

import asyncio
import csv
import logging
import os
import sys
from pathlib import Path
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr
from PyPDF2 import PdfReader

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate required environment variables
load_dotenv()
required_env_vars = ['OPENAI_API_KEY']
for var in required_env_vars:
	if not os.getenv(var):
		raise ValueError(f'{var} is not set. Please add it to your environment variables.')

# Full screen mode
controller = Controller()

# Check multiple locations for the CV file
current_dir = Path.cwd()
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))

# Try multiple possible locations for the CV file
possible_cv_paths = [
	current_dir / 'Vikas_CV_1.pdf',  # Main directory
	script_dir / 'Vikas_CV_1.pdf',   # Script directory
	current_dir / 'jira_task_creation_results' / 'Vikas_CV_1.pdf'  # Subfolder
]

CV = None
for path in possible_cv_paths:
	if path.exists():
		CV = path
		logger.info(f"Found CV at: {CV}")
		break

if CV is None:
	raise FileNotFoundError(f'CV file not found. Please place "Vikas_CV_1.pdf" in one of these locations: {", ".join(str(p) for p in possible_cv_paths)}')


class Job(BaseModel):
	title: str
	link: str
	company: str
	fit_score: float
	location: Optional[str] = None
	salary: Optional[str] = None


@controller.action('Save jobs to file - with a score how well it fits to my profile', param_model=Job)
def save_jobs(job: Job):
	with open('jobs.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow([job.title, job.company, job.link, job.salary, job.location])

	return 'Saved job to file'


@controller.action('Read jobs from file')
def read_jobs():
	try:
		with open('jobs.csv', 'r') as f:
			return f.read()
	except FileNotFoundError:
		# Create empty jobs file if it doesn't exist
		with open('jobs.csv', 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(['Title', 'Company', 'Link', 'Salary', 'Location'])
		return "New jobs file created."


@controller.action('Read my cv for context to fill forms')
def read_cv():
	pdf = PdfReader(CV)
	text = ''
	for page in pdf.pages:
		text += page.extract_text() or ''
	logger.info(f'Read cv with {len(text)} characters')
	return ActionResult(extracted_content=text, include_in_memory=True)


@controller.action(
	'Upload cv to element - call this function to upload if element is not found, try with different index of the same upload element',
)
async def upload_cv(index: int, browser: BrowserContext):
	path = str(CV.absolute())
	dom_el = await browser.get_dom_element_by_index(index)

	if dom_el is None:
		return ActionResult(error=f'No element found at index {index}')

	file_upload_dom_el = dom_el.get_file_upload_element()

	if file_upload_dom_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	file_upload_el = await browser.get_locate_element(file_upload_dom_el)

	if file_upload_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file "{path}" to index {index}'
		logger.info(msg)
		return ActionResult(extracted_content=msg)
	except Exception as e:
		logger.debug(f'Error in set_input_files: {str(e)}')
		return ActionResult(error=f'Failed to upload file to index {index}')


# Function to create a fresh browser instance with proper configuration
def create_browser():
	# Close any existing Chrome instances (optional)
	os.system("pkill -f 'Google Chrome'")
	
	return Browser(
		config=BrowserConfig(
			chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
			headless=False,  # Use visible browser
			default_viewport={"width": 1280, "height": 800},  # Set explicit viewport size
			args=[
				"--start-maximized",  # Start with maximized window
				"--window-size=1280,800",  # Explicit window size
				"--disable-dev-shm-usage",  # Avoid issues with shared memory in Docker
				"--no-sandbox",  # Run without sandbox for compatibility
			]
		)
	)


async def main():
	# Create a fresh browser instance
	browser = create_browser()
	
	# Task definition
	ground_task = (
		'You are a professional job finder. '
		'First, read my CV using the read_cv action to understand my skills and experience. '
		'Then, search for machine learning internships at the specified company. '
		'Navigate to the company careers page, search for relevant positions, and save promising listings to a file. '
		'For each good match, create a Job object with title, company name, link, and a fit score based on my CV. '
		'Do not take screenshots as they may cause errors. '
		'Target company: '
	)
	
	tasks = [ground_task + 'Google']
	
	# Using standard OpenAI API
	model = ChatOpenAI(
		model='gpt-4o',
		api_key=SecretStr(os.getenv('OPENAI_API_KEY', '')),
	)

	try:
		agents = []
		for task in tasks:
			agent = Agent(task=task, llm=model, controller=controller, browser=browser)
			agents.append(agent)

		await asyncio.gather(*[agent.run() for agent in agents])
	except Exception as e:
		logger.error(f"Error during execution: {e}")
	finally:
		# Always close the browser
		try:
			logger.info("Closing browser...")
			await browser.close()
		except Exception as close_error:
			logger.error(f"Error closing browser: {close_error}")


if __name__ == '__main__':
	asyncio.run(main())