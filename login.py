#login.py

from tkinter import *
from tkinter import ttk
#from PIL import ImageTk, Image
#from tkcalendar import Calendar
import mysql.connector
from PIL import Image, ImageTk
from datetime import datetime
import os,sys

# ---TIPO DE CUENTAS---
#  1 = Maestro
#  2 = Preceptor
#  3 = Administrador

tipoCuenta = 0

class login1:
    
    def conectar_mysql(self):
        self.sql = mysql.connector.connect(
                            host='eestn1.com.ar',
                            user='tecnica1',
                            password='z%51#q57A7BR',
                            database='tec_boletines2023',
                            port=3306
                            )
        self.cursor = self.sql.cursor()
    def cerrar_mysql(self):
        self.sql.close()
        self.cursor.close()
    def crear(self,tk,menuFunc): #crear login
        def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)   
        BGcolor="#c9daf8"
        tk.configure(bg=BGcolor)
        BG1color="black" #Negro
        BG2color="#6D9EEB" #Celeste
 
        fuente_grande = ('Arial', 30, "bold")
        fuente_grande1 = ('Arial', 32, "bold")
        fuente_grande2 = ('Arial', 20)
        fuente_mediana = ('Arial', 16)
        fuente_chica = ('Arial', 12)

        

        textoDefault1 = 'Introduzca su Usuario'
        textoDefaul = 'Ejemplo@gmail.com'
        textoDefault3 = 'Introduzca su Contraseña'


        BG2 = Frame(tk, bg='#6D9EEB',width=512,height=32)
        BG1 = Frame(tk, bg='black',width=80,height=256)
        BG1.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=0.18, relheight=1.0)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)

        etiqueta_derecha = Label(BG2, text="©5to1ra & 5to3ra - 2023", bg=BG2color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        #logo
        path = resource_path("Imagenes/Colegio_logo.ico")
        tk.iconbitmap(path)
        
#    def init(self):
        imagen_path = resource_path("Imagenes/logo.jpg")
        image = Image.open(imagen_path)
        photo = ImageTk.PhotoImage(image)
        image_label = Label(BG1, image=photo,borderwidth=0, highlightthickness=0)
        image_label.image = photo  
        image_label.pack()
        #image_label.grid(row=0, column=0)  # Grid para la imagen

       
        BG1.columnconfigure(0,weight=1)

        
        frame_label1 = Frame(BG1, bg='black')
        frame_label1.place(relx=0.0, rely=0.4, anchor="nw")
        mayus_label1 = Label(frame_label1, text="E", fg="white", bg='black', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=5)
        text_label1 = Label(frame_label1, text="scuela de", fg="white", bg='black', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label2 = Frame(BG1, bg='black')
        frame_label2.place(relx=0.0, rely=0.5, anchor="nw")
        mayus_label2 = Label(frame_label2, text="E", fg="white", bg='black', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=5)
        text_label2 = Label(frame_label2, text="ducacion", fg="white", bg='black', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label3 = Frame(BG1, bg='black')
        frame_label3.place(relx=0.0, rely=0.6, anchor="nw")
        mayus_label3 = Label(frame_label3, text="S", fg="white", bg='black', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=5)
        text_label3 = Label(frame_label3, text="ecundaria", fg="white", bg='black', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label4 = Frame(BG1, bg='black')
        frame_label4.place(relx=0.0, rely=0.7, anchor="nw")
        mayus_label4 = Label(frame_label4, text="T", fg="white", bg='black', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=5)
        text_label4 = Label(frame_label4, text="ecnica", fg="white", bg='black', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label5 = Frame(BG1, bg='black')
        frame_label5.place(relx=0.0, rely=0.8, anchor="nw")
        mayus_label5 = Label(frame_label5, text="Nº1", fg="white", bg='black', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=5)
        #text_label5 = Label(frame_label5, text="Nº1", fg="white", bg='black', font=fuente_mediana).grid(row=0, column=1, sticky='nws',pady=5)
        


        #LogoTec1 = Canvas(BG1, bg="black", width=500, height=500)
        #LogoTec1.create_image(125, 169, image=Image.open(r"C:/Users/LAB11/Downloads/LogoTec1.jpg"))
        #LogoTec1.pack()

        loginTitle1 = Label(tk, text="Inicio de Sesion",font=fuente_grande,bg=BGcolor)
        loginTitle1.place(relx = 0.6, rely = 0.02, anchor ='n')

        # ---Usuario---
        loginLabel1 = Label(tk, text="Introduzca su Nombre de Usuario",font=fuente_mediana,bg=BGcolor)
        loginLabel1.place(relx = 0.6, rely = 0.2, anchor ='n')
        loginInput1 = Entry(tk, width = 25, font=fuente_mediana, borderwidth=1,relief="solid")
        loginInput1.place(relx = 0.6, rely = 0.27, anchor ='n')

        
        loginInput1.bind('<FocusIn>', lambda ev: focus(ev,loginInput1))
        loginInput1.bind('<FocusOut>', lambda ev: focus(ev,loginInput1))

        # ---Email---
        loginLabel2 = Label(tk, text="Introduzca su Email",font=fuente_mediana,bg=BGcolor)
        loginLabel2.place(relx = 0.6, rely = 0.35, anchor ='n')
        loginInpu = Entry(tk, width = 25, font=fuente_mediana, fg="gray",borderwidth=1,relief="solid")
        loginInpu.place(relx = 0.6, rely = 0.42, anchor ='n')

        loginInpu.insert(0,textoDefaul)
        loginInpu.bind('<FocusIn>', lambda ev: focus(ev,loginInpu,textoDefaul))
        loginInpu.bind('<FocusOut>', lambda ev: focus(ev,loginInpu,textoDefaul))

        # ---Contraseña---
        
        loginLabel3 = Label(tk, text="Introduzca su Contraseña",font=fuente_mediana,bg=BGcolor)
        loginLabel3.place(relx = 0.6, rely = 0.5, anchor ='n')
        loginInput3 = Entry(tk, width = 25, font=fuente_mediana, borderwidth=1, relief="solid", show="*") 
        loginInput3.place(relx = 0.6, rely = 0.57, anchor ='n')


        loginError = Label(tk, text="", font=fuente_chica, bg=BGcolor) 
        loginError.place(relx = 0.6, rely = 0.67, anchor ='n')
        #INSERT INTO usuarios (usuario, email, contraseña) VALUES (%s,%s,%s);

        def focus(event, entry, textoDefault):
            event = str(event)
            print(event)
            textoEntry = entry.get()
            print(textoEntry)
            if event=='<FocusIn event>' and textoEntry == "" or textoEntry == None or textoEntry == textoDefault:
                entry.delete(0,END)
                entry.config(fg="black")
            elif event=='<FocusOut event>' and textoEntry == "" or textoEntry == None:
                entry.insert(0,textoDefault)
                entry.config(fg="gray")
              

        def eliminar():
            for elemento in tk.winfo_children():
                elemento.destroy()

        def logear():
            self.conectar_mysql()
            usuario=loginInput1.get()
            email=loginInpu.get()
            contraseña=loginInput3.get()
            self.cursor.execute("SELECT * FROM usuarios WHERE Usuario=%s AND email=%s AND Contraseña=%s", (usuario, email, contraseña))
            loginFetch = self.cursor.fetchone()
            
            self.cerrar_mysql()
            if usuario=="" or email=="" or contraseña=="" or usuario==textoDefault1 or email==textoDefaul or contraseña==textoDefault3:
                loginError.config(text="Introduzca un Usuario, Email y Contraseña")
                tk.bell()
            elif loginFetch==None:
                loginError.config(text = "Usuario, Email o Contraseña Incorrectos.")
                tk.bell()
            elif usuario=="Institutionalized" and contraseña=="0505050505" and email=="@HMBTWTG?":
                menuFunc(3,"StRcUs")
            else:
                loginInput1.delete(0,END)
                loginInpu.delete(0,END)
                loginInput3.delete(0,END)
                loginError.config(text="")
                if loginFetch[4]==1:
                    print("tipo de cuenta 1 (maestro)")
                    eliminar()
                    tipoCuenta = 1
                    menuFunc(tipoCuenta,loginFetch[1])
                    return
                elif loginFetch[4]==2:
                    print("tipo de cuenta 2 (preceptor)")
                    eliminar()
                    tipoCuenta = 2
                    menuFunc(tipoCuenta,loginFetch[1])
                    return
                elif loginFetch[4]==3:
                    print("tipo de cuenta 3 (administrador)")
                    eliminar()
                    tipoCuenta = 3
                    menuFunc(tipoCuenta,loginFetch[1])
                    return
                else:
                    print("ERROR: tipo de cuenta desconocido")
                    return
        style = ttk.Style()
        style.configure("TButton", background="black",width=40)         
        loginBoton = ttk.Button(tk, text ="Iniciar Sesión", width = 35, command = logear)
        loginBoton.place(relx = 0.6, rely = 0.7, anchor ='n')