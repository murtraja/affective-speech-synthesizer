import pyaudio
import wave
import threading

#Global variables
play_audio = True
CHUNK = 1024
FILENAME = "output/output.wav"

#Function to play the audio stream
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

#Function to commence audio playing
def start_playing():
    global play_audio
    t = threading.Thread(target = play)
    play_audio = True
    t.start()

#Function to stop audio playing
def stop_playing():
    global play_audio  
    play_audio = False

#Function to check the status of audio playing
def is_playing():
    global play_audio
    return play_audio
