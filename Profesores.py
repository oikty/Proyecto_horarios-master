import tkinter as tk
import mysql.connector
from tkinter import messagebox
from CompletarAU import AutocompleteEntry
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import re,os,sys
from ttkthemes import ThemedStyle

#Hecho por Javier Correa


def resource_path(relative_path):
      try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
       base_path = sys._MEIPASS
      except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
       base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
      return os.path.join(base_path, relative_path)   
def eliminar(ventana):
    for elemento in ventana.winfo_children():
        elemento.destroy()
        
def botones_docentes(ventana3,menuFunc,tipoCuenta,nombreCuenta):
    global frame_pe,imagen_profesor,imagen_materia_ver,imagen_eliminar,imagen_volver,imagen_materia_añadir,imagen_profesor_añadir,tipodecuenta,nombrecuenta,menufunc,current_color,BG3color
    menufunc=menuFunc
    tipodecuenta=tipoCuenta
    nombrecuenta=nombreCuenta
    ventana3.title("Pantalla de profesores")
    path = resource_path("Imagenes/Colegio_logo.ico")
    ventana3.iconbitmap(path)
    # Configuración de los colores
    BGcolor = "#c9daf8"
    BG1color = "#212121"
    BG2color = "#6D9EEB"
    BG3color = "#1b284f"
    current_color = ventana3.cget("bg")
    new_color = BGcolor if current_color != BG3color else BG3color
    nuevo_color = BG2color if new_color == BGcolor else "black"
    color_label = BGcolor if new_color == BGcolor else BG3color
    
    # Aplicar colores a la ventana y a los widgets
    ventana3.configure(bg=new_color)  # Configurar el color de fondo de la ventana
    style = ttk.Style()
    style.configure("TFrame", background=new_color)

    frame_pe = ttk.Frame(ventana3)
    frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
    frame_pe.columnconfigure(0, weight=1)
    frame_pe.rowconfigure(0, weight=1)
    frame_pe.rowconfigure(1, weight=1)
    frame_pe.rowconfigure(2, weight=1) 
    BG2 = tk.Frame(ventana3, bg=nuevo_color,width=512,height=32)
    BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)

    imagen_profesor_path = resource_path("imagenes/profesor.png")
    imagen_materia_ver_path = resource_path("imagenes/materia_ver.png")
    imagen_volver_path = resource_path("imagenes/volver.png")
    imagen_materia_añadir_path = resource_path("imagenes/agregar_materia.png")
    imagen_profesor_añadir_path = resource_path("imagenes/agregar_profesor.png")
    imagen_eliminar_path = resource_path("imagenes/eliminar.png")



    imagen_profesor = ImageTk.PhotoImage(Image.open(imagen_profesor_path).resize((20, 20)))
    imagen_materia_ver = ImageTk.PhotoImage(Image.open(imagen_materia_ver_path).resize((20, 20)))
    imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))
    imagen_materia_añadir = ImageTk.PhotoImage(Image.open(imagen_materia_añadir_path).resize((20, 20)))
    imagen_profesor_añadir = ImageTk.PhotoImage(Image.open(imagen_profesor_añadir_path).resize((20, 20)))
    imagen_eliminar =ImageTk.PhotoImage(Image.open(imagen_eliminar_path).resize((20, 20), Image.LANCZOS))

    tk.Label(ventana3,text="  Materia y Profesores",bg=color_label,fg="white" if color_label == BG3color else "black",font=("Monaco", 24, "bold")).grid(row=1,column=4,columnspan=2,padx=2,pady=2)
    tk.Button(ventana3, text="Volver",image=imagen_volver,compound="left",height=30 , width=300, command=lambda: volver_al_menu(ventana3,menuFunc,tipoCuenta,nombreCuenta)).grid(row=6, column=4,columnspan=2 ,sticky="s")
    tk.Button(ventana3, text="Ver profesores",image=imagen_profesor,compound="left",borderwidth=1,relief="solid",height=30 , width=300, command=lambda:ver_profes(("Id_profesor","Nombre", "Apellido", "Telefono", "Tipo_documento","Nro_de_documento","CUIL", "Correo","Direccion","Altura","Departamento","Fecha_nacimiento"), ("""SELECT Id_profesor, Nombre, Apellido, Telefono, Tipo_documento,Nro_de_documento,CUIL, Correo,Direccion,Altura,Departamento,Fecha_nacimiento FROM profesores ORDER BY Apellido ASC"""),(ventana3),1)).grid(row=3, column=3,columnspan=2, padx=2, pady=2,sticky="ew")
        

    añadir_profes=tk.Button(ventana3, text="Añadir profesores",image= imagen_profesor_añadir,compound="left",borderwidth=1,relief="solid",height=30 , width=300, command=lambda:agregar_profesores(( "Id_profesor","Nombre", "Apellido", "Telefono", "Tipo_documento","Nro_de_documento","CUIL", "Correo","Direccion","Altura","Departamento","Localidad","Fecha_nacimiento"), ("""SELECT Id_profesor,Nombre, Apellido, Telefono, Tipo_documento,Nro_de_documento,CUIL, Correo,Direccion,Altura,Departamento,Localidad,Fecha_nacimiento FROM profesores ORDER BY Apellido ASC"""),(ventana3)))
    añadir_profes.grid(row=3, column=5,columnspan=2, padx=2, pady=2,sticky="ew")
    tk.Button(ventana3, text="Ver materias",image=imagen_materia_ver,compound="left" ,borderwidth=1,relief="solid",height=30 , width=300,command=lambda:ver_aula(( "Materia","Cursos", "Grupo", "Especialidad"), """SELECT MATERIA, CURSOS, Grupo, Especialidad FROM materias ORDER BY MATERIA ASC"""),).grid(row=2, column=3,columnspan=2, padx=2, pady=2,sticky="ew")
        
    añadir_materia_boton=tk.Button(ventana3, text="Añadir materias",image=imagen_materia_añadir,compound="left",borderwidth=1,relief="solid",height=30 , width=300, command=lambda:agregar_materias(( "Materia","Cursos", "Grupo", "Especialidad"), """SELECT MATERIA, CURSOS, Grupo, Especialidad FROM materias ORDER BY MATERIA ASC""",(ventana3)))
    añadir_materia_boton.grid(row=2, column=5,columnspan=2, padx=2, pady=2,sticky="ew")

    

    if tipodecuenta==1:
        añadir_profes.configure(state="disabled")
        añadir_materia_boton.configure(state="disabled")
    etiqueta_derecha = tk.Label(BG2, text="©6°5 - 2024", bg=nuevo_color,fg="white" if color_label == BG3color else "black",font=("Helvetica", 16))
    etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')
        
   
def capitalize_first_letter(entry_widget):
    # Obtenemos el contenido actual del Entry
    try:
        current_text = entry_widget.get()

        # Capitalizamos la primera letra de cada palabra si el contenido no está vacío
        if current_text:
            capitalized_words = [word.capitalize() for word in current_text.split()]
            capitalized_text = " ".join(capitalized_words)
            entry_widget.delete(0, tk.END)  # Borramos el contenido actual
            entry_widget.insert(0, capitalized_text) 
            return True
    except:
        messagebox.showerror("Error", "No tiene mayuscula el inicio de los nombres")
        return False 

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

