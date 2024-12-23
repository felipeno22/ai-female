from flask import Flask, request, jsonify
from modules.nlp import process_input
from modules.tts import generate_voice
from modules.personality import get_response

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    processed_input = process_input(user_input)
    response = get_response(processed_input)
    audio = generate_voice(response)
    return jsonify({'response': response, 'audio': audio})

if __name__ == "__main__":
    app.run(debug=True)
