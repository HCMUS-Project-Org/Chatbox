import openai
import os

# Set up the OpenAI API key
openai.api_key = "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"

# Set up the GPT-3 model
model_engine = "text-davinci-002"
prompt = "Write a short story about a robot that learns to love."

# Generate text with the GPT-3 model
completions = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

message = completions.choices[0].text.strip()
print(message)