def validar_letras_numeros(P):
    
    # Esta función permite solo letras y números
    if all(c.isalpha() or c.isspace() or c.isdigit() for c in P):
        return True
    else:
        messagebox.showerror("Error", "Solo se permiten letras y numeros")
        return False 


def arroba(event):
    contenido = entry_correo.get()
    # Utilizamos una expresión regular para verificar el formato del correo
    if contenido.count('.') > 3 or contenido.count('.') == 0 or contenido.count('@') != 1 or not re.match(r'^[\w-]+@', contenido):
        if len(contenido) >0: #no mostrar error si el email se deja vacio
            
            # Si el correo no cumple con el formato o tiene más de una "@", mostramos un mensaje de error
            tk.messagebox.showerror("Error", "Dirección de correo inválida su correo debe verse asi example@gmail.com")
            entry_correo.delete(0, tk.END)  # Borramos el contenido del Entry
            return False
def limite(event):
    contenido = entry_dni.get()
    contenido2 = entry_telefono2.get()
    contenido3 = entry_correo.get()
    contenido4 = entry_direccion.get()
    contenido5 = entry_Altura.get()
    contenido6 = añadir_nombre.get()   
    contenido7 = añadir_apellido.get()
    contenido8 = entry_CUIL.get()
    contenido9 = añadir_localidad.get()
    
    if len(contenido) > 10:
        # Limitar el contenido a 11 caracteres
        nuevo_contenido = contenido[:10]
        entry_dni.delete(0, tk.END)
        entry_dni.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 10 caracteres")
    elif len(contenido2) > 20:
        nuevo_contenido = contenido[:20]
        entry_telefono2.delete(0, tk.END)
        entry_telefono2.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 20 caracteres")
    elif len(contenido3) > 100:
        nuevo_contenido = contenido[:100]
        entry_correo.delete(0, tk.END)
        entry_correo.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 50 caracteres")
    elif len(contenido4) > 100:
        nuevo_contenido = contenido[:100]
        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 50 caracteres")
    elif len(contenido5) > 6:
        nuevo_contenido = contenido[:6]
        entry_Altura.delete(0, tk.END)
        entry_Altura.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 6 caracteres")
    elif len(contenido6)  > 100:
        nuevo_contenido = contenido[:100]
        añadir_nombre.delete(0, tk.END)
        añadir_nombre.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 30 caracteres")
    elif len(contenido7) > 100:
        nuevo_contenido = contenido[:100]
        añadir_apellido.delete(0, tk.END)
        añadir_apellido.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 30 caracteres")
    elif len(contenido8) > 25:
        nuevo_contenido = contenido[:25]
        entry_CUIL.delete(0, tk.END)
        entry_CUIL.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 25 caracteres")
    elif len(contenido9) > 31:
        nuevo_contenido = contenido[:31]
        añadir_localidad.delete(0, tk.END)
        añadir_localidad.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 31 caracteres")


def guardar_informacion(event):
    obtenerfecha = entry_fecha.get()
    
    # Verifica si la fecha es válida
    if not es_fecha_valida(obtenerfecha):
        messagebox.showerror("Error", "Debe seleccionar una fecha a traves del calendario.")
        entry_fecha.delete(0, tk.END)
        return False

def es_fecha_valida(fecha):
    try:
        datetime.strptime(fecha, "%Y/%m/%d")
        return True
    except ValueError:
        return False   
    
def validar_prefijo(event, entry_widget,ver_Profesores):
        entry_telefono.hide_listbox(ver_Profesores)
        widget_con_enfoque = entry_telefono.focus_get()
        if isinstance(widget_con_enfoque, tk.Listbox):
            return
        entrada = entry_widget.get()
        if not entrada in prefijos:
            if len(entrada) > 0: #no mostrar error si campo se deja vacio
                messagebox.showerror("Error", "Por favor seleccionar la opcion del menu")
                entry_widget.delete(0, tk.END)


def toggle_entry_state():
    if check_var.get() == 0:
        entry_Altura.config(state=tk.NORMAL)  # Habilita el Entry
    else:
        entry_Altura.delete(0, tk.END)
        entry_Altura.config(state=tk.DISABLED)  # Deshabilita el Entry

def entrys(ver_Profesores):
    global añadir_nombre,check_departamento, check_departamento ,añadir_apellido, entry_telefono, entry_dni, entry_fecha, entry_correo, entry_direccion, entry_Altura, boton, check_var, variable4, arriba3, treeview_Profe, spin_piso, piso, departamento, prefijos, entry_telefono2, c_a, Opciones_departamento, entry_CUIL, añadir_localidad
    for x in range(7):
        arriba3.columnconfigure(x, weight=1)
    arriba3.rowconfigure(0, weight=1)
    arriba3.rowconfigure(1, weight=1)
    if  current_color== BG3color:
        style = ThemedStyle(arriba3)
        style.set_theme("black")
    else : 
        style = ThemedStyle(arriba3)
        style.set_theme("xpnative")
    
    ttk.Button(arriba3, text="Volver", image=imagen_volver,compound="left",command=lambda: volver_docentes(ver_Profesores)).grid(row=1, column=7, padx=2, pady=2)
    ttk.Label(arriba3, text="Nombre:").grid(column=0, row=0)
    
    añadir_nombre=ttk.Entry(arriba3)
    añadir_nombre.grid(column=0, row=1)
    añadir_nombre.bind("<FocusOut>", lambda event: capitalize_first_letter(añadir_nombre))
    añadir_nombre.bind("<KeyRelease>", limite)
    añadir_nombre.bind('<Return>', lambda event: procesar_enter(event, añadir_apellido))
    añadir_nombre.focus_set()
    añadir_nombre.config(validate="key",validatecommand=(arriba3.register(validar_letras), "%P"))
    
    ttk.Label(arriba3, text="Apellido").grid(column=1, row=0)
    
    añadir_apellido=ttk.Entry(arriba3)
    añadir_apellido.grid(column=1, row=1,  padx=5, pady=5)
    añadir_apellido.config(validate="key",validatecommand=(arriba3.register(validar_letras), "%P"))
    añadir_apellido.bind("<FocusOut>", lambda event: capitalize_first_letter(añadir_apellido))
    añadir_apellido.bind("<KeyRelease>", limite)
    añadir_apellido.bind("<Up>", lambda event: flecha_arriba(event, añadir_nombre))
    
    
    valor_predeterminado = "+54 9"

