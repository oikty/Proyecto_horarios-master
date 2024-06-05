import tkinter as tk
from tkinter import ttk
import mysql.connector
import re

# Definir los colores
BGcolor = "#c9daf8"
BG1color = "#212121"
BG2color = "#6D9EEB"
#BLUE = "#6D9EEB"
#BLACK = "#212121"


class registrar1():
    #def __init__(self,ventana,sql,cursor):
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
    def crear(self,ventana,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc,valores=[False]):
        ventana.columnconfigure (0,minsize=0)
        #ventana.columnconfigure (6,minsize=250)

        def eliminar():
            for elemento in ventana.winfo_children():
                elemento.destroy()
        def volver():
            ventana.columnconfigure (0,minsize=0)
            eliminar()
            cuentasFunc(ventana,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)
            return
        
        def registrar():
            mensaje_error.config(text="\n", fg="red")
            # Obtener los valores ingresados por el usuario
            nombre_usuario = entry_usuario.get()
            contraseña = entry_contraseña.get()
            email = entry_email.get()
            confirmar_contraseña = entry_confirmar_contraseña.get()
           
            tipoSelect = entry_tipo.get()
            
            tipo = 0
            for i in tipos:
                if i[1] == tipoSelect:
                    tipo = i[0]
                    print(tipo)
                    break
            if not tipo in (1,2,3):
                print("ERROR: tipo de cuenta no seleccionado o invalido")
                ventana.bell()
                return
            
            if email.count('.') > 3 or email.count('.') == 0 or email.count('@') != 1 or not re.match(r'^[\w-]+@', email):
                # Si el correo no cumple con el formato o tiene más de una "@", mostramos un mensaje de error
                tk.messagebox.showerror("Error", "Dirección de correo inválida su correo debe verse asi example@gmail.com")
                entry_email.delete(0, tk.END)  # Borramos el contenido del Entry
                return False 
            
            LoginValores = [nombre_usuario,contraseña,email,tipo,confirmar_contraseña]
            SQLmaterias = []
            if tipo == 1:
                for materia in seleccionM:
                    materia = ",".join(materia)
                    SQLmaterias.append(materia)
                    print(materia)
                SQLmaterias = list(set(SQLmaterias)) #remover materias duplicadas si por cualquier razon las hay
                SQLmaterias = ";".join(SQLmaterias)
                print(SQLmaterias)

            # --CHECKEO TODOS LOS CAMPOS LLENADOS--
            incompleto = False
            for valor in LoginValores:
                if valor is None or valor=="":
                    incompleto=True
            
            if incompleto is True:
                mensaje_error.config(text="Llene todos los campos\n", fg="red")
                ventana.bell()
                return

            
            # --CHECKEO CONTRASEÑAS COINCIDEN--
            if contraseña != confirmar_contraseña:
                # Mostrar un mensaje de error si las contraseñas no coinciden
                mensaje_error.config(text="Las contraseñas no coinciden\n", fg="red")
                ventana.bell()
                return
            

            # --CHECKEO CONTRASEÑA Y USUARIO SON DIFERENTES--
            if contraseña == nombre_usuario:
                # Mostrar un mensaje de error si la contraseña y el nombre son lo mismo
                mensaje_error.config(text="El usuario y la contraseña\nno pueden ser iguales.", fg="red")
                ventana.bell()
                return

            self.conectar_mysql()
            # --CHECKEO CUENTA YA EXISTE--
            self.cursor.execute(f"SELECT ID FROM usuarios WHERE usuario='{nombre_usuario}' or email='{email}' ")
            registrado = self.cursor.fetchone()
            self.cerrar_mysql()
            #si la cuenta ya existe y no se esta editando, si no que registrando un usuario nuevo:
            if not registrado is None and valores[0] is False: 
                mensaje_error.config(text="Esta Cuenta ya Existe\n", fg="red")
                ventana.bell()
                return
            


            # --SI TODOS LOS CHECKEOS SE PASAN, REGISTRAR O ACTUALIZAR CUENTA--
            if LoginValores[3]==1: #en el caso que el tipo sea maestro, agrega horarios al query de insert
                print("a")
                queryMaterias = f", '{SQLmaterias}'"
                queryMaterias2 = ",MATERIAS"
                queryMaterias3 = f", MATERIAS='{SQLmaterias}'"
            else: #en cualquier otro caso, no agrega nada
                print("b")
                queryMaterias = ""
                queryMaterias2 = ""
                queryMaterias3 = ""

            if valores[0]==True: #en el caso de que se este editando un usuario existente

                if valores[1] is False: #en el caso que la contraseña este oculta
                    queryContraseña = f", contraseña='{LoginValores[1]}'"
                else:
                    queryContraseña = ""

                print(LoginValores)
                print(queryContraseña)
                print(queryMaterias3)
                print(valores[6])
                self.conectar_mysql()
                self.cursor.execute(f"""UPDATE usuarios SET
                               usuario='{LoginValores[0]}',
                               email='{LoginValores[2]}'{queryContraseña},
                               tipo='{LoginValores[3]}'{queryMaterias3}
                               WHERE ID={valores[6]}""")
                self.sql.commit()
                print("Usuario Actualizado")
                self.cerrar_mysql()


            else: #en el caso que se este registrando un usuario nuevo
                self.conectar_mysql()
                self.cursor.execute(f"INSERT INTO usuarios (usuario,email,contraseña,tipo{queryMaterias2}) VALUES ('{LoginValores[0]}', '{LoginValores[2]}', '{LoginValores[1]}', '{LoginValores[3]}'{queryMaterias})")
                print("Usuario Registrado")
                self.sql.commit()
                mensaje_error.config(text="Usuario Registrado Exitosamente\n", fg="black")
                self.cerrar_mysql()
            
            #vaciar todos los campos
            entry_usuario.delete(0, tk.END)
            entry_contraseña.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_confirmar_contraseña.delete(0, tk.END)
            entry_tipo.current(0)

            #si se estaba editando, volver a cuentas.py
            if valores[0]==True:
                volver()
                    

        def arroba(event):
            contenido = entry_email.get()
            # Utilizamos una expresión regular para verificar el formato del correo
            if contenido.count('.') > 3 or contenido.count('.') == 0 or contenido.count('@') != 1 or not re.match(r'^[\w-]+@', contenido):
                if len(contenido) >0:
                    # Si el correo no cumple con el formato o tiene más de una "@", mostramos un mensaje de error
                    tk.messagebox.showerror("Error", "Dirección de correo inválida su correo debe verse asi example@gmail.com")
                    entry_email.delete(0, tk.END)  # Borramos el contenido del Entry
                    return False
                
        def limite(event):
            contenido = entry_email.get()
            contenido2 = entry_usuario.get()
            contenido3 = entry_contraseña.get()
            contenido4 = entry_confirmar_contraseña.get()
            
            if len(contenido) > 100:
                # Limitar el contenido a 11 caracteres
                nuevo_contenido = contenido[:100]
                entry_email.delete(0, tk.END)
                entry_email.insert(0, nuevo_contenido)
                tk.messagebox.showerror("Error", "Solo se permiten 100 caracteres")
            elif len(contenido2) > 50:
                nuevo_contenido2 = contenido2[:50]
                entry_usuario.delete(0, tk.END)
                entry_usuario.insert(0, nuevo_contenido2)
                tk.messagebox.showerror("Error", "Solo se permiten 50 caracteres")
            elif len(contenido3) > 20:
                nuevo_contenido3 = contenido3[:20]
                entry_contraseña.delete(0, tk.END)
                entry_contraseña.insert(0, nuevo_contenido3)
                tk.messagebox.showerror("Error", "Solo se permiten 20 caracteres")
            elif len(contenido4) > 20:
                nuevo_contenido4 = contenido4[:20]
                entry_confirmar_contraseña.delete(0, tk.END)
                entry_confirmar_contraseña.insert(0, nuevo_contenido4)
                tk.messagebox.showerror("Error", "Solo se permiten 20 caracteres")
                
                

        # Obtener la altura de la ventana
        #ventana_height = int(ventana.winfo_height()) #por ahora no se usa para nada esto

        # Crear un canvas para el rectángulo negro a la izquierda
        # canvas_izquierda = tk.Canvas(ventana, bg=BLACK, height=ventana_height)
        # canvas_izquierda.place(relx=0.0, rely=1.0, anchor='sw', relwidth=0.18, relheight=1.0)  # Sticky para que el rectángulo se expanda verticalmente

        # Crear un canvas para la barra azul abajo
        # canvas_abajo = tk.Canvas(ventana, bg=BLUE, width=512, height=32)  # Height es la altura de la barra azul
        # canvas_abajo.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)  # "ew" para que la barra se expanda horizontalmente
        BG2 = tk.Frame(ventana, bg=BG2color,width=512,height=32)
        #BG1 = tk.Frame(ventana, bg=BG1color,width=80,height=256)
        #BG1.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=0.1, relheight=1.0)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)

        etiqueta_derecha = tk.Label(BG2, text="©5to1ra & 5to3ra - 2023", bg=BG2color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        etiqueta_izquierda = tk.Label(BG2, text="", bg=BG2color,font=("Helvetica", 16))
        etiqueta_izquierda.place(relx = 0.0, rely = 0.5, anchor ='w')

        subfix = " > Cuentas > Registro"
        if tipoCuenta==1:
            etiqueta_izquierda.config(text=str("Profesor"+subfix))
        elif tipoCuenta==2:
            etiqueta_izquierda.config(text=str("Preceptor"+subfix))
        elif tipoCuenta==3:
            etiqueta_izquierda.config(text=str("Administrador"+subfix))

        FrameM = tk.Frame(ventana,bg=BGcolor)
        FrameM.place(relx = 0.7, rely = 0.1, anchor ='nw', relwidth=0.3, relheight=0.68)

        # Etiquetas y campos de entrada
        label_titulo = tk.Label(ventana, text="Registrar Cuenta", bg=BGcolor, font=("Helvetica", 20,"bold"))
        
        label_usuario = tk.Label(ventana, text="Nombre de Usuario:", bg=BGcolor, font=("Helvetica", 10))
        entry_usuario = tk.Entry(ventana, font=("Helvetica", 10), width=20)
        entry_usuario.bind("<KeyRelease>", limite)
        
        label_email = tk.Label(ventana, text="Email:", bg=BGcolor, font=("Helvetica", 10))
        
        entry_email = ttk.Entry(ventana, font=("Helvetica", 10), width=20)
        entry_email.bind("<FocusOut>", arroba,)
        entry_email.bind("KeyRelease", limite)

        label_contraseña = tk.Label(ventana, text="Contraseña:", bg=BGcolor, font=("Helvetica", 10))
        entry_contraseña = tk.Entry(ventana, font=("Helvetica", 10), width=20, show="*")
        entry_contraseña.bind("<KeyRelease>", limite)

        label_confirmar_contraseña = tk.Label(ventana, text="Confirmar Contraseña:", bg=BGcolor, font=("Helvetica", 10))
        entry_confirmar_contraseña = tk.Entry(ventana, font=("Helvetica", 10), width=20, show="*")

        tipos = [(1,"Maestro"),(2,"Preceptor"),(3,"Administrador")]
        tipos_combobox = []
        for i in tipos:
            tipos_combobox.append(i[1])

            
        label_tipo = tk.Label(ventana, text="Tipo de cuenta:", bg=BGcolor, font=("Helvetica", 10))
        entry_tipo = ttk.Combobox(ventana, values=tipos_combobox,state="readonly", font=("Helvetica", 10), width=17)
            

        
        Frame1 = tk.Frame(FrameM, bg=BGcolor)
        Frame1.place(relx = 0.0, rely = 0.0, anchor ='nw', relwidth=1.0, relheight=0.25)
        Frame1.columnconfigure((0,1),weight=1)
        Frame1.rowconfigure((1,2,3),weight=1)

        label_materias = tk.Label(Frame1, text="Selecciona las materias\nasignadas a este Maestro:", bg=BGcolor, font=("Helvetica", 10,"bold"))
        label_materias.grid(row=1, column=0, columnspan=2, padx=0, pady=0,sticky="news")

        cursoLabel = tk.Label(Frame1, text="Curso:",font=("arial", 10), bg=BGcolor, width=8)
        cursos = ["1ro","2do","3ro","4to","5to","6to","7mo"]  # Cursos del 1 al 7
        cursoInput = ttk.Combobox(Frame1, values=cursos,state="readonly", width=8)
        cursoLabel.grid(row=2, column=0, columnspan=1, sticky="nw")
        cursoInput.grid(row=3, column=0, columnspan=1, sticky="nw")

        divisionLabel = tk.Label(Frame1, text="Division:",font=("arial", 10), bg=BGcolor, width=8)
        divisiones = ["A", "B", "C", "D", "E"]  # Divisiones
        divisionInput = ttk.Combobox(Frame1, values=divisiones,state="readonly", width=8)
        divisionLabel.grid(row=2, column=1, columnspan=1, sticky="ne")
        divisionInput.grid(row=3, column=1, columnspan=1, sticky="ne")


        
        Frame2 = tk.Frame(FrameM,highlightthickness=1,highlightbackground="gray")

        Canvas1 = tk.Canvas(Frame2,background="gray94",highlightthickness=0)

        ScrollBar = ttk.Scrollbar(Frame2, orient="vertical")
        Canvas1.configure(yscrollcommand=ScrollBar.set)
        Frame3 = tk.Frame(Canvas1)
        Frame3.pack()

        

        Frame3.bind("<Configure>",lambda e: Canvas1.configure(scrollregion=Canvas1.bbox("all")))
        Canvas1.create_window((0, 0), window=Frame3, anchor="nw")
        

        Frame2.place(relx = 0.0, rely = 0.25, anchor ='nw', relwidth=1.0, relheight=0.75)
        Canvas1.place(relx = 0.0, rely = 0.0, anchor ='nw', relwidth=1.0, relheight=1.0)
        
        seleccionM = []
        print(valores)
        if valores[0]==True and valores[5]=="Maestro" and valores[7] is not None:
            listaM = list(valores[7].split(";"))
            for materia in listaM:
                materia = tuple(materia.split(","))
                seleccionM.append(materia)
        print(seleccionM)

            
        def CambioTipoCuenta(forzar=False):
            if entry_tipo.current()==0 and forzar is not True: #rehabilitar seleccion de materias si tipo es maestro
                divisionInput.config(state='normal')
                cursoInput.config(state='normal')
                divisionInput.current(0)
                cursoInput.current(0)
                Canvas1.create_window((0, 0), window=Frame3, anchor="nw")
                Canvas1.config(background="gray94")
                actualizarMaterias() #actualizar materias para volver a generar lista

                
            else: #deshabilitar seleccion de materias si tipo no es maestro
                divisionInput.config(state='disabled')
                cursoInput.config(state='disabled')
                divisionInput.current(0)
                cursoInput.current(0)
                Canvas1.config(background="lightgray")
                actualizarMaterias() #actualizar materias pero borrar lista justo despues
                for elemento in Frame3.winfo_children():
                    elemento.pack_forget()
                Canvas1.delete("all")
                
                

        def on_course_selected():
            selected_course = cursoInput.get()
            if selected_course in ["2do", "3ro"]:
                divisiones = ["A", "B", "C", "D"]
                divisionInput.config(values=divisiones)
            elif selected_course == "4to":
                divisiones = ["1ra", "2da", "3ra", "4ta", "5ta", "6ta"]
                divisionInput.config(values=divisiones)
            elif selected_course in ["5to", "6to"]:
                divisiones = ["1ra", "2da", "3ra", "4ta", "5ta"]
                divisionInput.config(values=divisiones)
            elif selected_course == "7mo":
                divisiones = ["1ra", "3ra", "4ta"]
                divisionInput.config(values=divisiones)
            else:
                divisiones = ["A", "B", "C", "D", "E"]
                divisionInput.config(values=divisiones)
            
            divisionInput.current(0)
            actualizarMaterias()

        def accionMaterias(var,boton,materia,curso,division):
            print(str(var.get()))
            print(materia,curso,division)
            seleccion=(materia,str(curso+"_"+division))
            if var.get() is True:
                if not seleccion in seleccionM:
                    seleccionM.append(seleccion)
            else:
                try:
                    seleccionM.remove(seleccion)
                except:
                    pass
            
            print(seleccionM)
        

        
        def actualizarMaterias():
            curso=cursoInput.get()
            division=divisionInput.get()
            self.conectar_mysql()
            self.cursor.execute(f"SELECT MATERIA FROM materias WHERE CURSOS LIKE '%{curso}_{division}%' ")
            
            listaMaterias = self.cursor.fetchall()
            self.cerrar_mysql()
            for elemento in Frame3.winfo_children(): #borra lista de materias anterior
                elemento.destroy()
                
            for i in range(0,len(listaMaterias)):
                listaMaterias[i] = str(listaMaterias[i][0])
                listaMaterias[i] = listaMaterias[i].replace("_"," ") #.split(";")
                materia = listaMaterias[i].replace(" ","_")
                if (materia,str(curso+"_"+division)) in seleccionM:
                    var = tk.BooleanVar(value=True)
                else:
                    var = tk.BooleanVar(value=False)

                boton = tk.Checkbutton(Frame3, text=listaMaterias[i], variable=var)
                boton.config(command=lambda A=var, B=boton, C=materia, D=curso, E=division: accionMaterias(A,B,C,D,E))
                boton.pack(anchor="w")

            Canvas1.update()
            if entry_tipo.current()==0:
                heightElementos = Canvas1.bbox("all")
                print(heightElementos[3])
                heightCanvas = Canvas1.winfo_height()
                print(heightCanvas)

                if heightElementos[3] > heightCanvas:
                    print("agregar Scrollbar")
                    ScrollBar.pack(side="right", fill="y")
                    ScrollBar.config(command=Canvas1.yview)
                    Canvas1.bind_all("<MouseWheel>", lambda e: Canvas1.yview_scroll(-1 * (e.delta // 120), "units"))
                else:
                    print("remover Scrollbar")
                    ScrollBar.pack_forget()
                    ScrollBar.config(command=None)
                    Canvas1.unbind_all("<MouseWheel>")
            else:
                print("no es maestro")
                ScrollBar.pack_forget()
                ScrollBar.config(command=None)
                Canvas1.unbind_all("<MouseWheel>") 

        
        cursoInput.bind("<<ComboboxSelected>>", lambda event: on_course_selected())
        divisionInput.bind("<<ComboboxSelected>>", lambda event: actualizarMaterias())
        entry_tipo.bind("<<ComboboxSelected>>", lambda event: CambioTipoCuenta())
        cursoInput.current(0)
        entry_tipo.current(0)

        on_course_selected()
        if valores[0] is True and valores[5]!="Maestro":
            CambioTipoCuenta(True)

        if valores[0]==True:
            label_titulo.config(text="Editar Cuenta")
            entry_usuario.insert(0,valores[2])
            entry_email.insert(0,valores[3])
            entry_contraseña.insert(0,valores[4])
            entry_confirmar_contraseña.insert(0,valores[4])
            entry_tipo.current(tipos_combobox.index(valores[5]))
            if valores[1]==True:
                entry_contraseña.config(state="disabled", show="*")
                entry_confirmar_contraseña.config(state="disabled", show="*")

        # Botón de registro
        boton_registrar = tk.Button(ventana, text="Registrar", command=registrar, bg=BG2color,
                                    width=16, height=1, font=("Helvetica", 10))
        boton_volver = tk.Button(ventana, text="Volver", command=volver, bg=BG2color,
                                    width=16, height=1, font=("Helvetica", 10))

        # Etiqueta para mostrar mensajes de error
        mensaje_error = tk.Label(ventana, text="\n", bg=BGcolor, fg="red", font=("Helvetica", 12))  # Cambia el tamaño de la fuente aquí

        # Organizar elementos en una cuadrícula
        label_titulo.grid(row=0, column=3, columnspan=2, padx=10, pady=10)
        
        label_usuario.grid(row=1, column=3, padx=0, pady=10,sticky="e")
        entry_usuario.grid(row=1, column=4, padx=0, pady=10,sticky="w")

        label_email.grid(row=2, column=3, padx=0, pady=10,sticky="e")
        entry_email.grid(row=2, column=4, padx=0, pady=10,sticky="w")

        label_contraseña.grid(row=3, column=3, padx=0, pady=10,sticky="e")
        entry_contraseña.grid(row=3, column=4, padx=0, pady=10,sticky="w")

        label_confirmar_contraseña.grid(row=4, column=3, padx=0, pady=10,sticky="e")  # Moviendo a la columna 7 (a la derecha)
        entry_confirmar_contraseña.grid(row=4, column=4, padx=0, pady=10,sticky="w")  # Moviendo a la columna 8 (a la derecha)


        label_tipo.grid(row=5, column=3, padx=0, pady=10,sticky="e")
        entry_tipo.grid(row=5, column=4, padx=0, pady=10,sticky="w")

        boton_registrar.grid(row=6, column=3, columnspan=1, padx=(0,0),sticky="")  # Moviendo a la columna 8 (a la derecha) y ajustando el ancho
        boton_volver.grid(row=6, column=4, columnspan=1, padx=(0,0),sticky="")  # Moviendo a la columna 8 (a la derecha) y ajustando el ancho

        mensaje_error.grid(row=7, column=3, columnspan=2,pady=(0,20))

        

"""
if __name__ == "__main__":
    sql = mysql.connector.connect(user='root',#usuario registrado en el mysql
                                  password='', #contraseña del usuario
                                  host='127.0.0.1', #IP del server mysql (en este caso localhost)
                                  autocommit=True #automaticamente aplicar cambios
                                  #database='pynotas' #Base de datos que se usara
                                  )
    cursor = sql.cursor()

    # Crear una ventana
    ventana = tk.Tk()
    ventana.title("Registro")
    ventana.columnconfigure ((0,1,2,3,4,5,6), weight=1)
    ventana.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
    ventana.columnconfigure (0,minsize=80)

    # Configurar el fondo de la ventana
    ventana.configure(bg=BGcolor)

    # Establecer la resolución de la ventana
    ventana.geometry("712x480")
    
    registrar = registrar1(ventana)
    registrar.crear(ventana,3,"Admin","menuFunc","cuentasFunc")

    # Iniciar el bucle principal de la ventana
    ventana.mainloop()
"""