import requests
import os
from zipfile import ZipFile
from io import BytesIO

# GitHub repository information
github_user = 'akdenizz'
github_repo = 'mnist_classification'
github_token = "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"

# Request headers
headers = {
    'Authorization': f'token {github_token}'
}

# API URL to fetch the GitHub repository
api_url = f'https://api.github.com/repos/{github_user}/{github_repo}/zipball/main'

# Send the request
response = requests.get(api_url, headers=headers)

# Check the response status
if response.status_code == 200:
    # Save the ZIP file to memory
    zip_content = BytesIO(response.content)

    # Get the name of the ZIP file
    zip_file_name = f'{github_repo}.zip'

    # Create the folder where the ZIP file will be extracted
    extract_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), zip_file_name.replace('.zip', ''))

    # Create the folder (it won't throw an error if it already exists)
    os.makedirs(extract_folder, exist_ok=True)

    # Extract the ZIP file
    with ZipFile(zip_content) as zip_ref:
        zip_ref.extractall(extract_folder)

    print(f'{zip_file_name} successfully extracted and placed in the {extract_folder} folder.')
else:
    print(f'Error code: {response.status_code}, GitHub repository could not be downloaded.')
