import os
import tkinter as tk
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
from tkinter import messagebox

class SpeechTranslationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Speech Translation")
        master.configure(bg="#f0f0f0")

        # Get the screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Set the dimensions and position of the window
        window_width = 400
        window_height = 300
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Create buttons
        self.record_button = tk.Button(master, text="Record", command=self.record_audio)
        self.record_button.pack(pady=10, padx=20, fill=tk.X)

        self.language_button = tk.Button(master, text="Translate to Spanish", command=self.translate_to_spanish)
        self.language_button.pack(pady=10, padx=20, fill=tk.X)

        self.play_button = tk.Button(master, text="Play Translation", command=self.play_translation)
        self.play_button.pack(pady=10, padx=20, fill=tk.X)

        self.status_label = tk.Label(master, text="", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12))
        self.status_label.pack()

    def record_audio(self):
        output_file = "recorded_audio.wav"
        fs = 44100  # Sample rate
        duration = 5  # Duration of recording in seconds
        self.status_label.config(text="Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        wav.write(output_file, fs, recording)  # Save the recorded audio to a file
        self.status_label.config(text="Recording finished.")

    def translate_to_spanish(self):
        audio_file = "recorded_audio.wav"
        english_text = self.audio_to_text(audio_file)
        if english_text:
            spanish_text = self.translate_text(english_text, dest_language='es')
            self.translated_text = spanish_text
            self.status_label.config(text="Translation complete.")
        else:
            self.status_label.config(text="No text recognized from the audio.")

    def play_translation(self):
        if hasattr(self, 'translated_text'):
            audio_file = self.text_to_speech(self.translated_text, lang='es')
            os.system("open " + audio_file)
        else:
            self.status_label.config(text="Translate text first.")

    def audio_to_text(self, audio_file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results; {e}"

    def translate_text(self, text, dest_language='hi'):
        translator = Translator()
        translated_text = translator.translate(text, dest=dest_language)
        return translated_text.text

    def text_to_speech(self, text, lang='hi'):
        tts = gTTS(text=text, lang=lang)
        tts.save("output.mp3")
        return "output.mp3"

root = tk.Tk()
app = SpeechTranslationGUI(root)
root.mainloop()