# Crea una instancia de StringVar y establece el valor predeterminado
    string_var = tk.StringVar()
    string_var.set(valor_predeterminado)

    # Crea el Entry y enlaza su textvariabl
    ttk.Label(arriba3, text="Codigo de area:").grid(column=2, row=0)
    c_a = tk.Entry(arriba3, textvariable=string_var, state=tk.DISABLED, width=len(valor_predeterminado))
    c_a.grid(column=2, row=1)
    
    ttk.Label(arriba3, text="Prefijos:").grid(column=3, row=0)
    def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)
       
    codigo_prefijos=resource_path('numero_codigo.txt')
    prefijos=[]
    with open(codigo_prefijos, 'r') as archivo:
        for linea in archivo:
            numero = linea.strip()
            prefijos.append(numero)
    entry_telefono = AutocompleteEntry(prefijos,arriba3)
    entry_telefono.bind("<FocusOut>", lambda event: validar_prefijo(event, entry_telefono,ver_Profesores))
    entry_telefono.grid(row=1, column=3)
    
    ttk.Label(arriba3, text="Numero de telefono").grid(column=4, row=0)
    entry_telefono2 = ttk.Entry(arriba3, validate="key")
    entry_telefono2.config(validatecommand=(arriba3.register(validar_numeros), "%P"))
    entry_telefono2.bind("<KeyRelease>", limite)
    entry_telefono2.grid(row=1, column=4)
    
    ttk.Label(arriba3, text="Nro de documento").grid(column=6, row=0)
    
    
    entry_dni = ttk.Entry(arriba3, validate="key")
    entry_dni.config(validatecommand=(arriba3.register(validar_numeros), "%P"))
    entry_dni.bind("<KeyRelease>", limite)
    entry_dni.grid(row=1, column=6)
    

    ttk.Label(arriba3, text="Correo electronico:").grid(column=0, row=3)
    entry_correo = ttk.Entry(arriba3)
    entry_correo.bind("<KeyRelease>", limite)
    entry_correo.bind("<FocusOut>", arroba,)
    entry_correo.grid(row=4, column=0, pady=10)
    
    ttk.Label(arriba3, text="Dirección:").grid(column=1, row=3)
    entry_direccion = ttk.Entry(arriba3)
    entry_direccion.bind("<KeyRelease>", limite)
    entry_direccion.bind("<FocusOut>", lambda event: capitalize_first_letter(entry_direccion))
    entry_direccion.grid(row=4, column=1, pady=10, padx=5)
    
    ttk.Label(arriba3, text="Numero:").grid(column=2, row=3)
    entry_Altura = ttk.Entry(arriba3)
    entry_Altura.bind("<KeyRelease>", limite)
    entry_Altura.config(validate="key", validatecommand=(arriba3.register(validar_numeros), "%P"))
    entry_Altura.grid(row=4, column=2, pady=10)
    check_var = tk.IntVar()
    altura = ttk.Checkbutton(arriba3, text="Sin Numero", variable=check_var, command=toggle_entry_state)
    altura.grid(row=5, column=2, pady=10)
    
    ttk.Label(arriba3, text="Piso(opcional)").grid(column=3, row=3)
    piso = tk.StringVar() 
    spin_piso = ttk.Spinbox(arriba3,textvariable=piso,from_=0,to=100,validate="key", state="readonly")
    spin_piso.grid(row=4, column=3, pady=10)
    spin_piso.config(validate="key", validatecommand=(arriba3.register(validar_letras_numeros), "%P"))
    spin_piso.config(validatecommand=(arriba3.register(validar50), "%P"))
    
    ttk.Label(arriba3, text="Departamento(opcional)").grid(column=4, row=3)
    Opciones_departamento=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    departamento = ttk.Combobox(arriba3, values=Opciones_departamento, state="readonly")

    departamento.grid (row=4, column=4, padx=20)
    ttk.Label(arriba3, text="Fecha de nacimiento:").grid(column=5, row=3)
    today = datetime.now()
    max_date = today - timedelta(days=365 * 18+4)
    check_departamento = tk.IntVar()
    check_departamento_button = ttk.Checkbutton(arriba3, text="Sin departamento", variable=check_departamento,  command=toggle_checkbutton)
    check_departamento_button.grid(row=5, column=4, padx=20)
    # Crea el widget DateEntry con la fecha máxima predefinida
    entry_fecha = DateEntry(arriba3, selectmode="day", year=2000, month=1, day=1,date_pattern="yyyy/mm/dd", mindate=None, maxdate=max_date)
    entry_fecha.grid(row=4, column=5, padx=20)
    entry_fecha.bind("<KeyRelease>", guardar_informacion)
    
    ttk.Label(arriba3, text="Ingrese su CUIL").grid(column=6, row=3)
    
    
    entry_CUIL = ttk.Entry(arriba3, validate="key")
    entry_CUIL.config(validatecommand=(arriba3.register(validar_numeros), "%P"))
    entry_CUIL.bind("<KeyRelease>", limite)
    entry_CUIL.grid(row=4, column=6)
    
    ttk.Label(arriba3, text="Localidad").grid(column=0, row=5)
    
    añadir_localidad=ttk.Entry(arriba3)
    añadir_localidad.grid(column=0, row=6)
    añadir_localidad.bind("<FocusOut>", lambda event: capitalize_first_letter(añadir_nombre))
    añadir_localidad.bind("<KeyRelease>", limite)
    añadir_localidad.bind('<Return>', lambda event: procesar_enter(event, añadir_apellido))
    añadir_localidad.focus_set()
    añadir_localidad.config(validate="key",validatecommand=(arriba3.register(validar_letras), "%P"))
    
    
    
def toggle_checkbutton():
    if check_departamento.get() == 0:
        spin_piso.config(state="readonly")
        departamento.set("")
        spin_piso.set("")
        departamento.config(state="readonly")

    else:    
        spin_piso.config(state=tk.DISABLED)
        spin_piso.set("")
        departamento.set("")
        departamento.config(state=tk.DISABLED)    
   

def agregar_numero():
    global numero
    numero = piso.get()
    if numero != 0:
        spin_piso.set(numero)
def validar50(P):
    global valor
    valor = piso.get()
    if valor:
        numero = int(P)
        if 1 <= numero <= 100:
            return True  
