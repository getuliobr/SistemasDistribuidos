# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from fileinput import filename
import os
import time
from tkinter import *

# import filedialog module
from tkinter import filedialog
from tkinter.ttk import Progressbar
import threading
from ex2_client import Client

class GUI(Client):

    def __init__(self):
        super().__init__()
        self.window = Tk()

        self.programIcon = PhotoImage(file='./resources/programIcon.png')
        # self.window.iconphoto(False, self.programIcon)
        self.window.iconbitmap('./resources/programIcon.ico')

        self.last_uploaded_file = StringVar()
        self.last_uploaded_file.set("Ultimo arquivo enviado: ")   
        self.last_uploaded_file_color = StringVar()
        self.last_uploaded_file_color.set("green")
        self.filename = ""

        self.window.title('Envie seu arquivo para o servidor')

        self.window.geometry("500x500")
        self.window.minsize(500, 500)
        self.window.maxsize(800, 800)


        self.window.config(background = "white")


        self.label_file_explorer = Label(self.window,
            text = "Escolha um arquivo para enviar para o servidor", bg = "white",
            height=4,
            fg = "blue")

        self.label_last_file = Label(self.window,
                textvariable = self.last_uploaded_file, bg = "white",
                height=4,
                fg = "green")

        self.label_file_explorer.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.label_file_explorer.columnconfigure(0, weight=2)

        self.button_explore = Button(self.window,
                        text = "Escolher arquivo",
                        command = self.browseFiles)

        self.button_exit = Button(self.window,
                        text = "Sair",
                        command = self.closeApp)

        self.button_upload = Button(self.window,
                        text = "Upload",
                        command = self.uploadFiles)



        self.label_file_explorer.pack()
        self.button_explore.pack(pady=3)
        self.button_upload.pack(pady=3,  anchor=CENTER)
        self.label_last_file.pack(pady=3, anchor=S, side=BOTTOM)
        self.button_exit.pack(side=BOTTOM, anchor=S ,pady=3)


        self.window.mainloop()


    def browseFiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",
                title = "Escolha um arquivo",
                filetypes = (("All files",
                    "*.*"),
                    ("all files",
                    "*.*")))
        

        self.label_file_explorer.configure(text="Arquivo selecionado: "+self.filename)
    

    def uploadFiles(self):
        threading.Thread(target=self.upload).start()
        
        
    def upload(self):
        pb1 = Progressbar(
            self.window, 
            orient=HORIZONTAL, 
            length=300,
            mode='determinate'
            )
        pb1.pack(pady=20)
        fileToUpload = self.filename
        threading.Thread(target=self.runWithPath, args=(fileToUpload,)).start()
        self.startedPercentage = True
        while self.startedPercentage:
            time.sleep(1)
            self.window.update_idletasks()
            pb1['value'] = self.percentage
        pb1.destroy()
        message = Label(self.window, text='File Uploaded Successfully!', foreground='green')
        message.pack(pady=20)
        if self.uploadSuccessfull:
            self.last_uploaded_file.set("Ultimo arquivo enviado com sucesso: "+fileToUpload.split('/')[-1])
            self.label_last_file.configure(fg="green")
        else:
            self.last_uploaded_file.set("Ultimo arquivo não enviado: "+fileToUpload.split('/')[-1])
            self.label_last_file.configure(fg="red")
        time.sleep(1)
        self.window.update_idletasks()
        time.sleep(2)
        message.forget()
    
    def closeApp(self):
        os._exit(0)

a = GUI()

    

    
