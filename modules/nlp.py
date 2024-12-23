import spacy

nlp = spacy.load("pt_core_news_sm")  # Ou pt_core_news_sm para português

def process_input(user_input):
    doc = nlp(user_input)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {'text': user_input, 'entities': entities}

