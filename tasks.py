from celery import Celery
import time
import os
import logging
from gtts import gTTS

# Configure logging
logging.basicConfig(level=logging.INFO)

celery = Celery(
        'tasks',
        backend='redis://127.0.0.1:6379/0',
        broker='redis://127.0.0.1:6379/0'
    )

@celery.task
def add_together(a, b):
    print('task:add_together:', a, b)
    return a + b

@celery.task(max_retries=3)
def generate_audio_task(text, upload_path, namefile):
    print('task:generate_audio_task:', text, upload_path)
    try:
        filePath = os.path.join(upload_path, namefile)
        print("run_tts:", filePath)
        tts = gTTS(text, lang='en')
        tts.save(filePath)
        return True
    except Exception as e:
        print(f"generate_audio_task:Caught an exception: {e}")
        raise e

if __name__ == '__main__':
    celery.start()