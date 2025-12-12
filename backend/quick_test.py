import requests

print("Probando endpoint GET /api/academic/courses/7")
response = requests.get("http://localhost:5000/api/academic/courses/7")
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
