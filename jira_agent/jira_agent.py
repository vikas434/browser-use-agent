from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
import dotenv
import os
import json
from datetime import datetime


# Create fixed JWT implementation plan - no browser needed for this part
jwt_implementation_plan = {
    "story_title": "JWT Authentication Implementation",
    "story_summary": "Implement secure JWT authentication for REST API endpoints",
    "subtasks": [
        {
            "summary": "Set up JWT authentication infrastructure",
            "description": """Implement the core JWT authentication infrastructure:

Tasks:
- Set up JWT token generation with proper secret key management
- Implement token signing and verification utilities
- Configure token expiration and refresh mechanisms
- Create secure storage for JWT secrets in environment variables
- Add unit tests for JWT token generation and validation

Definition of Done:
- JWT token generation and validation functions are working
- Secret keys are properly secured
- All tests are passing""",
            "priority": "Medium",
            "labels": ["authentication", "api"]
        },
        {
            "summary": "Create authentication middleware for REST API endpoints",
            "description": """Implement middleware to validate JWT tokens for all protected API endpoints:

Tasks:
- Create middleware to extract JWT from request headers
- Implement token validation logic with proper error handling
- Set up error responses (401/403) for invalid or expired tokens
- Add role-based access control checks
- Write integration tests for middleware

Definition of Done:
- Middleware successfully validates tokens on all protected routes
- Proper error responses are returned for invalid tokens
- All tests are passing""",
            "priority": "Medium",
            "labels": ["authentication", "api"]
        },
        {
            "summary": "Document authenticated API endpoints with Swagger",
            "description": """Create comprehensive API documentation with authentication information:

Tasks:
- Set up Swagger/OpenAPI documentation for all endpoints
- Document authentication requirements for each endpoint
- Include examples of properly authenticated requests
- Document error responses for authentication failures
- Ensure documentation is automatically generated from code

Definition of Done:
- All endpoints are documented with authentication requirements
- Swagger UI shows proper authentication information
- Examples are working and accurate""",
            "priority": "Medium",
            "labels": ["authentication", "api", "documentation"]
        },
        {
            "summary": "Implement secure token refresh mechanism",
            "description": """Create secure mechanism for refreshing expired JWT tokens:

Tasks:
- Implement refresh token generation and storage
- Create secure token refresh endpoint
- Add validation for refresh tokens
- Implement token blacklisting for logout
- Write security tests for refresh mechanism

Definition of Done:
- Users can securely refresh tokens without re-authentication
- Refresh tokens are properly secured and validated
- Blacklisting works for logged out users
- All security tests are passing""",
            "priority": "Medium",
            "labels": ["authentication", "api", "security"]
        }
    ]
}

# Configure the browser with correct parameters - only needed for task creation phase
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        headless=False,
    )
)

# Single agent for task creation only
task_creation_agent = Agent(
    task="""
    You'll be creating 4 specific JWT authentication subtasks in Jira. No analysis needed as the tasks are already defined.
    
    Follow these steps:
    1. Navigate to https://knowledge-gain-ai.atlassian.net/browse/MP-1
    2. For each of the 4 JWT subtasks provided in the JSON:
       a. Look for a "Create Subtask" button or option (often found in dropdown menus or "+" buttons)
       b. Fill in the summary and description exactly as specified in the JSON
       c. Set priority to Medium and add the labels specified
       d. Save the subtask
       
    If you encounter a login screen or JavaScript loading error (which is likely based on previous attempts):
    - Simply report that the Jira instance requires authentication or is having loading issues
    - No need to proceed further if you can't access the page
    
    Remember that the point is to demonstrate the approach, not necessarily complete the task if the system is inaccessible.
    
    Wait a full 10 seconds when first loading pages to allow all scripts to load properly.
    """,
    llm=ChatOpenAI(model='gpt-4o'),
    browser=browser,
)

async def main():
    print(f"Starting Jira workflow at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Skip analysis phase - use predefined task plan
    print("Using predefined JWT authentication implementation plan with 4 subtasks:")
    for i, subtask in enumerate(jwt_implementation_plan["subtasks"], 1):
        print(f"  {i}. {subtask['summary']}")
    
    # Update the agent's task with our predefined plan
    task_creation_agent.task = task_creation_agent.task + f"\n\nUse the following subtask details:\n```json\n{json.dumps(jwt_implementation_plan, indent=2)}\n```"
    
    # Run the task creation agent
    print("\nAttempting to create subtasks in Jira...")
    try:
        creation_result = await task_creation_agent.run()
        print("\nTask creation attempt completed.")
        print("Result:")
        print(creation_result)
    except Exception as e:
        print(f"\nError during task creation: {e}")
        print("\nThe Jira instance may be inaccessible or requires authentication.")
        print("In a real implementation, these tasks would be created with the details specified in the plan.")
    
    print("\nJWT Authentication Implementation Plan (for reference):")
    print(json.dumps(jwt_implementation_plan, indent=2))
    
    input('\nPress Enter to close the browser...')
    try:
        await browser.close()
    except:
        print("Browser already closed or not available.")

if __name__ == '__main__':
    asyncio.run(main())