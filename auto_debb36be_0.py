"""
Connects to the Todoist API using the todoist-api-python library and creates a new task.

Usage:
    python script.py --token <api_token> --title <task_title> --description <task_description>
"""

import json
from httpx import Client
from anthropic import arguments

# Define command line arguments
arguments(
    '--token', required=True, help='Your Todoist API token'
)
arguments(
    '--title', required=True, help='Task title'
)
arguments(
    '--description', required=True, help='Task description'
)

class TodoistAPI:
    def __init__(self, token):
        self.token = token
        self.client = Client('https://api.todoist.com/')

    def create_task(self, title, description):
        data = {
            'title': title,
            'description': description,
            'project_id': 1,  # Default project ID
            'priority': 3  # Default priority
        }

        try:
            response = self.client.post(
                '/api/v3/tasks/',
                headers={'Authorization': f'Bearer {self.token}'},
                json=data
            )
            return response.json()
        except Exception as e:
            print(f"Error creating task: {e}")
            return None

if __name__ == '__main__':
    try:
        token = input('--token ')
        title = input('--title ')
        description = input('--description ')

        todoist_api = TodoistAPI(token)
        response = todoist_api.create_task(title, description)

        if response is not None:
            print(json.dumps(response, indent=4))
    except Exception as e:
        print(f"Error: {e}")