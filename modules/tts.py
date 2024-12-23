from google.cloud import texttospeech
'''
def generate_voice(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    return "output.mp3"
'''

def generate_voice(response):
    # Simula a geração de voz sem custos
    print(f"[Simulação] Gerando áudio para: {response}")
    return "audio_placeholder.mp3"
