import pyaudio
import wave
import threading
play_audio = True
CHUNK = 1024
FILENAME = 'output/output.wav'
def play():
    
    wf = wave.open(FILENAME, 'rb')
    global play_audio

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)
    count = 0
    # play stream (3)
    while len(data) > 0 and play_audio:
        stream.write(data)
        data = wf.readframes(CHUNK)
        count += 1

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()
    # print "the loop looped for",count," times"


def start_playing():
    global play_audio
    t = threading.Thread(target = play)
    play_audio = True
    t.start()

def stop_playing():
    global play_audio  
    play_audio = False

def is_playing():
    global play_audio
    return play_audio