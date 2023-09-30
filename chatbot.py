import openai

openai.api_key = config['openai_api_key']

def get_chatbot_response(user_input, context=""):
    prompt = f"{context}\nUser: {user_input}\nChatBot:"
    openai_response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50
    )
    return openai_response.choices[0].text.strip()
