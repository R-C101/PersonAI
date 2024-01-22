from openai import OpenAI
from apikey import apikey

client = OpenAI(api_key=apikey)


conversations = []

def generate_gpt3_response(user_input):
     
    conversations.append(user_input)

    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
    {"role": "system", "content": "You are a helpful chat assistant. at the beginning of every user input, the past 5 conversations between you and the user will be attached for context and memory. the conversation history will start with the phrase Conversation History and end with three Hashes like ###"},
    {"role": "user", "content": "Conversation History: \n"+"\n".join(conversations[-10:])+"###\n" + user_input },

    ]
    )
    output = response.choices[0].message.content
    conversations.append(output)
    return output

