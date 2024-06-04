import google.generativeai as genai
import pyttsx3
import speech_recognition as sr

# Configuração inicial
genai.configure(api_key= open('api_key.txt', 'r').read().strip())
conversa = genai.GenerativeModel('gemini-pro').start_chat(history=[])

# Script de preparação
# script_preparacao = ""
# conversa.send_message(script_preparacao)

geminiIA = True
ligarMicrofone = True

# Configuração da voz
def configurar_voz(voice_index=1, rate=245):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', rate)
    engine.setProperty('voice', voices[voice_index].id)
    return engine

# Listar e selecionar a voz
def listar_vozes():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name}")

if geminiIA:
    listar_vozes()
    voz_selecionada = int(input("Selecione o número da voz desejada: "))
    engine = configurar_voz(voice_index=voz_selecionada)

# Configuração do microfone
if ligarMicrofone:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

print("Digite 'desligar' para encerrar\n")

while True:
    if ligarMicrofone:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Fale alguma coisa (ou diga 'desligar')")
            audio = recognizer.listen(source)
            try:
                texto = recognizer.recognize_google(audio, language="pt-BR")
                print(f"Você disse: {texto}")
            except Exception as e:
                print("Não entendi o que você disse. Erro:", e)
                texto = ""
    else:
        texto = input("Escreva sua mensagem (ou 'desligar'): ")

    if texto.lower() == "desligar":
        break

    response = conversa.send_message(texto)
    print(f"Gemini: {response.text}\n")

    if geminiIA:
        engine.say(response.text)
        engine.runAndWait()

print("Encerrando Chat")
