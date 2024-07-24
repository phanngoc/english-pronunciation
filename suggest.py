import openai
from openai import OpenAI
import dotenv
import os
import random

# Load environment variables from file
dotenv.load_dotenv('.env')

apiKey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apiKey)
GPT_MODEL = 'gpt-4o'

# write function to generate practice topics
def pick_topic():
    topics = [
        "Describe your favorite book/movie",
        "Talk about your dream vacation destination",
        "Discuss your favorite hobby",
        "Describe a memorable event from your childhood",
        "Talk about a recent news article that caught your attention",
        "Discuss the benefits of learning a new language",
        "Describe your ideal job",
        "Talk about a challenging experience you faced and how you overcame it",
        "Discuss the impact of technology on society",
        "Describe a person who has had a significant influence on your life"
    ]
    return random.choice(topics)


# write function helper
def get_suggest_sentence():
    system_prompt = """
        I am english learner, you are my coach, suggest me one sentence to practice speaking, for intermediate level.
        Only output sentence less than 2 lines.
        \n\n
        """

    chat_message = pick_topic()

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

import time
from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

text="It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent."

def run_tts(text, dir=""):
    namefile = "voice-" + str(int(time.time()))
    filePath = dir + "/" + namefile + ".wav"
    tts.tts_to_file(text=text,
        file_path=filePath,
        language="en",
        speaker="Ana Florence"
        )
    return namefile + ".wav"
