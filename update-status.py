import os
import requests

token = os.environ.get('$GITHUB_TOKEN')
username = '$GITHUB_USERNAME'

def calculate_grade(total_repos):
    # Customize the grading criteria as needed
    if total_repos >= 100:
        return 'A'
    elif total_repos >= 50:
        return 'B'
    elif total_repos >= 20:
        return 'C'
    else:
        return 'D'

def create_github_status(total_repos, grade):
    try:
        # HTML for the status description with the grade
        description_html = f'Grade: {grade}, Total Repositories: {total_repos}'

        # API endpoint to create a GitHub status
        status_url = f'https://api.github.com/user/status'

        # Set up the request headers
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Set up the request payload
        payload = {
            'state': 'success',  # Adjust the state as needed (success, error, failure, etc.)
            'target_url': 'https://example.com',  # Adjust the target URL as needed
            'description': description_html,
            'context': 'custom/github-status'
        }

        # Make the API request
        response = requests.post(status_url, json=payload, headers=headers)

        # Check the response status
        response.raise_for_status()
        print('GitHub status updated successfully.')
    except Exception as e:
        print(f'Error updating GitHub status: {e}')
        exit(1)

def main():
    try:
        user_response = requests.get(f'https://api.github.com/users/{username}', headers={'Authorization': f'Bearer {token}'})
        user_data = user_response.json()

        total_repos = user_data['public_repos']  # Adjust as needed

        # Calculate the grade based on the total repositories
        grade = calculate_grade(total_repos)

        print(f'Grade: {grade}, Total Repositories: {total_repos}')

        # Update GitHub status with the grade
        create_github_status(total_repos, grade)
    except Exception as e:
        print(f'Error updating GitHub status: {e}')
        exit(1)

if __name__ == "__main__":
    main()