#OS : macOS
#Python 3.9.2
#editor : vscode
import os
import json
import re
import tkinter as tk
from tkinter import filedialog

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from linebot import LineBotApi
from linebot.models import TextSendMessage


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("300x400")
        self.master.title("main.py")
        self.pack()
        self.create_file_button()
        self.create_file_label()
        self.create_upload_button()

    def create_file_button(self):
        self.open_file = tk.Button(self,width=15,height=5)
        self.open_file["text"] = 'ファイルを選択'
        self.open_file["command"] = self.open_file_pdf
        self.open_file.pack(side='top')

    def create_file_label(self):
        self.l_l = tk.Label(self,width=20)
        self.file_name = tk.StringVar()
        self.file_name.set('ファイル未選択')
        self.l_l["textvariable"] = self.file_name
        self.l_l["bg"] = '#99CCFF'
        self.l_l.pack(pady=20)

    def create_upload_button(self):
        self.upload_button = tk.Button(self,width=5,height=1)
        self.upload_button["text"] = '送信'
        self.upload_button["command"] = self.send_test_text
        self.upload_button.pack(side='bottom',pady=40)

    def open_file_pdf(self):
        typ = [('pdfファイル','*.pdf')] 
        dir = ''
        directory_name = filedialog.askopenfilename(filetypes=typ,initialdir=dir)
        self.directory_name = directory_name
        pattern = '^.+/(?P<name>.*)'
        file_name = re.search(pattern,directory_name)
        self.file_name.set(file_name[1])

    def send_test_text(self):
        print('test')


root = tk.Tk()
app = Application(master=root)
app.mainloop()