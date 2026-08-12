import os
import requests

api_key = os.environ.get("BUFFER_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

query = """
query GetChannels {
  channels(input: { organizationId: "6a710b4e10c3daf031701bd3" }) {
    id
    name
    service
  }
}
"""

payload = {"query": query}

response = requests.post("https://api.buffer.com", headers=headers, json=payload)
print(response.json())