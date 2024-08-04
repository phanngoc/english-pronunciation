# from celery import Celery
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
from gruut import sentences
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import difflib
import os
from nltk.corpus import cmudict
from suggest import get_suggest_sentence
from tasks import add_together, generate_audio_task
# from celery.result import AsyncResult
import time
import datetime
import jiwer

d = cmudict.dict()

def get_phonetic_transcription(word):
    """Returns the phonetic transcription of a word."""
    return d.get(word.lower())

def syllable_to_char_map(word, syllables):
    """Map each syllable to its corresponding characters in the word."""
    char_map = []
    start = 0
    for syllable in syllables:
        end = start + len(syllable)
        char_map.append(word[start:end])
        start = end
    return char_map

def highlight_syllables(expected_syllables, actual_syllables, word):
    """Highlight each syllable, red for wrong syllable, green for right syllable."""
    highlighted = []
    char_map = syllable_to_char_map(word, actual_syllables)
    for exp_syl, act_syl, chars in zip(expected_syllables, actual_syllables, char_map):
        print(f"highlight_syllables: {exp_syl} -> {act_syl} -> {chars}")
        if exp_syl == act_syl:
            highlighted.append(f'<span style="color: green;">{chars}</span>')
        else:
            highlighted.append(f'<span style="color: red;">{chars}</span>')
    return highlighted

def highlight_differences(true_text, pred_text):
    true_words = true_text.split()
    pred_words = pred_text.split()
    
    # Initialize lists for highlighted words
    highlighted = []
    print('true_words:', true_words)
    print('pred_words:', pred_words)
    # Compare words in true and predicted text
    max_len = max(len(true_words), len(pred_words))
    for i in range(max_len):
        pred_word = pred_words[i] if i < len(pred_words) else ""
        print('pred_word:', pred_word)
        if pred_word in true_words:
            highlighted.append(f'<span style="color: green;">{pred_word}</span>')  # Green for correct
        else:
            highlighted.append(f'<span style="color: red;">{pred_word}</span>')  # Red for incorrect

    return ' '.join(highlighted)

app = Flask(__name__)

# Set maximum request size (e.g., 16 MB)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File is too large. Please upload a file smaller than 100 MB."}), 413

# Load the Whisper model
model = whisper.load_model("small.en")

@app.route('/')
def index():
    print("Hello index")
    suggest_sentence = get_suggest_sentence()
    add_together.delay(23, 42)
    audioUrl = generate_name_file()
    generate_audio_task.delay(suggest_sentence, 'uploads', audioUrl)
    return render_template('index-temp.html', suggest_sentence=suggest_sentence, audioUrl=audioUrl)

def generate_name_file():
    now = datetime.datetime.now()
    name = "voice-" + now.strftime("%y%m%d%H:%M") + '.wav'
    return name

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
    
    if 'sentences' not in request.form:
        return jsonify({"status": "error", "message": "No sentences in request"}), 400

    # Transcribe the audio using Whisper
    audio_file = request.files['audio']
    temp_file_path = os.path.join('uploads', 'recording.wav')
    audio_file.save(temp_file_path)
    result = model.transcribe(temp_file_path)
    transcription = result["text"]

    reference_text = request.form['sentences']
    
    
    sentences_diff = highlight_differences(reference_text, transcription)
    print('sentences_diff', sentences_diff)
    return jsonify({
            'transcription': transcription,
            'sentences_diff': sentences_diff
            })

@app.route('/load-sentence-audio', methods=['GET'])
def get_new_sentence_and_audio():
    suggest_sentence = get_suggest_sentence()
    audioUrl = generate_name_file()
    generate_audio_task.delay(suggest_sentence, 'uploads', audioUrl)
    return jsonify({
        'sentence': suggest_sentence,
        'audioUrlMp3': url_for('uploaded_file', filename=audioUrl),
        'audioUrlOgg': url_for('uploaded_file', filename=audioUrl)
    })

if __name__ == '__main__':
    app.run(debug=True)

