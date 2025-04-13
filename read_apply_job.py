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

# Validate required environment variables
load_dotenv()
required_env_vars = ['OPENAI_API_KEY']
for var in required_env_vars:
	if not os.getenv(var):
		raise ValueError(f'{var} is not set. Please add it to your environment variables.')

logger = logging.getLogger(__name__)
# full screen mode
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
	with open('jobs.csv', 'r') as f:
		return f.read()


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
	"""Uploads a CV file to a specified index element in a browser context.
	Parameters:
	- index (int): Index of the element where the CV should be uploaded.
	- browser (BrowserContext): The browser context used to locate elements.
	Returns:
	- ActionResult: Contains a success message if upload succeeds, or an error message if it fails.
	Processing Logic:
	- Retrieves the DOM element based on the given index and checks if it is a file upload element.
	- Handles cases where the element cannot be found or is not suitable for file uploads.
	- Attempts to upload a CV file to the located element and logs the process."""
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


browser = Browser(
	config=BrowserConfig(
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		disable_security=True,
	)
)


async def main():
	# ground_task = (
	# 	'You are a professional job finder. '
	# 	'1. Read my cv with read_cv'
	# 	'2. Read the saved jobs file '
	# 	'3. start applying to the first link of Amazon '
	# 	'You can navigate through pages e.g. by scrolling '
	# 	'Make sure to be on the english version of the page'
	# )
	"""Async function to automate job search tasks using an AI language model for specific companies.
	Parameters:
	- None.
	Returns:
	- None.
	Processing Logic:
	- Constructs task strings for searching machine learning internships at specified companies.
	- Initializes a list of job-finding tasks for each target company.
	- Utilizes the OpenAI API for language model interaction to process tasks.
	- Deploys agents to execute tasks concurrently using asyncio."""
	ground_task = (
		'You are a professional job finder. '
		'1. Read my cv with read_cv'
		'find ml internships in and save them to a file'
		'search at company:'
	)
	tasks = [
		ground_task + '\n' + 'Google',
		# ground_task + '\n' + 'Amazon',
		# ground_task + '\n' + 'Apple',
		# ground_task + '\n' + 'Microsoft',
		# ground_task
		# + '\n'
		# + 'go to https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Taiwan%2C-Remote/Fulfillment-Analyst---New-College-Graduate-2025_JR1988949/apply/autofillWithResume?workerSubType=0c40f6bd1d8f10adf6dae42e46d44a17&workerSubType=ab40a98049581037a3ada55b087049b7 NVIDIA',
		# ground_task + '\n' + 'Meta',
	]
	
	# Using standard OpenAI API instead of Azure
	model = ChatOpenAI(
		model='gpt-4o',
		api_key=SecretStr(os.getenv('OPENAI_API_KEY', '')),
	)

	agents = []
	for task in tasks:
		agent = Agent(task=task, llm=model, controller=controller, browser=browser)
		agents.append(agent)

	await asyncio.gather(*[agent.run() for agent in agents])


if __name__ == '__main__':
	asyncio.run(main())