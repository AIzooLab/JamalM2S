from flask import Flask, render_template, request, jsonify
import openai
import requests
import hashlib
import json
import time
import speech_recognition as sr
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import filestack

app = Flask(__name__)

# Load API keys from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

openai.api_key = config['openai_api_key']
wolfram_alpha_api_key = config['wolfram_alpha_api_key']
github_token = config['github_access_token']
azure_token = config['azure_api_key']
filestack_api_key = config['filestack_api_key']

# Initialize OpenAI GPT-3.5 Turbo model and tokenizer
model_name = "gpt3.5-turbo"
gpt3_model = GPT2LMHeadModel.from_pretrained(model_name)
gpt3_tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Initialize Filestack client
filestack_client = filestack.Client(filestack_api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    chatbot_response = generate_chatbot_response(user_input)
    return jsonify({'response': chatbot_response})

@app.route('/voice_interaction', methods=['POST'])
def voice_interaction():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Speak something:")
        audio = recognizer.listen(source)
        
    try:
        voice_input = recognizer.recognize_google(audio)
        print("Voice Input:", voice_input)
        response = process_voice_input(voice_input)
        return jsonify({'response': response})
    except sr.UnknownValueError:
        return jsonify({'response': "Sorry, I could not understand your voice."})
    except sr.RequestError:
        return jsonify({'response': "Sorry, I'm having trouble accessing the microphone."})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file_url = request.form['file_url']
    uploaded_file_url = upload_to_filestack(file_url)
    return jsonify({'uploaded_file_url': uploaded_file_url})

def generate_chatbot_response(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    chatbot_response = response.choices[0].text.strip()
    return chatbot_response

def process_voice_input(voice_input):
    # Implement logic to process voice input
    return "Response to voice input"

def upload_to_filestack(file_url):
    new_file_link = filestack_client.upload(url=file_url)
    return new_file_link.url

if __name__ == '__main__':
    app.run(debug=True)

