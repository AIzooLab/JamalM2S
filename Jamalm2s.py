from flask import Flask, render_template, request, jsonify
import openai
import requests
import hashlib
import json
import time
import speech_recognition as sr

app = Flask(__name__)

# Load API keys from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

openai.api_key = config['openai_api_key']
wolfram_alpha_api_key = config['wolfram_alpha_api_key']
github_token = config['github_access_token']
azure_token = config['azure_api_key']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    # Send user input to OpenAI for response
    openai_response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    assistant_response = openai_response.choices[0].text.strip()
    
    return jsonify({'response': assistant_response})

@app.route('/voice-interaction', methods=['POST'])
def voice_interaction():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Speak something:")
        audio = recognizer.listen(source)
        
    try:
        voice_input = recognizer.recognize_google(audio)
        print("Voice Input:", voice_input)
        
        # Perform actions based on voice input
        if "weather" in voice_input:
            response = query_wolfram_alpha("current weather")
        elif "location" in voice_input:
            response = get_location_address("New York")
        else:
            response = "Sorry, I could not understand your voice."
            
        return jsonify({'response': response})
        
    except sr.UnknownValueError:
        return jsonify({'response': "Sorry, I could not understand your voice."})
    except sr.RequestError:
        return jsonify({'response': "Sorry, I'm having trouble accessing the microphone."})

def query_wolfram_alpha(query):
    url = f"http://api.wolframalpha.com/v2/query?input={query}&format=plaintext&output=JSON&appid={wolfram_alpha_api_key}"
    response = requests.get(url)
    data = response.json()
    result = data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
    return result

@app.route('/github-repo', methods=['GET'])
def get_github_repo():
    headers = {'Authorization': f'Bearer {github_token}'}
    response = requests.get('https://api.github.com/repos/yourusername/yourrepository', headers=headers)
    repo_info = response.json()
    return jsonify(repo_info)

@app.route('/azure-service', methods=['GET'])
def get_azure_service():
    headers = {'Authorization': f'Bearer {azure_token}'}
    response = requests.get('https://management.azure.com/...', headers=headers)
    service_info = response.json()
    return jsonify(service_info)

if __name__ == '__main__':
    app.run(debug=True)
