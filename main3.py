from flask import Flask, render_template, request, jsonify
import random
from modules.tts import generate_voice
import json

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


# Carregar conhecimento existente
def load_knowledge():
    try:
        with open("knowledge.json", "r", encoding="utf-8") as file:
            return json.load(file)  # Retorna os dados em formato de dicionário
    except FileNotFoundError:
        return {}  # Caso o arquivo não exista, retorna um dicionário vazio

# Salvar novas perguntas/respostas
def save_knowledge(data):
    with open("knowledge.json", "w") as file:
        json.dump(data, file, indent=4)  # Salva o dicionário como JSON com indentação para melhor leitura


# Responder com aprendizado
# Responder com aprendizado
def get_response2(user_input):
    # Carrega o conhecimento existente
    knowledge = load_knowledge()

    # Verifica se a pergunta já foi respondida antes
    for question, responses in knowledge.items():
        if user_input.lower() in question.lower():
            return random.choice(responses)  # Retorna uma resposta aleatória da lista

   # Pergunta não encontrada - solicita ao usuário uma resposta personalizada
    response = "Desculpe, não entendi. Pode me ensinar o que devo responder?"

    # Se a entrada não existir no knowledge, pede ao usuário para fornecer uma resposta
    if user_input not in knowledge:
        # Em vez de salvar diretamente a resposta padrão, agora podemos pedir ao usuário
        # por uma resposta personalizada, por exemplo, via outro formulário ou interação.
        knowledge[user_input] = []  # Inicializa a entrada sem resposta
        save_knowledge(knowledge)  # Salva o conhecimento atualizado

        # Retorna a resposta padrão até que o usuário forneça uma resposta
        return response
    else:
        # Se já tiver alguma resposta personalizada, retorna-a
        return random.choice(knowledge[user_input])  # Retorna uma resposta já salva
    


# Função para selecionar a resposta baseada em palavras-chave
def get_response(user_input):
    user_input = user_input.lower()
    if "oi" in user_input or "olá" in user_input:
        return random.choice(responses["saudação"])
    elif "ajuda" in user_input or "preciso" in user_input:
        return random.choice(responses["ajuda"])
    elif "tchau" in user_input or "até mais" in user_input:
        return random.choice(responses["despedida"])
    elif "sair" in user_input or "fim" in user_input:
        return random.choice(responses["despedida"])
    else:
        return random.choice(responses["default"])




# Rota para renderizar a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o chat, processando a mensagem
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('input', '')

    # Obter resposta personalizada
    response = get_response2(user_input)

    # Geração de "áudio" (simulado)
    audio = generate_voice(response)

    return jsonify({"response": response, "audio": audio})

if __name__ == "__main__":
    app.run(debug=True)

