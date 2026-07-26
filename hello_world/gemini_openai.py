from openai import OpenAI

client = OpenAI(
    api_key="AQ.Ab8RN6JbwWbdOVlpII5HtBHRMFOjSaV32BB_GIqhTMnQFC9z4w",
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[{"role": "user", "content": "Hello, Nide to meet you, who are you?"}],
)

print(response.choices[0].message.content)
