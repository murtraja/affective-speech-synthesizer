from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
import PyQt4
import sys
import textract
from cStringIO import StringIO
import emossifier
import get_voice as gv
import play_voice as pv
import time
import os

class GUI(QtGui.QWidget):
    def __init__(self):
        super(GUI, self).__init__();
        self.initGUI()
        self.file_name = ""
        self.ispdf = False
        self.is_second_loaded = False
        self.is_third_loaded = False
        
        
    def initGUI(self):
        '''
        idea:
        there are 4 compartments
        1st - file path line edit and load file button
        2nd - the text edit widget AND two buttons - speak neutral and speak affective
        3rd - media player
        4th - about 
        
        now each compartment will have a top level widget
        
        furthermore, the following shows the events and the corresponding widgets that they reveal
        
        program start - compartment 1 and 4
        load click - compartment 2
        speak click - compartment 3
        '''
        self.main_layout = QtGui.QVBoxLayout()
        
        #    FIRST COMPARTMENT
        self.btn_load = QtGui.QPushButton("&Load File")
        self.btn_load.clicked.connect(self.on_click_load_file)
        self.ledit_file_name = QtGui.QLineEdit("Path of the file to be selected")
        self.ledit_file_name.setMinimumWidth(300)
        self.ledit_file_name.setReadOnly(True)
        com1_layout = QtGui.QHBoxLayout()
        com1_layout.addWidget(self.ledit_file_name, 5)
        com1_layout.addWidget(self.btn_load, 1)
        self.main_layout.addLayout(com1_layout)

        #    FOURTH COMPARTMENT    
        font = QtGui.QFont();
        font.setPointSize(13);
        font.setBold(True);    
        self.label_about_project = QtGui.QLabel('''
                  ABOUT THE PROJECT
                  
        This project was motivated by the fact that the
        pdf readers read the text in a monotonous way
        and no emotion value is attached to it.
        This small project tries to not only identify
        the underlying emotions for the input text, but
        also it speaks it in that way!
        ''')
        self.label_about_project.setFont(font)
        self.label_about_us = QtGui.QLabel('''
            THE TEAM
            
        - Pranjal Bhor
        - Vaibhav Chaudhari
        - Prathamesh Dharangutte
        - Murtaza Raja
        ''')
        self.label_about_us.setFont(font)
        self.com4_layout = QtGui.QHBoxLayout()
        self.com4_layout.addWidget(self.label_about_project, 3)
        self.com4_layout.addWidget(QtGui.QLabel(''))
        self.com4_layout.addWidget(self.label_about_us, 3)
        self.main_layout.addLayout(self.com4_layout)
        
        self.setLayout(self.main_layout)
        self.setWindowTitle("Affective Speech Synthesizer")
        self.setGeometry(600, 200, 100,100)
        #self.setFixedSize(730, 300)
        self.show()

    def makeSentenceEmotionCompartment(self):
        '''
        There is a main widget here which takes care of 
        the whole sentence and emotion layout
        call this widget_sentence_emotion

        this widget uses QVBoxLayout (main_layout)which
        contains another Widget - widget_sentence_emotion_pair

        this widget uses the QHBoxLayout (sub_layout) which contains
        two widgets one line edit and one QComboBox

        '''

        self.widget_sentence_emotion = QtGui.QScrollArea()
        main_layout = QtGui.QVBoxLayout()

        for sentence, emotion in zip(emossifier.sentences, emossifier.emotions):
            widget_sentence_emotion_pair = QtGui.QWidget()
            sub_layout = QtGui.QHBoxLayout()

            ledit_sentence = QtGui.QLineEdit(sentence)
            cb_emotion = QtGui.QComboBox()
            cb_emotion.addItems(gv.emotions_from_data)
            cb_emotion.setCurrentIndex(gv.emotions_from_data.index(emotion))
            sub_layout.addWidget(ledit_sentence, 5)
            sub_layout.addWidget(cb_emotion)

            widget_sentence_emotion_pair.setLayout(sub_layout)

            main_layout.addWidget(widget_sentence_emotion_pair)
        subwidget_sentence_emotion = QtGui.QWidget()
        subwidget_sentence_emotion.setLayout(main_layout)
        self.widget_sentence_emotion.setWidget(subwidget_sentence_emotion)
        self.widget_sentence_emotion.setWidgetResizable(True)
        self.widget_sentence_emotion.setMinimumHeight(400)
        # self.widget_sentence_emotion = subwidget_sentence_emotion





    def addSecondCompartment(self):
        #self.setFixedSize(730, 600)
        if self.is_second_loaded:
            # remove the second compartment here
            self.main_layout.removeWidget(self.widget_second_compartment)
            self.widget_second_compartment.close()
        else:
            self.is_second_loaded = True
        self.widget_second_compartment = QtGui.QWidget()
        self.com2_layout = QtGui.QVBoxLayout()

        self.makeSentenceEmotionCompartment()
        self.com2_layout.addWidget(self.widget_sentence_emotion)
        
        com2_sublayout = QtGui.QHBoxLayout()
        self.btn_speak_neutral = QtGui.QPushButton('Speak in Neutral Voice')
        self.btn_speak_neutral.clicked.connect(self.on_click_speak_neutral_handle)
        self.btn_speak_affective = QtGui.QPushButton('Speak in Affective Voice')
        self.btn_speak_affective.clicked.connect(self.on_click_speak_affective_handle)
        dummy_label = QtGui.QLabel("")
        com2_sublayout.addWidget(self.btn_speak_neutral)
        com2_sublayout.addWidget(dummy_label)
        com2_sublayout.addWidget(self.btn_speak_affective)
        
        self.com2_layout.addLayout(com2_sublayout)
        self.com2_layout.setSpacing(3)
        self.widget_second_compartment.setLayout(self.com2_layout)
        self.main_layout.insertWidget(1, self.widget_second_compartment)
    
    def addActions(self):
        self.playAction = QtGui.QAction(
                self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play",
                self, shortcut="Ctrl+P", enabled=False,
                triggered=self.mediaObject.play)

        self.pauseAction = QtGui.QAction(
                self.style().standardIcon(QtGui.QStyle.SP_MediaPause),
                "Pause", self, shortcut="Ctrl+A", enabled=False,
                triggered=self.mediaObject.pause)

        self.stopAction = QtGui.QAction(
                self.style().standardIcon(QtGui.QStyle.SP_MediaStop), "Stop",
                self, shortcut="Ctrl+S", enabled=False,
                triggered=self.mediaObject.stop)
        
    
    def addThirdCompartment(self):
        #self.setFixedSize(730, 800)
        self.com3_layout = QtGui.QVBoxLayout()
        self.mediaObject = Phonon.MediaObject()
        self.addActions()
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkGray)
        self.timeLcd = QtGui.QLCDNumber()
        self.timeLcd.setPalette(palette)
        self.timeLcd.display("00:00")
        
        self.mediaObject.stateChanged.connect(self.stateChanged)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.setTickInterval(1000)
        self.mediaObject.tick.connect(self.tick)
        
        self.slider = Phonon.SeekSlider(self)
        self.slider.setMediaObject(self.mediaObject)
        
        
        
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addActions([self.playAction, self.pauseAction, self.stopAction])
        
        seekerLayout = QtGui.QHBoxLayout()
        seekerLayout.addWidget(self.slider)
        seekerLayout.addWidget(self.timeLcd)
        

        
        self.volumeSlider = Phonon.VolumeSlider(self)
        self.volumeSlider.setAudioOutput(self.audioOutput)
        #self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Maximum,
        #QtGui.QSizePolicy.Maximum)

        volumeLabel = QtGui.QLabel()
        volumeLabel.setPixmap(QtGui.QPixmap('images/volume.png'))
        
        playbackLayout = QtGui.QHBoxLayout()
        playbackLayout.addWidget(self.toolbar)
        playbackLayout.addStretch(10)
        playbackLayout.addWidget(volumeLabel)
        playbackLayout.addWidget(self.volumeSlider)
        
        mainLayout = QtGui.QVBoxLayout()
        #mainLayout.minimumSize()
        mainLayout.addLayout(seekerLayout)
        mainLayout.addLayout(playbackLayout)
        
        widget = QtGui.QWidget()
        widget.setLayout(mainLayout)
        
        self.com3_layout.addWidget(widget, 0, QtCore.Qt.AlignCenter)
        self.main_layout.insertLayout(2, self.com3_layout)
    
    def tick(self, time):
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.timeLcd.display(displayTime.toString('mm:ss'))
    
    def stateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            if self.mediaObject.errorType() == Phonon.FatalError:
                QtGui.QMessageBox.warning(self, "Fatal Error",
                        self.mediaObject.errorString())
            else:
                QtGui.QMessageBox.warning(self, "Error",
                        self.mediaObject.errorString())

        elif newState == Phonon.PlayingState:
            self.playAction.setEnabled(False)
            self.pauseAction.setEnabled(True)
            self.stopAction.setEnabled(True)

        elif newState == Phonon.StoppedState:
            self.stopAction.setEnabled(False)
            self.playAction.setEnabled(True)
            self.pauseAction.setEnabled(False)
            self.timeLcd.display("00:00")

        elif newState == Phonon.PausedState:
            self.pauseAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.playAction.setEnabled(True)
    
    def Music_handle(self):
        self.mediaObject.setCurrentSource(Phonon.MediaSource("output/output.wav"))
        self.mediaObject.play()
    
    def on_click_speak_neutral_handle(self):
        self.on_click_speak(True)
        
    def on_click_speak_affective_handle(self):
        self.on_click_speak(False)
    
    #This function speaks the text with its emotions
    def on_click_speak(self, want_neutral):
        if not self.is_third_loaded:
            self.is_third_loaded = True
            self.addThirdCompartment()
	    #check here if the file name is valid
        #now pass the file name to emossifer and get the output
        emossifier.get_emotions_from_content(self.tedit_file_contents.toPlainText(), want_neutral)
        no_of_sentences = len(emossifier.sentences)
        print "No. of sentences classified:", no_of_sentences
        classified_sentences = "\n\n".join([x + "\n"+y.upper() for (x,y) in zip(emossifier.sentences, emossifier.emotions)])
        print classified_sentences
        
        #Before inserting new text, delete old one
        print "here"
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.tedit_file_contents.clear()
        self.tedit_file_contents.setFont(font)
        self.tedit_file_contents.append(classified_sentences+"\n\n"+"All "+str(no_of_sentences)+" sentences processed successfully!")
        
        #So now we have the sentences emossifier.sentences and emotions emossifier.emotions
        #we pass it to the get_voice module	
        gv.start_audio_file_generation(emossifier.sentences, emossifier.emotions)
        time.sleep(1)
        #This is a blocking call, try to make it non blocking, pass a callback?
        #pv.start_playing()
        self.Music_handle()
        
    #On clicking the 'load file' button
    #display a file selection widget   
    def on_click_load_file(self):
        self.ledit_file_name.setText(QtGui.QFileDialog.getOpenFileName())
        self.file_name = self.ledit_file_name.text()
        path_array = self.file_name.split("/")
        neededWord = str(path_array[len(path_array)-1])
        data = None
        if neededWord.split(".")[1] == "pdf":
            self.ispdf = True
            data = textract.process(str(self.file_name), encoding='ascii')
            data = data[:-2]
            self.tedit_file_contents.append(str(data))
            temp_file = open("/tmp/pdf_temp.txt","w")
            temp_file.write(data)
            temp_file.close()
        else:
            self.ispdf = False
            fd = open(str(self.file_name))
            data = fd.read()

        emossifier.get_emotions_from_content(data, False)

        self.addSecondCompartment()

    
def start():
    app = QtGui.QApplication(sys.argv)
    main_window = GUI()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    start()
    
