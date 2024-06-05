#pip install mysql-connector-python
#pip install tkcalendar

#CREATE USER 'pipo'@'localhost' IDENTIFIED BY '1243';
#GRANT ALL PRIVILEGES ON *.* TO 'pipo'@'localhost'; 

try:
    from tkinter import *
    import tkinter as tk
    from tkinter import ttk
    from tkcalendar import Calendar
    from tkinter import messagebox
    import mysql.connector
    from datetime import datetime
    from CompletarAU import AutocompleteEntry
    import os,sys
except ImportError as e:
    print("No se encuentran librerías necesarias:", e)
    exit()

BGcolor="#c9daf8"
BG1color="#212121"
BG2color="#6D9EEB"

class ingreso1():
    def text_file_path(relative_path):
     """Obtener la ruta absoluta de un archivo de texto."""
     try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
     except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
        base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del archivo de texto para obtener la ruta absoluta
     return os.path.join(base_path, relative_path)
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
        
    def __init__(self,tk):
    
        try:
            self.conectar_mysql()#crea el procedimiento para actualizar el curso de un alumno en todas las tablas de materias
            self.cursor.execute("""
            
            DELIMITER //

            CREATE PROCEDURE actualizarCurso(
                IN table_name VARCHAR(255),
                IN curso VARCHAR(255),
                IN ID VARCHAR(255)
            )
            BEGIN
                SET @query_update = CONCAT(
                    "UPDATE ", table_name,
                    " SET CURSO = '", curso, "'",
                    " WHERE ID = ", ID
                );

                -- Prepare and execute the dynamic SQL statement
                PREPARE stmt FROM @query_update;
                EXECUTE stmt;

                -- Check if any rows were affected by the update
                IF ROW_COUNT() = 0 THEN
                    -- No rows were updated, so insert a new row
                    SET @query_insert = CONCAT("INSERT IGNORE INTO ", table_name,"(ID,CURSO)
                                            VALUES ('",ID,"','",curso,"')");
                    
                    -- Prepare and execute the dynamic insert SQL statement
                    PREPARE insert_stmt FROM @query_insert;
                    EXECUTE insert_stmt;
                END IF;

                -- Deallocate prepared statements
                DEALLOCATE PREPARE stmt;
                DEALLOCATE PREPARE insert_stmt;
            END;
            //

            DELIMITER ;
            """)
            self.cerrar_mysql()
        except:
            pass

    def crear(self,tk,tipoCuenta,nombreCuenta,menuFunc,alumnosFunc,valores=[False]):

        def eliminar():
            for elemento in tk.winfo_children():
                elemento.destroy()
        def volver():
            eliminar()
            alumnosFunc(tk,tipoCuenta,nombreCuenta,menuFunc,alumnosFunc)
            return

        def validar_telefono(tel):
           return tel.startswith('11') and tel.isdigit() and len(tel) ==10

        def cargar():
            self.cursor.reset()
            Cnombre = NombreInput.get().strip()
            Capellido = ApellidoInput.get().strip()
            Icurso = cursoInput.get()
            Ifecha = FechaInput.get().strip()
            Sfechas = Ifecha.replace('/','.').replace('-','.')
            Lfechas = Sfechas.split('.')

            ErrorLabel.config(text = "", bg=BGcolor)
            
            Ccurso = str(Icurso)
            Cdivision = divisionInput.get()
            Cgrupo = grupoInput.get()
            Ctelefono = TELEInput.get()

            # --CHECKEO CAMPOS VACIOS--
            if Cnombre == '' or Capellido == '':
                ErrorLabel.config(text = "Ingrese un Nombre y Apellido válidos.", bg=BGcolor)
                tk.bell()
                return
            
            
            try:
                if Ifecha==Fechadefault:
                    raise ValueError
                Cfecha = datetime(int(Lfechas[0]), int(Lfechas[1]), int(Lfechas[2]))
            except ValueError:
                ErrorLabel.config(text = "Ingrese una Fecha de Nacimiento Válida.", bg=BGcolor)
                tk.bell()
                return
            

            SQLcurso = str(Ccurso+"_"+Cdivision).lower()
            print(SQLcurso)
            
           
            
            Cdni = DNIInput.get()
            Cdni = Cdni.replace(".", "")
            self.conectar_mysql()
            self.cursor.execute("SELECT CURSO FROM cursos")
            fetchCursos=self.cursor.fetchall()
            self.cerrar_mysql()
            
            if Cdni != DNIdefault and Cdni.isdigit() is True and len(Cdni) < 8:
                ErrorLabel.config(text = "Ingrese un DNI válido (8 números).", bg=BGcolor)
                tk.bell()
            else:
                for curso in fetchCursos:
                    self.cursor.reset()
                    self.conectar_mysql()
                    self.cursor.execute(f"SELECT CURSO FROM alumnos WHERE nro_de_documento = '{Cdni}'")
                    
                    fetchDNI=self.cursor.fetchone()
                    self.cerrar_mysql()
                    
                    if (fetchDNI is not None) and (valores[0] is False):
                        #fetchDNI = fetchDNI.split("_")
                        #fetchDNI[1] = fetchDNI[1].upper()
                        #fetchDNI
                        ErrorLabel.config(text = f"El Dni ingresado ya se encuentra a nombre de un alumno en {fetchDNI}")
                        tk.bell()
                        Repetido=True
                        
                        break
                        
                    else:
                        Repetido=False

                if Repetido==True:
                    return
                
                #en el caso de que se modifique el curso o division, el mismo tambien debe ser modificado en
                #todas las tablas de materias para evitar que se pierdan las notas del alumno
                def actualizarCurso():
                    print("!! Se cambio el curso o division !!")
                    self.conectar_mysql()
                    #obtener lista de materias del curso
                    self.cursor.execute(f"SELECT MATERIA FROM materias WHERE CURSOS LIKE '%{SQLcurso}%' ")
                    self.cerrar_mysql()
                    materiasFetch = self.cursor.fetchall()
                    for i in materiasFetch:
                        materiasFetch[materiasFetch.index(i)] = str(i[0]).replace(" ","_")
                    print(materiasFetch)


                    queryMaterias=[]
                    Lquery=[]
                    Iquery=[]
                    for materia in materiasFetch:
                        #llama un procedimiento (lo equivalente a funciones en mysql) que automaticamente
                        #inserta o actualiza dependiendo de 
                        Lquery.append(f"CALL actualizarCurso('boletines__{materia}','{SQLcurso}','{valores[9]}')")
                        queryMaterias.append(materia.replace(" ","_"))
                    query = "; ".join(Lquery)


                    print(query)
                    if query is None or query==[] or query=="":
                        print(f"no se encontraron materias en {SQLcurso}, ninguna tabla de boletines modificada")
                        return
                    else:
                        print("se modificaran los boletines de:"+str(queryMaterias))
                    
                    print(Lquery)
                    print(queryMaterias)
                    for resultado in self.cursor.execute(query,multi=True):
                        pass

                        
                
                #Codigo que se encarga de Insertar o Actualizar la base de datos
                self.cursor.reset()
                if valores[0]==True:
                    self.conectar_mysql()
                    self.cursor.execute("UPDATE alumnos SET NOMBRE=%s,APELLIDO=%s,GRUPO=%s,NACIMIENTO=%s,TELEFONO=%s,nro_de_documento=%s,CURSO=%s WHERE ID=%s",(Cnombre, Capellido, Cgrupo, Cfecha, Ctelefono, Cdni, SQLcurso, valores[9]))
                    self.sql.commit()
                    print(f"Alumno {Cnombre} Actualizado Exitosamente")
                    ErrorLabel.config(text = "", bg=BGcolor)
                    if SQLcurso.lower() != str(valores[3]+"_"+valores[4]).lower():
                        actualizarCurso()
                    volver()
                    self.cerrar_mysql()
                    return
                else:
                    self.conectar_mysql
                    self.cursor.execute("INSERT INTO alumnos (NOMBRE,APELLIDO,GRUPO,NACIMIENTO,TELEFONO,nro_de_documento,CURSO) VALUES (%s,%s,%s,%s,%s,%s,%s)",(Cnombre, Capellido, Cgrupo, Cfecha, Ctelefono, Cdni, SQLcurso))
                    self.sql.commit()
                    print(f"Alumno {Cnombre} Cargado Exitosamente")
                    ErrorLabel.config(text = f"Alumno {Cnombre} Cargado Exitosamente", bg=BGcolor)
                    self.cerrar_mysql()
                    return
                
        #def capitalize_first_letter(entry_widget):
        # Obtenemos el contenido actual del Entry
        #        current_text = entry_widget.get()
        #        # Capitalizamos la primera letra de cada palabra si el contenido no está vacío
        #        if current_text:
        #            capitalized_words = [word.capitalize() for word in current_text.split()]
        #            capitalized_text = " ".join(capitalized_words)
        #            entry_widget.delete(0, END)  # Borramos el contenido actual
        #            entry_widget.insert(0, capitalized_text) 
        #            return True
        #        messagebox.showerror("Error", "No tiene mayuscula el inicio de los nombres")
        #        return False 
        def validar_nombres(nombre):
            print("nombre")
            print(type(nombre))
            Lnombre = nombre.get().split(" ")
            print(Lnombre)
            for i in range(0,len(Lnombre)):
                print(i)
                Lnombre[i] = Lnombre[i].capitalize()
                print(Lnombre[i])
            print(Lnombre)
            nombre.set(" ".join(Lnombre))

        def validar_numeros(P):
        # Función de validación para permitir solo caracteres numéricos
            if all(c.isdigit() for c in P):
                return True
            else:
                messagebox.showerror("Error", "Solo se permiten números")
                return False
        def validar_letras(P):
        
            # Esta función permite solo letras y números
            if all(c.isalpha() or c.isspace() for c in P):
                return True
            else:
                messagebox.showerror("Error", "Solo se permiten letras")
                return False 
        def limite(event):
            contenido = NombreInput.get()
            contenido2 = ApellidoInput.get()
            #contenido3 = entry_telefono2.get()
            contenido3 = TELEInput.get()
            contenido4 = DNIInput.get()
            
            if len(contenido) > 30:
                # Limitar el contenido a 11 caracteres
                nuevo_contenido = contenido[:0]
                NombreInput.delete(0, END)
                NombreInput.insert(0, nuevo_contenido)
                messagebox.showerror("Error", "Solo se permiten 30 caracteres")
            elif len(contenido2) > 30:
                # Limitar el contenido a 11 caracteres
                nuevo_contenido2 = contenido2[:0]
                ApellidoInput.delete(0, END)
                ApellidoInput.insert(0, nuevo_contenido2)
                messagebox.showerror("Error", "Solo se permiten 30 caracteres")
            elif len(contenido3) > 11:
                # Limitar el contenido a 11 caracteres
                nuevo_contenido3 = contenido3[:11]
                #entry_telefono2.delete(0, END)
                #entry_telefono2.insert(0, nuevo_contenido3)
                TELEInput.delete(0, END)
                TELEInput.insert(0, nuevo_contenido3)
                messagebox.showerror("Error", "Solo se permiten 11 caracteres")
            elif len(contenido4) > 8: #10:
                # Limitar el contenido a 11 caracteres
                nuevo_contenido4 = contenido4[:8] #[:10]
                DNIInput.delete(0, END)
                DNIInput.insert(0, nuevo_contenido4)
                messagebox.showerror("Error", "Solo se permiten 8 caracteres")
        def validar_prefijo(event, entry_widget,tk):
            #TELEInput.hide_listbox(tk)
            widget_con_enfoque =TELEInput.focus_get()
            if isinstance(widget_con_enfoque, Listbox):
                return
            entrada = entry_widget.get()
            if not entrada in prefijos:
                print(entrada)
                if len(entrada) > 0:
                    messagebox.showerror("Error", "Por favor seleccionar la opcion del menu")
                    entry_widget.delete(0, END)
                    entry_widget.focus()
        BG2 = Frame(tk, bg=BG2color,width=512,height=32)
        BG1 = Frame(tk, bg=BG1color,width=80,height=256)
        BG1.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=0.1, relheight=1.0)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)

        etiqueta_derecha = Label(BG2, text="©5to1ra Grupo A - 2023", bg=BG2color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        etiqueta_izquierda = Label(BG2, text="", bg=BG2color,font=("Helvetica", 16))
        etiqueta_izquierda.place(relx = 0.1, rely = 0.5, anchor ='w')

        subfix = " > Alumnos > Ingreso"
        if tipoCuenta==1:
            etiqueta_izquierda.config(text=str("Profesor"+subfix))
        elif tipoCuenta==2:
            etiqueta_izquierda.config(text=str("Preceptor"+subfix))
        elif tipoCuenta==3:
            etiqueta_izquierda.config(text=str("Administrador"+subfix))


        Titulo = Label(tk, text="Cargar Alumno",font=("arial", 16, "bold"), bg=BGcolor)
        Titulo.place(relx=0.55, rely=0.0, anchor='n')

        global NombreString #trace no parece funcionar si variable no es global
        NombreString = StringVar()
        NombreString.trace_add('write', lambda *args: validar_nombres(NombreString))
        NombreLabel = Label(tk, text="Introduce el Nombre del alumno",font=("arial", 8), bg=BGcolor)
        NombreInput = ttk.Entry(tk, width=25, textvariable=NombreString)
        NombreLabel.place(relx = 0.2, rely = 0.1, anchor ='sw')
        NombreInput.place(relx = 0.2, rely = 0.15, anchor ='sw')
        #NombreInput.bind("<FocusOut>", lambda event: capitalize_first_letter(NombreInput))
        NombreInput.bind("<KeyRelease>", limite)
        NombreInput.config(validate="key",validatecommand=(tk.register(validar_letras), "%P"))

        global ApellidoString #trace no parece funcionar si variable no es global
        ApellidoString = StringVar()
        ApellidoString.trace_add('write', lambda *args: validar_nombres(ApellidoString))
        ApellidoLabel = Label(tk, text="Introduce el Apellido del alumno",font=("arial", 8), bg=BGcolor)
        ApellidoInput = ttk.Entry(tk, width=25, textvariable=ApellidoString)
        ApellidoLabel.place(relx = 0.2, rely = 0.2, anchor ='sw')
        ApellidoInput.place(relx = 0.2, rely = 0.25, anchor ='sw')
        #ApellidoInput.bind("<FocusOut>", lambda event: capitalize_first_letter(ApellidoInput))
        ApellidoInput.bind("<KeyRelease>", limite)
        ApellidoInput.config(validate="key",validatecommand=(tk.register(validar_letras), "%P"))
        

        cursoLabel = Label(tk, text="Seleccione el Curso del Alumno",font=("arial", 8), bg=BGcolor)
        cursos = ["1ro","2do","3ro","4to","5to","6to","7mo"]  # Cursos del 1 al 7
        cursoInput = ttk.Combobox(tk, values=cursos,state="readonly")
        cursoLabel.place(relx = 0.2, rely = 0.3, anchor ='sw')
        cursoInput.place(relx = 0.2, rely = 0.35, anchor ='sw')

        divisionLabel = Label(tk, text="Seleccione la División del Alumno",font=("arial", 8), bg=BGcolor)
        divisiones = ["A", "B", "C", "D", "E"]  # Divisiones
        divisionInput = ttk.Combobox(tk, values=divisiones,state="readonly")
        divisionLabel.place(relx = 0.2, rely = 0.4, anchor ='sw')
        divisionInput.place(relx = 0.2, rely = 0.45, anchor ='sw')
        
        grupoLabel = Label(tk, text="Seleccione el Grupo del Alumno",font=("arial", 8), bg=BGcolor)
        grupoInput = ttk.Combobox(tk,state="readonly")
        grupoLabel.place(relx = 0.2, rely = 0.5, anchor ='sw')
        grupoInput.place(relx = 0.2, rely = 0.55, anchor ='sw')

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
            
            selected_course = cursoInput.get()
            if selected_course in["1ro"]:
                grupos=["Ninguno","A", "B", "C"]
                grupoInput.config(values=grupos)
            else:
                grupos = ["Ninguno","A", "B"]  # Grupos
                grupoInput.config(values=grupos)
            
            divisionInput.current(0)
            grupoInput.current(0)
        
        cursoInput.bind("<<ComboboxSelected>>", lambda event: on_course_selected())
        cursoInput.current(0)

        on_course_selected()

        valor_predeterminado = "+54 9"

    # Crea una instancia de StringVar y establece el valor predeterminado
        string_var = StringVar()
        string_var.set(valor_predeterminado)

        # Crea el Entry y enlaza su textvariabl
        c_a = Entry(tk, textvariable=string_var, state=DISABLED, width=len(valor_predeterminado))
        #c_a.place(relx = 0.2, rely = 0.65, anchor ='sw', relwidth=0.05)
        
        
        global prefijos
        def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)
        prefijos=[]
        codigo_prefijos=resource_path('numero_codigo.txt')
        with open(codigo_prefijos, 'r') as archivo:
            for linea in archivo:
                numero = linea.strip()
                prefijos.append(numero)
        #TELEInput = AutocompleteEntry(prefijos,tk)
        TELEInput = ttk.Entry(tk, validate="key")
        TELEInput.config(width=25)
        #TELEInput.bind("<FocusOut>", lambda event: validar_prefijo(event, TELEInput,tk))
        TELEInput.config(validatecommand=(tk.register(validar_numeros), "%P"))
        TELEInput.bind("<KeyRelease>", limite)
        
        entry_telefono2 = ttk.Entry(tk, validate="key")
        #entry_telefono2.config(validatecommand=(tk.register(validar_numeros), "%P"))
        #entry_telefono2.bind("<KeyRelease>", limite)
        #entry_telefono2.place(relx = 0.32, rely = 0.65, anchor ='sw', relwidth=0.12)
        

        TELELabel = Label(tk, text="Introduzca el Telefono de un Tutor",font=("arial", 8), bg=BGcolor)
        TELELabel.place(relx = 0.2, rely = 0.6, anchor ='sw')
        #TELEInput.place(relx = 0.26, rely = 0.65, anchor ='sw', relwidth=0.05)
        TELEInput.place(relx = 0.2, rely = 0.65, anchor ='sw')

        #ttk.Label(tk, text="Numero de telefono",font=("arial", 8)).place(relx = 0.32, rely = 0.655, anchor ='nw', relwidth=0.15)
        #ttk.Label(tk, text="Codigo de area:",font=("arial", 8)).place(relx = 0.26, rely = 0.655, anchor ='nw', relwidth=0.05)
        #ttk.Label(tk, text="Prefijos:",font=("arial", 8)).place(relx = 0.2, rely = 0.655, anchor ='nw', relwidth=0.05)


        DNILabel = Label(tk, text="Introduce el DNI del Alumno",font=("arial", 8), bg=BGcolor)
        DNIInput = Entry(tk, width=25)
        DNIInput.config(validate="key",validatecommand=(tk.register(validar_numeros), "%P"))
        DNIInput.bind("<KeyRelease>", limite)
        DNILabel.place(relx = 0.66, rely = 0.1, anchor ='sw')
        DNIInput.place(relx = 0.66, rely = 0.15, anchor ='sw')

        opciones_documento =  ["DU","DNI","Libreta de enrolamiento", "Libreta civica", "Pasaporte", "Cedula de identidad"]
        division = ttk.Combobox(tk,  values=opciones_documento, state="readonly")
        #division.place(relx = 0.66, rely = 0.7, anchor ='sw')
        def focus(event, entry, textoDefault):
            event = str(event)
            print(event)
            textoEntry = entry.get()
            print(textoEntry)
            if event=='<<CalendarSelected>>' or event=='<VirtualEvent event x=0 y=0>':
                entry.delete(0,END)
                entry.config(fg="black")
                entry.focus()
                entry.insert(0,FechaCalendario.get_date())
            elif event=='<FocusIn event>' and textoEntry == "" or textoEntry == None or textoEntry == textoDefault:
                entry.delete(0,END)
                entry.config(fg="black")
            elif event=='<FocusOut event>' and textoEntry == "" or textoEntry == None:
                entry.insert(0,textoDefault)
                entry.config(fg="gray")
        

        DNIdefault = "00000000"
        DNIInput.bind('<FocusIn>', lambda ev: focus(ev,DNIInput,DNIdefault))
        DNIInput.bind('<FocusOut>', lambda ev: focus(ev,DNIInput,DNIdefault))

        FechaLabel = Label(tk, text="Introduce la Fecha de Nacimiento del Alumno",font=("arial", 8), bg=BGcolor)
        FechaInput = Entry(tk, width = 25)
        #FechaBoton = Button(tk, text ="Actualizar Fecha", command = lambda: focus('<<CalendarSelected>>',FechaInput,Fechadefault),font=("arial", 7))
        FechaLabel.place(relx = 0.66, rely = 0.2, anchor ='sw')
        FechaInput.place(relx = 0.66, rely = 0.25, anchor ='sw')
        #FechaBoton.place(relx = 0.825, rely = 0.25, anchor ='sw')

        Fechadefault = "2000-01-01"
        FechaInput.bind('<FocusIn>', lambda ev: focus(ev,FechaInput,Fechadefault))
        FechaInput.bind('<FocusOut>', lambda ev: focus(ev,FechaInput,Fechadefault))

        FechaCalendario = Calendar(tk,font=("arial", 7) , selectmode = 'day', date_pattern="yyyy-mm-dd", mindate=datetime(2000,1,1), maxdate=datetime.now())
        FechaCalendario.place(relx = 0.66, rely = 0.255, anchor ='nw')
        FechaCalendario.bind("<<CalendarSelected>>",lambda ev: focus(ev,FechaInput,Fechadefault))

        if valores[0]==True: #si se esta editando un alumno existente
            Titulo.config(text="Editar Alumno")
            #print(tk.winfo_children())
            print(valores)
            NombreInput.insert(0,valores[1])
            ApellidoInput.insert(0,valores[2])

            cursoInput.current(cursos.index(valores[3]))
            on_course_selected()
            divisionInput.current(divisionInput["values"].index(valores[4]))
            grupoInput.current(grupoInput["values"].index(valores[5]))
            TELEInput.insert(0,valores[6])
            DNIInput.insert(0,valores[7])
            FechaCalendario.selection_set(valores[8])
            focus('<<CalendarSelected>>',FechaInput,Fechadefault)
            tk.focus() #deseleccionar todos los widgets (arreglo de un bug)

        else: #si se esta ingresando un alumno nuevo
            cursoInput.current(cursos.index(valores[1]))
            on_course_selected()
            divisionInput.current(divisionInput["values"].index(valores[2]))
        
        focus('<FocusOut event>',DNIInput,DNIdefault)
        focus('<FocusOut event>',FechaInput,Fechadefault)

        ErrorLabel = Label(tk, text="",font=("arial", 8), bg=BGcolor, anchor="center")
        ErrorLabel.place(relx = 0.55, rely = 0.75, anchor ='s')

        CargarBoton = Button(tk, text ="Cargar Alumno", width=12, command = cargar)
        CargarBoton.place(relx = 0.53, rely = 0.85, anchor ='se')

        VolverBoton = Button(tk, text ="Volver", width=12, command = volver)
        VolverBoton.place(relx = 0.57, rely = 0.85, anchor ='sw')