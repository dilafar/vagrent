import requests
import sys 

file_name = sys.argv[1]
scan_type = ''

if file_name == 'gitleaks.json':
    scan_type = 'Gitleaks Scan'
elif file_name == 'njsscan.sarif':
    scan_type = 'SARIF'
elif file_name == 'semgrep.json':
    scan_type = 'Semgrep JSON Report'
elif file_name == 'retire.json':
    scan_type = 'Retire.js Scan'

headers = {
    'Authorization': 'Token b4ac1a9bd3a45df412f23225a86bd64e1d4a8bc5'
}

url = 'https://demo.defectdojo.org/api/v2/import-scan/'

# create product and engagement and include engagement number

data = {
    'active': True,
    'verified': True,
    'scan_type': scan_type,
    'minimum_severity': 'Low',
    'engagement': 14
}

files = {
    'file': open(file_name, 'rb')
}

response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 201:
    print('Scan results imported successfully')
else:
    print(f'Failed to import scan results: {response.content}')