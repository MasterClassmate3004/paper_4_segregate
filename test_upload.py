import requests

with open('0625_m25_qp_42.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload', files=files)
    
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
