from tkinter import *

class BGRViewer(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.QUIT=Button(self)
        self.QUIT["text"]="QUIT"
        self.QUIT.pack({"side":"left"})

        self.hi=Button(self)
        self.hi["text"]="Hello"
        self.hi["command"]=self.say_hi
        self.hi.pack({"side":"left"})

    def say_hi(self):
        print("hi!!!!")


