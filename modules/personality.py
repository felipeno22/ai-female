def get_response(processed_input):
    text = processed_input.get('text')
    if "oi" in text.lower():
        return "Olá! Como posso ajudar você hoje?"
    elif "tudo bem" in text.lower():
        return "Sim, tudo ótimo! E você?"
    return "Desculpe, ainda estou aprendendo a conversar sobre isso."
