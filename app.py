from flask import Flask, request, jsonify, render_template
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import difflib
import os

app = Flask(__name__)

# Set maximum request size (e.g., 16 MB)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 20 MB

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File is too large. Please upload a file smaller than 100 MB."}), 413

# Load the Whisper model
model = whisper.load_model("base")

@app.route('/')
def index():
    print("Hello")
    return render_template('index-temp.html')

def get_pronunciation_feedback(transcription, reference):
    diff = difflib.ndiff(transcription.split(), reference.split())
    feedback = []

    for i, s in enumerate(diff):
        if s[0] == ' ':
            feedback.append({'word': s[2:], 'status': 'correct'})
        elif s[0] == '-':
            feedback.append({'word': s[2:], 'status': 'missing'})
        elif s[0] == '+':
            feedback.append({'word': s[2:], 'status': 'extra'})

    return feedback

@app.route('/record', methods=['POST'])
def record():

    if 'audio' not in request.files:
        return jsonify({"status": "error", "message": "No audio file in request"}), 400
    
    # Transcribe the audio using Whisper
    audio_file = request.files['audio']
    temp_file_path = os.path.join('uploads', 'recording.wav')
    audio_file.save(temp_file_path)
    result = model.transcribe(temp_file_path)
    transcription = result["text"]
    # duration = int(request.form.get('duration', 5))
    # sample_rate = 44100
    # print('duration', duration)
    # Record audio
    # recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    # sd.wait()

    # Save the recording as a temporary file
    # wav.write('recording.wav', sample_rate, recording)


    # Reference text (this can be dynamically set as well)
    reference_text = "This is a sample sentence to practice pronunciation."

    # Compare transcriptions
    feedback = get_pronunciation_feedback(transcription, reference_text)

    return jsonify({'transcription': transcription, 'feedback': feedback})


if __name__ == '__main__':
    app.run(debug=True)

