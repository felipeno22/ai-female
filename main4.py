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
def get_response2(user_input):
    # Carrega o conhecimento existente
    knowledge = load_knowledge()

    # Verifica se a pergunta já foi respondida antes
    if user_input in knowledge:
        # Retorna uma resposta se não for a mensagem padrão
        if knowledge[user_input] and "Desculpe, não entendi. Pode me ensinar o que devo responder?" not in knowledge[user_input]:
            return random.choice(knowledge[user_input])
        else:
            # Se a resposta for a mensagem padrão, solicita ao usuário uma nova resposta
            return "Essa pergunta já foi registrada, mas ainda não tenho uma resposta. O que você gostaria que eu respondesse?"

    # Pergunta não encontrada - solicita ao usuário uma resposta personalizada
    response = "Desculpe, não entendi. Pode me ensinar o que devo responder?"

    # Salva a pergunta com uma lista vazia para evitar duplicação
    knowledge[user_input] = []
    save_knowledge(knowledge)
    
    return response

def load_conversationsw():
    try:
        with open("history.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("conversations", [])
    except FileNotFoundError:
        return []


def load_conversations():
    try:
        # Tenta carregar o histórico existente
        with open("history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Caso o arquivo não exista ou esteja vazio/corrompido, retorna estrutura inicial
        return {"conversations": []}




"""def save_conversation(user_message, bot_response):
    history = load_conversations()
    if "conversations" not in history:
        #history["conversations"] = []
        history = {"conversations": []}


    history["conversations"].append({"user": user_message, "bot": bot_response})

    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)"""

def save_conversation(user_message, bot_response):
    # Carregar o histórico existente
    history = load_conversations()
    #print(history)
    # Garante que a chave "conversations" está presente
    if "conversations" not in history or not isinstance(history["conversations"], list):
        history["conversations"] = []

    # Adicionar a nova conversa ao histórico
    history["conversations"].append({"user": user_message, "bot": bot_response})

    # Salvar o histórico atualizado
    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

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
    if(response != "Desculpe, não entendi. Pode me ensinar o que devo responder?"): 
        save_conversation(user_input, response)

    # Geração de "áudio" (simulado)
    audio = generate_voice(response)

    return jsonify({"response": response, "audio": audio})




# Rota para receber e salvar uma nova resposta para uma pergunta
@app.route('/teach', methods=['POST'])
def teach():
    data = request.get_json()
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()

    if not question or not answer:
        return jsonify({"error": "Pergunta ou resposta inválida."}), 400

    # Carrega o conhecimento existente
    knowledge = load_knowledge()

    # Adiciona a nova resposta para a pergunta existente
    if question in knowledge:
        if answer not in knowledge[question]:
            knowledge[question].append(answer)
    else:
        # Caso a pergunta ainda não exista (possível edge case)
        knowledge[question] = [answer]

    # Salva o conhecimento atualizado
    save_knowledge(knowledge)
    save_conversation(question, answer) 

    return jsonify({"message": "Resposta adicionada com sucesso!"})


@app.route('/history', methods=['GET'])
def history():
    conversations = load_conversations()
    print(conversations)
    return jsonify({"history": conversations})


if __name__ == "__main__":
    app.run(debug=True)

