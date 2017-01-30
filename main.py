#!/usr/bin/python

from Tkinter import *
from tkFileDialog import askopenfilename
import emossifier

top = Tk()
# Code to add widgets will go here...
entry_file_path_text = StringVar()
text_file = None

lbl_file_path = None
def open_file(filename):
	f = open(filename)
	global text_file
	'''
	before inserting new text, delete old one
	'''
	text_file.delete("1.0", "end")
	text_file.insert("1.0", f.read())
def on_click_open_file():
	filename = askopenfilename(parent=top)
	global entry_file_path_text
	# global lbl_file_path
	#lbl_file_path['text'] = filename
	entry_file_path_text.set(filename)
	'''
	now try to read and open the file here
	'''
	open_file(filename)
def on_click_speak():
	pass
	'''
	check here if the file name is valid
	'''

	'''
	now pass the file name to emossifer and get the output
	'''
	# print entry_file_path_text.get()
	emossifier.get_emotions_from_file(entry_file_path_text.get())
	no_of_sentences = len(emossifier.sentences)
	print "No. of sentences classified:", no_of_sentences
	classified_sentences = "\n\n".join([x + "\n"+y.upper() for (x,y) in zip(emossifier.sentences, emossifier.emotions)])
	print classified_sentences
	global text_file
	'''
	before inserting new text, delete old one
	'''
	text_file.delete("1.0", "end")
	text_file.insert("1.0", classified_sentences+"\n\n"+"All "+str(no_of_sentences)+" sentences processed successfully!")

def on_change_entry_file_path():
	pass
	'''
	now display the file contents here!
	'''

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

btn_open_file = Button ( frame_top, command=on_click_open_file, text="Load Text File" )
btn_open_file.pack(side=LEFT)

text_file = Text(frame_middle, width = 100)
text_file.grid(row=0, column=0, sticky='nsew')

scrollbar_file = Scrollbar(frame_middle, command=text_file.yview)
scrollbar_file.grid(sticky='nsew', row=0, column=1)
text_file['yscrollcommand'] = scrollbar_file.set

btn_speak = Button(frame_bottom, command=on_click_speak, text="Speak")
btn_speak.pack(side=BOTTOM)

top.mainloop()