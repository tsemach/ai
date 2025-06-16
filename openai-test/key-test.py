from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ],
    temperature=1,
    max_tokens=2048,
    top_p=1
)

print(response.choices[0].message.content)