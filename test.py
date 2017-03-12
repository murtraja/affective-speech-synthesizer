import emossifier
import get_voice as gv
emossifier.get_emotions_from_file('sample.txt')
gv.start_audio_file_generation(emossifier.sentences, emossifier.emotions)