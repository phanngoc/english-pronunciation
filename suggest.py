import openai
from openai import OpenAI
import dotenv
import os

# Load environment variables from file
dotenv.load_dotenv('.env')

apiKey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apiKey)
GPT_MODEL = 'gpt-4o'

# write function helper
def get_suggest_sentence():
    system_prompt = """
        I am english learner, you are coach, suggest me one sentence to practice speaking, for intermediate level.
        Sentence less than 2 lines.
        \n\n
        """
    topic1 = "interview backend enginnering job."
    topic2 = "holiday in Japan."

    chat_message = topic2

    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": chat_message},
    ]
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        max_tokens=200,
        top_p=1.0,
        n=1,
        stop=None,
        temperature=0.7)

    summary = response.choices
    return summary[0].message.content
