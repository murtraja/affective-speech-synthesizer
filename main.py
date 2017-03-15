#!/usr/bin/python

from Tkinter import *
from tkFileDialog import askopenfilename
import emossifier
import get_voice as gv
import play_voice as pv
import textract
from cStringIO import StringIO

#Top level TKinter object
top = Tk()
top.title("Highly trained emotional speech synthesis")
#global variables
entry_file_path_text = StringVar()
text_file = None
is_pdf = False
lbl_file_path = None

#Function to open file and set its contents
#in the display window
def open_file(filename):
	f = open(filename)
	global text_file
	'''
	before inserting new text, delete old one
	'''
	text_file.delete("1.0", "end")
	text_file.insert("1.0", f.read())

#Function to handle opening of text files
def on_click_open_text_file():
	filename = askopenfilename(parent=top)
	global entry_file_path_text
	entry_file_path_text.set(filename)

	#now try to read and open the file here
	open_file(filename)

#Function to handle opening of PDF files
def on_click_open_PDF_file():
  filename = askopenfilename(parent=top)
  data = textract.process(filename, encoding='ascii')
  data = data[:-2]
  temp_file = open("/tmp/pdf_temp.txt","w")
  temp_file.write(data)
  temp_file.close()
  
  global entry_file_path_text
  entry_file_path_text.set(filename)
  global is_pdf
  is_pdf = True
  open_file("/tmp/pdf_temp.txt")
  
def on_click_speak():
	#check here if the file name is valid
    #now pass the file name to emossifer and get the output
	global is_pdf
	if not is_pdf:
	  emossifier.get_emotions_from_file(entry_file_path_text.get())
	else:
	  emossifier.get_emotions_from_file("/tmp/pdf_temp.txt")
	no_of_sentences = len(emossifier.sentences)
	print "No. of sentences classified:", no_of_sentences
	classified_sentences = "\n\n".join([x + "\n"+y.upper() for (x,y) in zip(emossifier.sentences, emossifier.emotions)])
	print classified_sentences
	global text_file
	
	#Before inserting new text, delete old one
	text_file.delete("1.0", "end")
	text_file.insert("1.0", classified_sentences+"\n\n"+"All "+str(no_of_sentences)+" sentences processed successfully!")

	#So now we have the sentences emossifier.sentences and emotions emossifier.emotions
	#we pass it to the get_voice module	
	gv.start_audio_file_generation(emossifier.sentences, emossifier.emotions)
	
	#This is a blocking call, try to make it non blocking, pass a callback?
	pv.start_playing()

def on_change_entry_file_path():
	pass
	'''
	now display the file contents here!
	'''

if __name__ == "__main__":
  
  frame_top = Frame(top)
  frame_top.pack()

  frame_middle = Frame(top)
  frame_middle.pack()

  frame_bottom = Frame(top)
  frame_bottom.pack()

  lbl_file_path = Label(frame_top, text="File Path")
  lbl_file_path.pack(side=LEFT)

  entry_file_path = Entry(frame_top, bd=5, textvariable=entry_file_path_text, width=100)
  entry_file_path.pack(side=LEFT)

  #button for loading text file
  btn_open_file = Button ( frame_top, command=on_click_open_text_file, text="Load Text File" )
  btn_open_file.pack(side=LEFT)

  #button for loading PDF file
  btn_open_file = Button ( frame_top, command=on_click_open_PDF_file, text="Load PDF File" )
  btn_open_file.pack(side=LEFT)

  text_file = Text(frame_middle, width = 100)
  text_file.grid(row=0, column=0, sticky='nsew')

  scrollbar_file = Scrollbar(frame_middle, command=text_file.yview)
  scrollbar_file.grid(sticky='nsew', row=0, column=1)
  text_file['yscrollcommand'] = scrollbar_file.set

  #button for speaking
  btn_speak = Button(frame_bottom, command=on_click_speak, text="Speak")
  btn_speak.pack(side=BOTTOM)

  top.mainloop()
