import random
from flask import Flask, request, jsonify
from modules.tts import generate_voice

app = Flask(__name__)

# Banco de respostas carinhoso e feminino
responses = {
    "saudação": [
        "Oi, meu bem! Como você está? 😘",
        "Olá, querido! Que alegria falar com você! 🌸",
        "Oi, linda! Tudo bem com você? 💖"
    ],
    "ajuda": [
        "Estou aqui para te ajudar no que você precisar, fofinho! 💕",
        "Claro, meu amor! O que você precisa que eu faça por você? 🌷",
        "Fique tranquilo, estou aqui para tudo o que você precisar, meu bem! 💝"
    ],
    "despedida": [
        "Tchau, meu anjo! Até logo! 😘",
        "Foi tão bom conversar com você, até mais, querido! 💖",
        "Até logo, amorzinho! Cuide-se! 🌸"
    ],
    "default": [
        "Desculpe, não entendi. Pode falar de novo, meu anjo? 💕",
        "Hmm, não consegui entender direito. Pode repetir, fofura? 😘",
        "Oh, que pena, não entendi. Me fala de novo, querido? 💖"
    ]
}

# Função para selecionar a resposta baseada em palavras-chave
def get_response(user_input):
    user_input = user_input.lower()
    if "oi" in user_input or "olá" in user_input:
        return random.choice(responses["saudação"])
    elif "ajuda" in user_input or "preciso" in user_input:
        return random.choice(responses["ajuda"])
    elif "tchau" in user_input or "até mais" in user_input:
        return random.choice(responses["despedida"])
    else:
        return random.choice(responses["default"])

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('input', '')

    # Obter resposta personalizada
    response = get_response(user_input)

    # Geração de "áudio" (simulado)
    audio = generate_voice(response)

    return jsonify({"response": response, "audio": audio})

if __name__ == "__main__":
    app.run(debug=True)