def ver_profes(columnas_aula,query,ver_Profesores,eliminar_b):
    global tree_Profe, treeview_Profe, tree_Profe,frame_pe
    if eliminar_b==1:
        print("anashe")
        eliminar(ver_Profesores)
        frame_pe = ttk.Frame(ver_Profesores)
        frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
        
    ver_Profesores.title("Profesores")
    conectar_base_de_datos()
    cursor = cnx.cursor()
    ttk.Button(frame_pe, text="Volver", image=imagen_volver,compound="left",command=lambda: volver_docentes(ver_Profesores)).grid(row=0, column=0, padx=2, pady=2)
    treeview_Profe=ttk.Labelframe(frame_pe, text="Profesores")
    treeview_Profe.grid(padx=10, pady=10, row=1, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(treeview_Profe)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_Profe = ttk.Treeview(treeview_Profe, yscrollcommand=scrollbar.set, selectmode="extended")
    tree_Profe.pack(expand=True, fill="both")
    tree_Profe.bind("<Double-1>", doble_click)
    scrollbar.config(command=tree_Profe.yview)
    tree_Profe["columns"]=("Id_profesor","Nombre", "Apellido", "Telefono", "Tipo_documento","Nro_de_documento","CUIL", "Correo","Direccion","Altura","Departamento","Localidad","Fecha_nacimiento") 
    tree_Profe.column("#0", width=0, stretch=0)
    tree_Profe.column("Id_profesor", anchor="n", width=1) 
    tree_Profe.column("Nombre", anchor="center", width=50)
    tree_Profe.column("Apellido", anchor="center", width=50)
    tree_Profe.column("Telefono", anchor="center", width=200)
    tree_Profe.column("Tipo_documento", anchor="center", width=50)
    tree_Profe.column("Nro_de_documento", anchor="center", width=30)
    tree_Profe.column("CUIL", anchor="center", width=50)
    tree_Profe.column("Correo", anchor="center", width=50)
    tree_Profe.column("Direccion", anchor="center", width=50)
    tree_Profe.column("Altura", anchor="center", width=10)
    tree_Profe.column("Departamento", anchor="center", width=20)
    tree_Profe.column("Localidad", anchor="center", width=30)
    tree_Profe.column("Fecha_nacimiento", anchor="center", width=20)
    columnas_aula = ("Id_profesor", "Nombre", "Apellido", "Telefono", "Tipo_documento", "Nro_de_documento", "CUIL", "Correo", "Direccion", "Altura","Departamento", "Localidad", "Fecha_nacimiento")
    for columna in columnas_aula:
        tree_Profe.column(columna, anchor="center", width=100)
        tree_Profe.heading(columna, text=columna)
    cursor.execute(query)
    data = cursor.fetchall()
    for index, values in enumerate(data):
        tree_Profe.insert(parent='', index='end', iid=index, values=values)
    tree_Profe.pack()
    treeview_Profe.columnconfigure(0, weight=1)
    treeview_Profe.rowconfigure(1, weight=1)
    frame_pe.columnconfigure(0, weight=1)
    frame_pe.rowconfigure(1, weight=1)
    
def agregar_profesores(columnas_aula,query,ver_Profesores):
    global añadir_nombre, añadir_apellido, entry_telefono,entry_dni,entry_fecha, entry_correo, entry_direccion, entry_Altura, check_var, variable4, arriba3, opciones_documento,tree_Profe, treeview_Profe, tree_Profe,frame_pe, entry_CUIL
    eliminar(ver_Profesores)
    frame_pe = ttk.Frame(ver_Profesores)
    frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
    ver_profes(columnas_aula,query,ver_Profesores,0)
    arriba3 = ttk.LabelFrame(frame_pe, text="Añadir")
    arriba3.grid(row=0, column=0,sticky="nsew")
    ttk.Label(arriba3, text="Tipo de documento:").grid(column=5, row=0)
    variable4 = tk.StringVar(arriba3)
    opciones_documento =  ["DU","DNI","Libreta de enrolamiento", "Libreta civica", "Pasaporte", "Cedula de identidad"]
    division = ttk.OptionMenu(arriba3, variable4, opciones_documento[0], *opciones_documento)
    division.grid(column=5, row=1)
    ttk.Button(arriba3, text="Agregar", command=lambda:  opciones_docentes(3)).grid(column=7, row=0, sticky="nsew")
    tk.Button(arriba3, text="Eliminar",image=imagen_eliminar,compound="left",fg="white",bg="#960000", command=lambda:  opciones_docentes(4)).grid(column=7, row=3, sticky="nsew")
    ttk.Button(arriba3, text="Modificar", command=lambda:  opciones_docentes(7)).grid(column=7, row=4, sticky="nsew")
    entrys(ver_Profesores)
    for x in range(7):
        arriba3.rowconfigure(x, weight=1)
        arriba3.columnconfigure(x, weight=1)
    cerrar_base_de_datos()    



def funcionamiento2():
    messagebox.showinfo("Explicación","Como eliminar una fila: La tabla que aparece abajo es la tabla de profesores, para eliminar un profesor haga click y deje seleccionada la fila que quiera eliminar y luego haga click en el boton eliminar, si no se hace click en alguna fila abra un error.\n"
                        "\nComo eliminar varias filas: Para eliminar varias filas puede usar el comando shift+click manteniendolo apretado y seleccionando varios.\n" 
                        "\nEl boton de volver es para ir a la ventana anterior que seria la de los botones de ver añadir y eliminar")
def explicacion2():
    messagebox.showinfo("Explicación","Lo que se ve en la pantalla es la tabla de datos donde se ve la informacion guardada de cada profesor, para saber su funcionamiento haga click en el boton como funciona")



    
    
      
def letras(P):
    if all(c.isalpha() or c.isspace()or c=="_" for c in P):
        return True
    else:
        messagebox.showerror("Error", "Solo se permiten letras.")
        return False    

    # Obtener los valores actuales de las variables
   

def limite3(event):
    contenido = materia_nombre.get()
    contenido1 = entry_especialidad.get()
    if len(contenido) > 30:
        nuevo_contenido = contenido[:30]
        materia_nombre.delete(0, tk.END)
        materia_nombre.insert(0, nuevo_contenido)
        messagebox.showerror("Error", "Solo se permiten 30 caracteres")
    elif len(contenido1) > 30:
        nuevo_contenido1 = contenido1[:30]
        entry_especialidad.delete(0, tk.END)
        entry_especialidad.insert(0, nuevo_contenido1)
        messagebox.showerror("Error", "Solo se permiten 30 caracteres")
def borrar_entrys():
    añadir_nombre.delete(0, tk.END)
    añadir_apellido.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_Altura.delete(0, tk.END)
    entry_telefono2.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    piso.set("")
    departamento.set("")
    entry_CUIL.delete(0, tk.END)
    añadir_localidad.delete(0, tk.END)
    


def doble_click(event):
    global values
    item = tree_Profe.selection()
    if item:
        values = tree_Profe.item(item, "values")
        añadir_nombre.delete(0, tk.END)
        añadir_nombre.insert(0, values[1])
        añadir_apellido.delete(0, tk.END)
        añadir_apellido.insert(0, values[2])

        # Divide la cadena en código de área, Teléfono1 y Teléfono2
        telefonos = values[3].split()


        if len(telefonos) >= 2:
            telefono1 = telefonos[2]
        else:
            telefono1 = ""

        if len(telefonos) >= 3:
            telefono2 = telefonos[3]
        else:
            telefono2 = ""
        

        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, telefono1)

        entry_telefono2.delete(0, tk.END)
        entry_telefono2.insert(0, telefono2)

        entry_dni.delete(0, tk.END)
        entry_dni.insert(0, values[5])

        variable4.set(values[4])

        entry_correo.delete(0, tk.END)
        entry_correo.insert(0, values[7])

        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, values[8])

        entry_Altura.delete(0, tk.END)
        entry_Altura.insert(0, values[9])
        
        añadir_localidad.delete(0, tk.END)
        añadir_localidad.insert(0, values[11])


        # Obtén el valor del departamento si existe
        if check_departamento.get() == 0:
            departamento_completo = values[10]  # Por ejemplo, "Piso 1-B"
            partes = departamento_completo.split()  # Dividir por espacios
            if len(partes) >= 2:
                numero_piso = partes[1]  # El segundo elemento es el número de piso
                codigo_departamento = partes[2] if len(partes) > 2 else ""  # El tercer elemento es el código de departamento, si existe
            
                # Establecer los valores en los widgets correspondientes
                spin_piso.set(numero_piso)
            
                # Establecer el valor seleccionado en el Combobox
                departamento.set(codigo_departamento)   

        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, values[12])
        
        entry_CUIL.delete(0, tk.END)
        entry_CUIL.insert(0, values[6])
                
