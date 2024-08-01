import os
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

# client = OpenAI()
client = OpenAI(
   # open ai api key goes here,
)

completion = client.chat.completions.create(
  model="text-davinci-002",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)
message = completion.choices[0].message.content
logging.info(message)
