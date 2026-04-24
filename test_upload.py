import requests
import os

url = "https://plant-analyser-zo2x.vercel.app/api/analyse"

# Create a tiny dummy image (valid PNG header)
dummy_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

files = {'image': ('test.png', dummy_png, 'image/png')}
data = {'session_id': 'test-session-1234'}

print("Sending request...")
response = requests.post(url, files=files, data=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