def funcionamiento():
    messagebox.showinfo("Explicación","Como modificar: La tabla que aparece abajo es la tabla de profesores, para modificar un profesor haga dobleclick en la fila que quiera modificar y luego haga click en el boton modificar, si no se hace doble click en alguna fila abra un error.\n"
                        "\nCada caja de entrada maneja un limite de caracteres que al soltar el teclado si el limite es superado se borra el contenido extra.\n" 
                        "\nEl boton de volver es para ir a la ventana anterior que seria la de los botones de ver añadir y eliminar")
def explicacion():
    messagebox.showinfo("Explicación","Lo que se ve en la pantalla son 2 sectores una con la seccion donde se ingresan los datos para modificar y otra con la tabla de datos donde se ve la informacion guardada de cada profesor, para saber su funcionamiento haga click en el boton como funciona")

def ventana_curso():
    global curso_checkbuttons,curso_vars 
    def seleccionar_todos_los_primeros():
        for curso in curso_checkbuttons:
            if curso.startswith("1ro"):
                # Obtén el índice de la variable en la lista
                index = curso_checkbuttons.index(curso)
                
                # Establece la variable IntVar en 1 (marcado)
                curso_vars[index].set(1)
    def seleccionar_todos_los_segundos():
        for curso in curso_checkbuttons:
            if curso.startswith("2do"):
                index = curso_checkbuttons.index(curso)
                curso_vars[index].set(1)
    def seleccionar_todos_los_terceros():
        for curso in curso_checkbuttons:
            if curso.startswith("3ro"):
                index = curso_checkbuttons.index(curso)
                curso_vars[index].set(1)
    def seleccionar_todos_los_cuartos():
        for curso in curso_checkbuttons:
            if curso.startswith("4to"):
                index = curso_checkbuttons.index(curso)
                curso_vars[index].set(1)
    def seleccionar_todos_los_quintos():
        for curso in curso_checkbuttons:
            if curso.startswith("5to"):
                index = curso_checkbuttons.index(curso)
                curso_vars[index].set(1)
    def seleccionar_todos_los_sexto():
        for curso in curso_checkbuttons:
            if curso.startswith("6to"):
                index = curso_checkbuttons.index(curso)
                curso_vars[index].set(1)
    def seleccionar_todos_los_septimo():
        for curso in curso_checkbuttons:
            if curso.startswith("7mo"):
                index = curso_checkbuttons.index(curso)
                curso_vars[index].set(1)

            
            
    def ayuda():
        messagebox.showinfo("Ayuda", "Los botones funcionan de tal manera para que los botones marcados con tilde se le agregue la materia a los cursos seleccionados \npor ejemplo si yo selecciono todos los primeros y apreto guardar para primero va a estar registrada la materia escrita anteriormente")
    def guardar():
        
        cursos_primer_al_tercero = ["1ro_a", "1ro_b", "1ro_c", "1ro_d", "1ro_e", "2do_a", "2do_b", "2do_c", "2do_d", "2do_e", "3ro_a", "3ro_b", "3ro_c", "3ro_d"]
        cursos_cuarto_al_septimo = ["4to_1ra", "4to_2da", "4to_3ra", "4to_4ta", "4to_5ta", "4to_6ta", "5to_1ra", "5to_2da", "5to_3ra", "5to_4ta", "5to_5ta", "5to_6ta", "6to_1ra", "6to_2da", "6to_3ra", "6to_4ta", "6to_5ta", "6to_6ta", "7mo_1ra", "7mo_3ra", "7mo_4ta"]

        cursos_primer_al_tercero_seleccionados = [curso_checkbuttons[i] for i, var in enumerate(curso_vars) if var.get() == 1 and curso_checkbuttons[i] in cursos_primer_al_tercero]
        cursos_cuarto_al_septimo_seleccionados = [curso_checkbuttons[i] for i, var in enumerate(curso_vars) if var.get() == 1 and curso_checkbuttons[i] in cursos_cuarto_al_septimo]

        if cursos_primer_al_tercero_seleccionados and cursos_cuarto_al_septimo_seleccionados:
            # Si al menos un curso del primer al tercer año y al menos un curso del cuarto al séptimo año están seleccionados,
            # desactivar los cursos del cuarto al séptimo año
            for j in range(len(curso_vars)):
                if curso_checkbuttons[j] in cursos_cuarto_al_septimo:
                    curso_vars[j].set(0)
            messagebox.showerror("Error", "No puede seleccionar ciclo superior y ciclo básico al mismo tiempo \nDebido a la especialidad")
            return False

        cursos_seleccionados_ver = [curso_checkbuttons[i] for i, var in enumerate(curso_vars) if var.get() == 1]

        if len(cursos_seleccionados_ver) == len(curso_checkbuttons):
            cursos_seleccionados_label.config(text="Todos los cursos seleccionados")
        else:
            cursos_seleccionados_label.config(text=", ".join(cursos_seleccionados_ver))

        cursos_a_desactivar = ["1ro_a", "1ro_b", "1ro_c", "1ro_d", "1ro_e", "2do_a", "2do_b", "2do_c", "2do_d", "2do_e", "3ro_a", "3ro_b", "3ro_c", "3ro_d"]

        if any(curso in cursos_seleccionados_ver for curso in cursos_a_desactivar):
            entry_especialidad.config(state="disabled")
            entry_especialidad.set("")
        else:
            entry_especialidad.config(state="readonly")
                

    curso_vars = []  # Lista para almacenar las variables IntVar
    
    cursos = tk.Toplevel()
    
    curso_checkbuttons = ["1ro_a", "1ro_b", "1ro_c","1ro_d","1ro_e","2do_a","2do_b","2do_c","2do_d","2do_e","3ro_a","3ro_b","3ro_c","3ro_d","4to_1ra","4to_2da","4to_3ra","4to_4ta","4to_5ta","4to_6ta","5to_1ra","5to_2da","5to_3ra","5to_4ta","5to_5ta","5to_6ta","6to_1ra","6to_2da","6to_3ra","6to_4ta","6to_5ta","6to_6ta","7mo_1ra","7mo_3ra","7mo_4ta"]
    
    column = 0  # Inicialmente, comenzamos en la columna 0
    row = 0  # Inicializamos el contador de fila
    
    for curso in curso_checkbuttons:
        primero = tk.IntVar()
        checkbutton = ttk.Checkbutton(cursos, text=curso, variable=primero)
        checkbutton.grid(row=row, column=column,padx=25, pady=8)
        curso_vars.append(primero)
        
        row += 1  # Incrementamos el contador de fila
        
        if row >= 10:
            row = 0  # Reiniciamos el contador de fila a 0
            column += 1  # Cambiamos a la siguiente columna
    
    guardar=ttk.Button(cursos, text="Guardar", command=guardar)
    guardar.grid(column=4, row=0)
    seleccionar_primero=ttk.Button(cursos, text="Seleccionar todos los primeros", command=seleccionar_todos_los_primeros)
    seleccionar_primero.grid(column=4, row=1)
    seleccionar_segundo=ttk.Button(cursos, text="Seleccionar todos los segundos", command=seleccionar_todos_los_segundos)
    seleccionar_segundo.grid(column=4, row=2)
    seleccionar_tercero=ttk.Button(cursos, text="Seleccionar todos los terceros", command=seleccionar_todos_los_terceros)
    seleccionar_tercero.grid(column=4, row=3)
    seleccionar_cuarto = ttk.Button(cursos, text="seleccionar todos los cuartos", command=seleccionar_todos_los_cuartos)
    seleccionar_cuarto.grid(column=4, row=4)
    seleccionar_quintos = ttk.Button(cursos, text="seleccionar todos los quintos", command=seleccionar_todos_los_quintos)
    seleccionar_quintos.grid(column=4, row=5)
    seleccionar_sexto = ttk.Button(cursos, text="seleccionar todos los sexto", command=seleccionar_todos_los_sexto)
    seleccionar_sexto.grid(column=4, row=6)
    seleccionar_septimo = ttk.Button(cursos, text="seleccionar todos los septimo", command=seleccionar_todos_los_septimo)
    seleccionar_septimo.grid(column=4, row=7)
    ayuda = ttk.Button(cursos, text="Ayuda", command=ayuda)
    ayuda.grid(column=4, row=9)
    
    
    
    
    
      
