from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set up your Google API key
GOOGLE_API_KEY = 'AIzaSyCN34idj87N0cenyCxGwGHoSKcr32I_Kyo'

# Configure the generative model
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1024
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel('gemini-1.0-pro-latest', generation_config=generation_config, safety_settings=safety_settings)
convo = model.start_chat()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    convo.send_message(user_input)
    response = convo.last.text
    print(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
