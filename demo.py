#OS : windows10
#Python 3.9.2
#editor : vscode
import os
import json
import re
import sys
import tkinter as tk
from tkinter import filedialog

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from linebot import LineBotApi
from linebot.models import TextSendMessage


class Application(tk.Frame):
    ##googleAPI##
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    ##LINEAPI##
    file_1 = open('line-info.json','r')
    line_info = json.load(file_1)
    ACCESS_TOKEN = line_info['ACCESS_TOKEN']
    BOT_ID = line_info['USER_ID']
    line_bot_api = LineBotApi(ACCESS_TOKEN)


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("300x400")
        self.master.title("main.py")
        self.pack()
        self.create_file_button()
        self.create_file_label()
        self.create_end_button()
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
        self.upload_button["command"] = self.upload_file_to_drive
        self.upload_button.pack(side='bottom',pady=40)
    
    def create_end_button(self):
        self.end_button = tk.Button(self,width=5,height=1)
        self.end_button["text"] = '終了'
        self.end_button["command"] = sys.exit
        self.end_button.pack(side='bottom',pady=5)

    def open_file_pdf(self):
        typ = [('pdfファイル','*.pdf')] 
        dir = ''
        directory_name = filedialog.askopenfilename(filetypes=typ,initialdir=dir)
        self.directory_name = directory_name
        pattern = '^.+/(?P<name>.*)'
        file_name = re.search(pattern,directory_name)
        self.file_name.set(file_name[1])
    
    def upload_file_to_drive(self):
        drive_file_name = self.file_name.get()
        directory_name = self.directory_name
        ##google-driveのファイルID##
        folder_id = '1cM1sdUliBTIz2giekSskzVjYx8wI7Q_T'
        G_file = self.drive.CreateFile({'title':drive_file_name, 'mimeType':'application/pdf', "parents":[{"id":folder_id}]})
        G_file.SetContentFile(directory_name)
        G_file.Upload()
        self.Send_Line_Url = 'https://drive.google.com/open?id=' + str(G_file['id'])
        self.send_line_message()

    def send_line_message(self):
        message = TextSendMessage(text=self.Send_Line_Url)
        self.line_bot_api.push_message(self.BOT_ID,messages=message)

    def send_test_text(self):
        print('test')


root = tk.Tk()
app = Application(master=root)
app.mainloop()