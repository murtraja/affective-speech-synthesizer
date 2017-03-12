# import requests
# filename = "output.wav"

# def write_wave(text, voice = None):
#     payload = {
#     "INPUT_TYPE":"TEXT", 
#     "INPUT_TEXT":text,
#     "OUTPUT_TYPE": "AUDIO",
#     "AUDIO":"WAVE_FILE",
#     "LOCALE":"en_US"
#     }
#     if voice:
#         payload['VOICE'] = voice
#     r = requests.get('http://localhost:59125/process', params = payload)
#     with open(filename, 'wb') as fd:
#         fd.write(r.content)
#     return len(r.content)
SERVER_ADDRESS = "http://localhost"
SERVER_PORT = "59125"
SERVER_URL = SERVER_ADDRESS+":"+SERVER_PORT+"/process"
OUTPUT_FILE = "output/output.wav"
OUTPUT_SENTENCE_FILE_PREFIX = 'output/output_'
emotion_voice_map = {
    'neutral' : 'cmu-slt-hsmm'
}
#pip install requests
import requests, threading, wave, os.path

def get_voice_name(emotion):
    if emotion not in emotion_voice_map:
        emotion = 'neutral'
    emotion = emotion_voice_map[emotion]
    return emotion

def get_payload(sentence, emotion):
    payload = {
    "INPUT_TYPE":"TEXT", 
    "INPUT_TEXT":sentence,
    "OUTPUT_TYPE": "AUDIO",
    "AUDIO":"WAVE_FILE",
    "LOCALE":"en_US"
    }

    voice_name = get_voice_name(emotion)
    payload['VOICE'] = voice_name
    return payload

def get_wav_from_server(payload):
    response = requests.get(SERVER_URL, params = payload, timeout=5)
    status_code = response.status_code
    print "status_code = "+str(status_code)
    if response.status_code != 200:
        print "BAD REQUEST given by payload"+str(payload)
        return 0
    content = response.content # this is in binary format
    return content
    
def get_sentence_file_name(index):
    padder = 10000
    file_suffix = padder + index;
    file_suffix = str(file_suffix)[1:]
    file_name = OUTPUT_SENTENCE_FILE_PREFIX+file_suffix+".wav"
    return file_name

def write_wav_file(wav_object, sentence_file_name):
    wav_file = open(sentence_file_name, 'wb')
    wav_file.write(wav_object)
    wav_file.close()

def get_wav_file(sentence, emotion, sentence_files, index):
    sentence_file_name = get_sentence_file_name(index)
    if os.path.isfile(sentence_file_name):
        sentence_files[index] = sentence_file_name        
        return

    payload = get_payload(sentence, emotion)
    print "Thread "+str(index)+" fetched the payload"

    wav_object = get_wav_from_server(payload)
    print "Thread "+str(index)+" fetched the wav_object of length "+str(len(wav_object))

    
    sentence_files[index] = sentence_file_name
    write_wav_file(wav_object, sentence_file_name)
    #print "Thread",index,":\nwav_object size:",len(sentence_files)

def start_thread(sentence, emotion, sentence_files, index):
    thread = threading.Thread(target = get_wav_file, args = (sentence, emotion, sentence_files, index))
    return thread

def start_threads(sentences, emotions, sentence_files):
    thread_list = []

    for index in range(len(sentences)):
        thread = start_thread(sentences[index], emotions[index], sentence_files, index)
        print 'now starting thread', index
        thread.start()
        thread_list.append(thread)
        #thread.join()
    return thread_list

def wait_for_all_threads_to_join(thread_list):
    print 'now waiting for threads to join'
    for index in range(len(thread_list))    :
        thread = thread_list[index]
        print 'now waiting for thread',index
        thread.join()

def construct_final_wav_file(sentence_files):
    data= []
    for file_name in sentence_files:
        wav_file = wave.open(file_name, 'rb')
        data.append( [wav_file.getparams(), wav_file.readframes(wav_file.getnframes())] )
        wav_file.close()

    output = wave.open(OUTPUT_FILE, 'wb')
    #print "the data is:", data
    output.setparams(data[0][0])
    for i in range(len(sentence_files)):
        output.writeframes(data[i][1])
    output.close()

def start_audio_file_generation(sentences, emotions):
    sentence_files = [0 for _ in sentences]
    thread_list = start_threads(sentences, emotions, sentence_files)
    wait_for_all_threads_to_join(thread_list)
    #print sentence_files, "<- sentence files"
    construct_final_wav_file(sentence_files)
