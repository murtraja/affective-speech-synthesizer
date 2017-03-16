from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
import PyQt4
import sys

class GUI(QtGui.QWidget):
    def __init__(self):
        super(GUI, self).__init__();
        self.initGUI()
    def initGUI(self):
        '''
        idea:
        there are 5 compartments
        1st - file path line edit and load file button
        2nd - the text edit widget AND two buttons - speak neutral and speak affective
        3rd - media player
        4th - about 
        
        now each compartment will have a top level widget
        
        furthermore, the following shows the events and the corresponding widgets that they reveal
        
        program start - compartment 1 and 5
        load click - compartment 2 and 3
        speak click - compartment 4
        '''
        self.main_layout = QtGui.QVBoxLayout()
        
        #    FIRST COMPARTMENT
        self.btn_load = QtGui.QPushButton("load file")
        self.ledit_file_name = QtGui.QLineEdit("some default text in the line edit")
        self.ledit_file_name.setMinimumWidth(300)
        com1_layout = QtGui.QHBoxLayout()
        com1_layout.addWidget(self.ledit_file_name, 5)
        com1_layout.addWidget(self.btn_load, 1)
        self.main_layout.addLayout(com1_layout)

        #    THIRD COMPARTMENT
        

        #    FOURTH COMPARTMENT        
        self.label_about_project = QtGui.QLabel('''
                  ABOUT THE PROJECT
                  
        This project was motivated by the fact that the
        pdf readers read the text in a monotonous way
        and no emotion value is attached to it.
        This small project tries to not only identify
        the underlying emotions for the input text, but
        also it speaks it in that way!
        ''')
        self.label_about_us = QtGui.QLabel('''
            THE TEAM
            
        - Pranjal Bhor
        - Vaibhav Chaudari
        - Prathamesh Dharangutte
        - Murtaza Raja
        ''')
        self.com4_layout = QtGui.QHBoxLayout()
        self.com4_layout.addWidget(self.label_about_project, 3)
        self.com4_layout.addWidget(QtGui.QLabel(''))
        self.com4_layout.addWidget(self.label_about_us, 3)
        self.main_layout.addLayout(self.com4_layout)
        
        self.setLayout(self.main_layout)
        self.setWindowTitle("Affective Speech Synthesizer")
        #self.setMinimumSize(300, 200)
        self.show()
        
        self.setupSignals()
    def addSecondCompartment(self):
        self.com2_layout = QtGui.QVBoxLayout()
        self.tedit_file_contents = QtGui.QTextEdit()
        self.com2_layout.addWidget(self.tedit_file_contents)
        
        com2_sublayout = QtGui.QHBoxLayout()
        self.btn_speak_neutral = QtGui.QPushButton('Speak in Neutral Voice')
        self.btn_speak_neutral.clicked.connect(self.on_click_speak_neutral)
        self.btn_speak_affective = QtGui.QPushButton('Speak in Affective Voice')
        dummy_label = QtGui.QLabel("")
        com2_sublayout.addWidget(self.btn_speak_neutral)
        com2_sublayout.addWidget(dummy_label)
        com2_sublayout.addWidget(self.btn_speak_affective)
        
        self.com2_layout.addLayout(com2_sublayout)
        self.main_layout.insertLayout(1, self.com2_layout)
        
    def addFourthCompartment(self):
        self.com3_layout = QtGui.QVBoxLayout()
        self.slider = QtGui.QSlider(1)
        self.com3_layout.addWidget(self.slider)
        
        self.mediaObject = Phonon.MediaObject(self)
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
        
        self.toolbar = QtGui.QToolBar()
        self.toolbar.addActions([self.playAction, self.pauseAction, self.stopAction])
        self.com3_layout.addWidget(self.toolbar, 0, QtCore.Qt.AlignCenter)
        self.main_layout.insertLayout(2, self.com3_layout)
        
    def on_click_speak_neutral(self):
        self.addFourthCompartment()
    def setupSignals(self):
        self.btn_load.clicked.connect(self.on_click_load);
    def on_click_load(self):
        self.addSecondCompartment()

def start():
    app = QtGui.QApplication(sys.argv)
    main_window = GUI()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    start()
    