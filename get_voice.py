import requests
filename = "output.wav"

def write_wave(text, voice = None):
    payload = {
    "INPUT_TYPE":"TEXT", 
    "INPUT_TEXT":text,
    "OUTPUT_TYPE": "AUDIO",
    "AUDIO":"WAVE_FILE",
    "LOCALE":"en_US"
    }
    if voice:
        payload['VOICE'] = voice
    r = requests.get('http://localhost:59125/process', params = payload)
    with open(filename, 'wb') as fd:
        fd.write(r.content)
    return len(r.content)
