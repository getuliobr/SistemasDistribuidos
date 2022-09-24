"""
    Descrição: Interface gráfica para envio de arquivos 
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 23 / 09 / 2022
"""
from fileinput import filename
import os
import time
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
import threading
from ex2_client import Client

# Classe para a interface gráfica
class GUI(Client):

    def __init__(self):
        # Inicializa a classe client
        super().__init__()
        # Seta variavel da janela
        self.window = Tk()

        # Seta titulo e icone da janela
        self.programIcon = PhotoImage(file='./resources/programIcon.png')
        self.window.iconphoto(False, self.programIcon)        
        self.window.iconbitmap('./resources/programIcon.ico')
        self.window.title('Envie seu arquivo para o servidor')

        # Seta variaveis de controle dos widgets
        self.last_uploaded_file = StringVar()
        self.last_uploaded_file.set("Ultimo arquivo enviado: ")   
        self.last_uploaded_file_color = StringVar()
        self.last_uploaded_file_color.set("green")
        self.filename = ""

        # Seta tamanhos da janela
        self.window.geometry("500x500")
        self.window.minsize(500, 500)
        self.window.maxsize(800, 800)

        # Cor de fundo da janela
        self.window.config(background = "white")

        # Cria label de texto 
        self.label_file_explorer = Label(self.window,
            text = "Escolha um arquivo para enviar para o servidor", bg = "white",
            height=4,
            fg = "blue")
        self.label_file_explorer.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.label_file_explorer.columnconfigure(0, weight=2)

        # Cria label de texto para o ultimo arquivo enviado
        self.label_last_file = Label(self.window,
                textvariable = self.last_uploaded_file, bg = "white",
                height=4,
                fg = "green")

        # Cria botao para escolher arquivo
        self.button_explore = Button(self.window,
                        text = "Escolher arquivo",
                        command = self.browseFiles)

        # Cria botao para enviar arquivo
        self.button_upload = Button(self.window,
                        text = "Upload",
                        command = self.uploadFiles)

        # Cria botao para Sair do programa
        self.button_exit = Button(self.window,
                        text = "Sair",
                        command = self.closeApp)

        # Inicializa os widgets na tela
        self.label_file_explorer.pack()
        self.button_explore.pack(pady=3)
        self.button_upload.pack(pady=3,  anchor=CENTER)
        self.label_last_file.pack(pady=3, anchor=S, side=BOTTOM)
        self.button_exit.pack(side=BOTTOM, anchor=S ,pady=3)

        # Inicia a janela
        self.window.mainloop()

    # Função para escolher arquivo
    def browseFiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",
                title = "Escolha um arquivo",
                filetypes = (("All files",
                    "*.*"),
                    ("all files",
                    "*.*")))
        

        self.label_file_explorer.configure(text="Arquivo selecionado: "+self.filename)
    
    # Função para criar thread de upload do arquivo selecionado
    def uploadFiles(self):
        threading.Thread(target=self.upload).start()
        
    # Função para upload do arquivo selecionado
    def upload(self):
        # Verifica se o arquivo selecionado é valido
        if os.path.exists(self.filename):
            # Cria barra de progresso
            pb1 = Progressbar(
                self.window, 
                orient=HORIZONTAL, 
                length=300,
                mode='determinate'
                )
            pb1.pack(pady=20)

            # Transforma nome do arquivo
            fileToUpload = self.filename
            threading.Thread(target=self.runWithPath, args=(fileToUpload,)).start()

            # Inicia barra de progresso
            self.startedPercentage = True
            while self.startedPercentage:
                time.sleep(1)
                self.window.update_idletasks()
                pb1['value'] = self.percentage
            pb1.destroy()

            # Se o upload foi bem sucedido, seta mensagem de sucesso e atualiza a label de ultimo arquivo enviado
            if self.uploadSuccessfull:
                message = Label(self.window, text='File Uploaded Successfully! =D', foreground='green')
                message.pack(pady=20)
                self.last_uploaded_file.set("Ultimo arquivo enviado com sucesso: "+fileToUpload.split('/')[-1])
                self.label_last_file.configure(fg="green")
            # Se o upload não foi bem sucedido, seta mensagem de erro e atualiza a label de ultimo arquivo enviado
            else:
                message = Label(self.window, text='File Upload Failed. =(', foreground='red')
                message.pack(pady=20)
                self.last_uploaded_file.set("Ultimo arquivo não enviado: "+fileToUpload.split('/')[-1])
                self.label_last_file.configure(fg="red")
            # Atualiza a janela
            time.sleep(1)
            self.window.update_idletasks()
            time.sleep(2)
            message.forget()
    
    # Função para fechar a janela
    def closeApp(self):
        os._exit(0)

# Inicializa a classe GUI
gui = GUI()

    

    
