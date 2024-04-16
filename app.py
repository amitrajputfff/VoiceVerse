from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import os

app = Flask(__name__)

# Define the directory where your static files are located
static_dir = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/record_audio', methods=['POST'])
def record_audio():
    output_file = "recorded_audio.wav"
    fs = 44100  # Sample rate
    duration = 5  # Duration of recording in seconds

    # Recording audio
    print("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wav.write(output_file, fs, recording)  # Save the recorded audio to a file

    return jsonify({'message': 'Recording finished'})

@app.route('/translate_text', methods=['POST'])
def translate_text():
    # Get the selected target language from the request
    target_language = request.json.get('target_language')

    audio_file = "recorded_audio.wav"

    # Transcribing audio to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            english_text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not understand audio'})
        except sr.RequestError as e:
            return jsonify({'error': f'Could not request results; {e}'})

    # Translating text to the selected target language
    translator = Translator()
    translated_text = translator.translate(english_text, dest=target_language).text

    return jsonify({'translated_text': translated_text, 'target_language': target_language})


@app.route('/play_translation', methods=['POST'])
def play_translation():

    audio_file = "recorded_audio.wav"

    # Transcribing audio to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            english_text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not understand audio'})
        except sr.RequestError as e:
            return jsonify({'error': f'Could not request results; {e}'})

  
    translator = Translator()
    spanish_text = translator.translate(english_text, dest='es').text

    if spanish_text is None:
        return jsonify({'error': 'Translated text not found in request data'}), 400

    # Generating speech from translated text
    tts = gTTS(text= spanish_text, lang='es')
    tts.save("output.mp3")
    # Get the absolute path of the saved MP3 file
    output_file_path = os.path.abspath("output.mp3")
    os.system("open output.mp3")
    return jsonify({'message': 'Speech saved', 'mp3_file': output_file_path})

# Serve the index.html file
@app.route('/')
def index():
    return send_from_directory(static_dir, 'index.html')

# Serve the static files (script.js)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)

