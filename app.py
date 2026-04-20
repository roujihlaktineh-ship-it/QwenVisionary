import os
from pathlib import Path
from huggingface_hub import InferenceClient
import ssl

# Load HF_TOKEN from .env with BOM handling
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Create SSL context that verifies certificates
ssl_context = ssl.create_default_context()

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"],
)

stream = client.chat.completions.create(
    model="Qwen/Qwen3.5-9B:together",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in one sentence."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"
                    }
                }
            ]
        }
    ],
    stream=True,
)

for chunk in stream:
    if chunk.choices and len(chunk.choices) > 0:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)