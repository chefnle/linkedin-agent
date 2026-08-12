import os
import requests

api_key = os.environ.get("BUFFER_API_KEY") 
channel_id = "6a710b9a99afb44349f6d28a"

headers = { "Authorization": f"Bearer {api_key}", 
"Content-Type": "application/json" }

query = """ mutation CreatePost { createPost(input: { text: "Hello from my self-built AI Agent!",
channelId: "6a710b9a99afb44349f6d28a", schedulingType: automatic, mode: customScheduled,
dueAt: "2026-08-15T12:00:00.000Z" })
{ ... on PostActionSuccess { post { id text dueAt } }
 ... on MutationError { message } } } """

response = requests.post("https://api.buffer.com", headers=headers,
json={"query": query})
print(response.json())