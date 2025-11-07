
import os
from dotenv import load_dotenv
from openai import OpenAI

# Step 1: Load your environment variables
load_dotenv('api.env')

# Step 2: Access your API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")


# Step 3: Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Step 4: Make a small test request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello from my first Python AI app!"}]
)

print(response.choices[0].message.content)
