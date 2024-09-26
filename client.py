from openai import OpenAI
client = OpenAI(
    api_key="sk-b42nysr4Y8iNheTQTbOtkqJY13tXykQcvkU4JFKthoT3BlbkFJgK7Og00sbKMtioHCbudAzJZUoIQpAf7RFnNi8TgPoA",
)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like alexa and Google cloud."},
        {"role": "user","content": "What is coding."
        }
    ]
)

print(completion.choices[0].message)

#pip install Openai