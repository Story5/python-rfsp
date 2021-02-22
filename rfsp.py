import requests

url = 'https://shanghaicity.openservice.kankanews.com/public/tour/filterinfo2'
response = requests.get(url, headers={'user-agent': 'rfsp/0.0.1'})
print(response.status_code)
print(response.json())
