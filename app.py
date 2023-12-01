import os
from flask import Flask, render_template, request, jsonify

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

app = Flask(__name__)

def translate_to_hindi(text):
    try:
        # Base URL for Google Translate
        url = "https://translate.googleapis.com/translate_a/single" \
              f"?client=gtx&sl=en&tl=hi&dt=t&q={text}"

        # Make an HTTP GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract the translation from the JSON response
            translation = data[0][0][0]

            # Replace encoded HTML entities with their actual symbols
            translation = translation.replace("&amp;", "&") \
                .replace("&quot;", "\"") \
                .replace("&lt;", "<") \
                .replace("&gt;", ">")

            return translation
        else:
            return f"HTTP Request Failed with error code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_text', methods=['POST'])
def translate_text():
    english_text = request.form['english_text']
    hindi_translation = translate_to_hindi(english_text)
    return jsonify({"translation": hindi_translation})

@app.route('/translate_file', methods=['POST'])
def translate_file():
    uploaded_file = request.files['file']
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        hindi_translation = translate_to_hindi(content)
        return jsonify({"translation": hindi_translation})
    return jsonify({"error": "File not found."})

if __name__ == "__main__":
    app.run(debug=True)