def agregar_materias(columnas_aula,query,ver_Materias):
    global materia_nombre,entry_especialidad,cursos_seleccionados_label, tree_materias, año, division, variable2,variable1,opciones_division1, variable3, opciones_año, opciones_division, opciones_division2, opciones_divisionci
    eliminar(ver_Materias)
    
    frame_pe = ttk.Frame(ver_Materias)
    frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
    ver_Materias.title("Materias")
    conectar_base_de_datos()

    if  current_color== BG3color:
        style = ThemedStyle(frame_pe)
        style.set_theme("black")
    else : 
        style = ThemedStyle(frame_pe)
        style.set_theme("xpnative")

    style_labelframe=ttk.Style()
    style_labelframe.configure(".TLabelframe", background="#c9daf8")
    treeview_Materias=ttk.Labelframe(frame_pe, text="Materias",style=".TLabelframe")
    treeview_Materias.grid(padx=10, pady=10, row=1, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(treeview_Materias)
    scrollbar.pack(side="right", fill="y")
    tree_materias = ttk.Treeview(treeview_Materias, yscrollcommand=scrollbar.set, selectmode="extended")
    tree_materias.pack(expand=True, fill="both")
    scrollbar.config(command=tree_materias.yview)
    
    tree_materias["columns"]=(columnas_aula)
    tree_materias.column("#0", width=0,)
    for columna in columnas_aula:
        tree_materias.column(columna, anchor="center")
        tree_materias.heading(columna, text=columna)
    cursor.execute(query)
    data = cursor.fetchall()
    for index, values in enumerate(data):
        tree_materias.insert(parent='', index='end', iid=index, values=values)
    tree_materias.pack()
    
    arriba5 = ttk.LabelFrame(frame_pe, text="Añadir")
    arriba5.grid(padx=10, pady=10, row=0, column=0, sticky="nsew")
    ttk.Button(arriba5, text="Volver",image=imagen_volver,compound="left",width=37, command=lambda: volver_docentes(ver_Materias)).grid(row=2, column=4, padx=2, pady=2)
    ttk.Button(arriba5, text="Agregar",width=41, command=lambda: opciones_docentes(5)).grid(row=1, column=4, padx=2, pady=2)
    tk.Button(arriba5, text="Eliminar",image=imagen_eliminar,compound="left",width=247,height=30,fg="white",bg="#960000", command=lambda:  opciones_docentes(6)).grid(column=4, row=3)
    ttk.Label(arriba5, text="Nombre de la materia:").grid(column=0, row=0, sticky="nsew")
    opciones_division=[]
    materia_nombre=ttk.Entry(arriba5)
    materia_nombre.config(validate="key", validatecommand=(arriba5.register(letras), "%P"))
    materia_nombre.bind("<FocusOut>", lambda event: capitalize_first_letter(materia_nombre))
    materia_nombre.grid(column=0, row=0, sticky="nsew")
    materia_nombre.bind("<KeyRelease>", limite3)
    materia_nombre.focus_set()
    
    ttk.Label(arriba5, text="Año:").grid(column=1, row=0, sticky="nsew")
    
    año = ttk.Button(arriba5,text="Seleccionar cursos de la materia", command=ventana_curso)
    año.grid(column=1, row=1)
    cursos_seleccionados_label = tk.Label(arriba5, text="", wraplength=200)
    cursos_seleccionados_label.grid(row=2, column=1)
    
    
    ttk.Label(arriba5, text="Grupo:").grid(column=3, row=0, sticky="nsew")
    variable3 = tk.StringVar(arriba5)
    opciones_grupo =  ["Ambos","A", "B", "C", "D", "E", "F", "G"]
    grupo = ttk.OptionMenu(arriba5, variable3, opciones_grupo[0], *opciones_grupo)
    grupo.grid(column=3, row=1, sticky="nsew")
    
    lista_especialidad=["Programacion", "Maestro mayor de obras", "Informatica"]

    entry_especialidad = ttk.Combobox(arriba5, values=lista_especialidad, state="readonly")
    entry_especialidad.grid(column=0, row=3, padx=5, pady=5)
    entry_especialidad.set("Programacion")
        
    
    treeview_Materias.columnconfigure(0, weight=1)
    treeview_Materias.rowconfigure(1, weight=1)
    frame_pe.columnconfigure(0, weight=1)
    frame_pe.rowconfigure(1, weight=1)
    arriba5.rowconfigure((0,1), weight=1)
    arriba5.columnconfigure((0,1,2,3,4), weight=1)
def doble_click2(event):
    global values
    item = tree_materias.selection()
    if item:
        values = tree_Profe.item(item, "values")
        materia_nombre.delete(0, tk.END)
        materia_nombre.insert(0, values[1])
        variable1.set(values[2])
        variable2.set(values[3])
        variable3.set(values[4])
def actualizar_division(*args):
    global opciones_division
    año_seleccionado = variable1.get()
    variable2.set("")
    if año_seleccionado <= 3:
        opciones_division = opciones_division1
    else:
        opciones_division = opciones_division2
    # Actualiza el menú desplegable de división con las nuevas opciones
    menu_division = division["menu"]
    menu_division.delete(0, "end")
    for opcion in opciones_division:
        menu_division.add_command(label=opcion, command=lambda value=opcion: variable2.set(value))  
    cerrar_base_de_datos()
    
def reemplazar_espacios(event):
    texto = materia_nombre.get()
    texto_modificado = texto.replace(' ', '_')
    materia_nombre.delete(0, tk.END)  # Borra el contenido actual
    materia_nombre.insert(0, texto_modificado)
    


def opciones_docentes(option):
    conectar_base_de_datos()
    if option==3:
        codigo_area = c_a.get()
        telefono1 = entry_telefono.get()
        telefono2 = entry_telefono2.get()

        # Limpia los valores de los teléfonos de espacios y caracteres no deseados
        codigo_area = codigo_area.strip()
        telefono1 = telefono1.strip()
        telefono2 = telefono2.strip()
        
        obtenernombre=añadir_nombre.get()
        obtenerapellido=añadir_apellido.get()
        obtenertelefono= f"{codigo_area} {telefono1} {telefono2}"
        obtenerdni=entry_dni.get()
        obtenertipodni = variable4.get()
        obtenercorreo=entry_correo.get()
        obtenerdireccion=entry_direccion.get()
        obteneraltura=entry_Altura.get()
        obtenerfecha=entry_fecha.get()
        obtenerdpto=f"Piso {piso.get()}" + " " + departamento.get()
        obtenercuil=entry_CUIL.get()
        obtenerlocalidad=añadir_localidad.get()

        
        
    
        if check_var.get() == 1:
            if not obtenernombre or not obtenerapellido or not obtenertelefono or not obtenerdni or not obtenercorreo or not obtenerdireccion or not obtenerfecha  or not obtenertipodni or not obtenercuil or not obtenerlocalidad:
                messagebox.showerror("Error", "Debe ingresar todos los datos.")
                return False
        else:
            if not obtenernombre or not obtenerapellido or not obtenertelefono or not obtenerdni or not obtenercorreo or not obtenerdireccion or not obteneraltura or not  obtenerfecha or not obtenertipodni or not obtenercuil or not obtenerlocalidad:
                messagebox.showerror("Error", "Debe ingresar todos los datos.")
                return False
        
        select_query = "SELECT * FROM profesores WHERE Nombre = %s AND Apellido = %s AND Telefono= %s AND Tipo_documento = %s AND Nro_de_documento = %s AND CUIL = %s AND Correo = %s AND Direccion = %s AND Altura = %s AND Departamento = %s AND Localidad = %s AND Fecha_nacimiento = %s"
        data_verificar = (obtenernombre,obtenerapellido,obtenertelefono,obtenertipodni,obtenerdni,obtenercuil,obtenercorreo,obtenerdireccion,obteneraltura,obtenerdpto,obtenerlocalidad,obtenerfecha)
                
        cursor = cnx.cursor()
        cursor.execute(select_query, data_verificar)
        existing_row = cursor.fetchone()
            
        if existing_row:
            messagebox.showerror("Error", "La fila ya existe en la base de datos.")
            return     
                
                # Crear la sentencia SQL de inserción
        insert_query = "INSERT INTO profesores (Nombre, Apellido, Telefono, Tipo_documento,Nro_de_documento,CUIL, Correo, Direccion,Altura, Departamento,Localidad, Fecha_nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        dataagregar = (obtenernombre, obtenerapellido, obtenertelefono,obtenertipodni, obtenerdni, obtenercuil, obtenercorreo, obtenerdireccion,obteneraltura, obtenerdpto, obtenerlocalidad, obtenerfecha)  
        agregar_numero()        
        cursor = cnx.cursor()
        
        cursor.execute(insert_query, dataagregar)
        cnx.commit() # Importante: Confirmar los cambios en la base de datos
        last_id = cursor.lastrowid
        messagebox.showinfo("Aviso", "Profesor agregado correctamente")
        tree_Profe.insert(parent='', index='end', values=(last_id,obtenernombre, obtenerapellido, obtenertelefono, obtenertipodni, obtenerdni, obtenercuil, obtenercorreo, obtenerdireccion, obteneraltura, obtenerdpto, obtenerlocalidad, obtenerfecha)) 
        borrar_entrys()
        division.set(opciones_documento[0])
        cerrar_base_de_datos()
    elif option == 4:
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar estos datos?")
        if respuesta:
            conectar_base_de_datos()
            eleccion = tree_Profe.selection()
            if not eleccion:
                messagebox.showerror("Error", "Seleccione al menos un aula")
            else:
                try:
                    cursor = cnx.cursor()
                    for ele in eleccion:
                        profes_id = tree_Profe.item(ele, "values")[0]
                        cursor.execute("DELETE FROM profesores WHERE Id_profesor = %s",(profes_id,))
                        tree_Profe.delete(ele)
                    cnx.commit()
                    cursor.close()
                    if len(eleccion) == 1:
                        messagebox.showinfo("Profesor", "Profesor eliminado")
                    else:
                        messagebox.showinfo("Profesores", f"{len(eleccion)} profesores eliminados exitosamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error al eliminar: {str(e)}")
                finally:
                    cerrar_base_de_datos()
    elif option == 5:
        conectar_base_de_datos()
        obtenernombre=materia_nombre.get()
        obtenergrupo = variable3.get()
        obtenerespecialidad = entry_especialidad.get()
        
        cursos_seleccionados = []

        for i, var in enumerate(curso_vars):
            if var.get() == 1:
                cursos_seleccionados.append(curso_checkbuttons[i])
        
        cursos_seleccionados_str = ';'.join(cursos_seleccionados)

            
            
        print("Valor de obtenerespecialidad:", obtenerespecialidad)
        if not obtenernombre or not cursos_seleccionados_str:
            messagebox.showerror("Error", "Debe ingresar todos los datos.")
            return False



        
        select_query = "SELECT * FROM materias WHERE MATERIA = %s AND CURSOS = %s AND Grupo = %s AND Especialidad = %s"
        data_verificar = (obtenernombre,cursos_seleccionados_str,obtenergrupo, obtenerespecialidad)
                
        cursor = cnx.cursor()
        cursor.execute(select_query, data_verificar)
        existing_row = cursor.fetchone()
            
        if existing_row:
            messagebox.showerror("Error", "La fila ya existe en la base de datos.")
            return     
                
                # Crear la sentencia SQL de inserción
        insert_query = "INSERT INTO materias (MATERIA, CURSOS, Grupo, Especialidad) VALUES (%s, %s, %s, %s)"
        dataagregar = (obtenernombre,cursos_seleccionados_str,obtenergrupo, obtenerespecialidad)
        cursor = cnx.cursor()
        cursor.execute(insert_query, dataagregar)
        cnx.commit()  # Importante: Confirmar los cambios en la base de datos
        messagebox.showinfo("Aviso", "Materia agregada correctamente\nSe recomienda reiniciar el programa para poder ver los cambios") 
        tree_materias.insert(parent='', index='end', values=(obtenernombre,cursos_seleccionados_str,obtenergrupo,obtenerespecialidad))
        materia_nombre.delete(0, tk.END)
        entry_especialidad.delete(0, tk.END)
        cerrar_base_de_datos()
    elif option == 6:
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar estos datos?")
        if respuesta == True:
            conectar_base_de_datos()
            eleccion = tree_materias.selection()
            if not eleccion:
                messagebox.showerror("Error", "Seleccione al menos una materia")
            else:
                try:
                    cursor = cnx.cursor()
                    for ele in eleccion:
                        obtenernombremateria = tree_materias.item(ele, 'values')[0]
                        cursor.execute("DELETE FROM materias WHERE MATERIA = %s", (obtenernombremateria,))
                        tree_materias.delete(ele)
                    
                    cnx.commit()  # Importante: Confirmar los cambios en la base de datos
                    cursor.close()

                    if len(eleccion) == 1:
                        messagebox.showinfo("Materia", "Materia eliminada")
                    else:
                        messagebox.showinfo("Materias eliminadas", f"{len(eleccion)} materias eliminadas exitosamente")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error al eliminar: {str(e)}")
                finally:
                    cerrar_base_de_datos()
    elif option == 7:
        codigo_area = c_a.get()
        telefono1 = entry_telefono.get()
        telefono2 = entry_telefono2.get()

        # Limpia los valores de los teléfonos de espacios y caracteres no deseados
        codigo_area = codigo_area.strip()
        telefono1 = telefono1.strip()
        telefono2 = telefono2.strip()
        
        obtenernombre=añadir_nombre.get()
        obtenerapellido=añadir_apellido.get()
        obtenertelefono= f"{codigo_area} {telefono1} {telefono2}"
        obtenerdni=entry_dni.get()
        obtenertipodni = variable4.get()
        obtenercorreo=entry_correo.get()
        obtenerdireccion=entry_direccion.get()
        obteneraltura=entry_Altura.get()
        obtenerfecha=entry_fecha.get()
        obtenerdpto=f"Piso {piso.get()}" + " " + departamento.get()
        obtenercuil=entry_CUIL.get()
        obtenerlocalidad=añadir_localidad.get()
       

        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de modificar estos datos?")
        if respuesta == True:
            conectar_base_de_datos()
            eleccion = tree_Profe.selection()
            if check_var.get() == 1:
                if not obtenernombre or not obtenerapellido or not obtenertelefono or not obtenerdni or not obtenercorreo or not obtenerdireccion or not obtenertipodni or not obtenercuil or not obtenerlocalidad:
                    messagebox.showerror("Error", "Debe ingresar todos los datos.")
                    return False
            else:
                if not obtenernombre or not obtenerapellido or not obtenertelefono or not obtenerdni or not obtenercorreo or not obtenerdireccion or not obteneraltura  or not obtenertipodni or not obtenercuil or not obtenerlocalidad:
                    messagebox.showerror("Error", "Debe ingresar todos los datos.")
                    return False
            if not eleccion:
                 messagebox.showerror("Error", "Elija por lo menos una fila de la tabla apretando doble click.")
                 return False
            else:
                try:
            
                    
                    # Verificar si se han realizado cambios
                    if obtenernombre == values[1] and obtenerapellido == values[2] and obtenertelefono == values[3] and obtenerdni == values[5] and obtenertipodni == values[4] and obtenercuil == values[6] and obtenercorreo == values[7] and obtenerdireccion == values[8] and obteneraltura == values[9] and obtenerdpto == values[10] and obtenerlocalidad == values[11] and obtenerfecha == values[12]:
                        messagebox.showerror("Error", "No ha modificado ningún dato.") 
                        return False
                    else:
                        cursor = cnx.cursor()
                        profes_id = tree_Profe.item(eleccion, "values")[0]
                        cursor.execute("UPDATE profesores SET Nombre = %s, Apellido = %s, Telefono = %s, Tipo_documento = %s,Nro_de_documento = %s,CUIL = %s, Correo = %s, Direccion = %s, Altura = %s,Departamento = %s,Localidad = %s, Fecha_nacimiento = %s WHERE Id_profesor = %s",(obtenernombre, obtenerapellido, obtenertelefono, obtenertipodni,obtenerdni, obtenercuil, obtenercorreo, obtenerdireccion,obteneraltura,obtenerdpto,obtenerlocalidad,obtenerfecha ,profes_id))
                        cnx.commit()
                        cursor.close()
                        messagebox.showinfo("Éxito", "Los datos se han actualizado correctamente.")
                        tree_Profe.item(eleccion, values=(profes_id,obtenernombre, obtenerapellido, obtenertelefono, obtenertipodni,obtenerdni,obtenercuil, obtenercorreo, obtenerdireccion,obteneraltura,obtenerdpto,obtenerlocalidad,obtenerfecha))
                except Exception as e:
                    messagebox.showerror("Error", "Se produjo un error al actualizar los datos: " + str(e))
   
def ver_aula(columnas_aula,query):
    ver_aula = tk.Toplevel()
    conectar_base_de_datos()
    scrollbar = ttk.Scrollbar(ver_aula)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_aula = ttk.Treeview(ver_aula, yscrollcommand=scrollbar.set, selectmode="extended")
    tree_aula.pack(expand=True, fill="both")
    scrollbar.config(command=tree_aula.yview)
    
    tree_aula["columns"]=(columnas_aula)
    tree_aula.column("#0", width=0, stretch=tk.NO)
    for columna in columnas_aula:
        tree_aula.column(columna, anchor=tk.CENTER)
        tree_aula.heading(columna, text=columna)
        
    cursor.execute(query)
    data = cursor.fetchall()
    for index, values in enumerate(data):
        tree_aula.insert(parent='', index='end', iid=index, values=values)
    tree_aula.pack()
    cerrar_base_de_datos()
def conectar_base_de_datos():
    global cursor
    global cnx
    cnx = mysql.connector.connect(
            host='eestn1.com.ar',
            user='tecnica1',
            password='z%51#q57A7BR',
            database='tec_boletines2023',
            port=3306
    )
    # Crear un cursor para ejecutar consultas
    cursor = cnx.cursor()
def cerrar_base_de_datos():
    cursor.close()
    cnx.close()    
    
def volver_al_menu(ventana,menuFunc,tipoCuenta,nombreCuenta):
    print("volver")
    for elemento in ventana.winfo_children():
        elemento.destroy()
    menuFunc(tipoCuenta,nombreCuenta)
def volver_docentes(ventana):
    eliminar(ventana)
    botones_docentes(ventana,menufunc,tipodecuenta,nombrecuenta)
def flecha_arriba(event, anterior_entry): 
    anterior_entry.focus_set()
def procesar_enter(event, next_entry):
    next_entry.focus_set()


if __name__ == "__main__":
    ventana = tk.Tk()
    botones_docentes(ventana)
    ventana.mainloop()
