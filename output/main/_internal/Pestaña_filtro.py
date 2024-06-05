import tkinter as tk
import mysql.connector
from CompletarAU import AutocompleteEntry
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
from PDF import PDF_filtro
import os,sys
#Hecho por Tobias Bonanno


     
class menu_filtros():
    
    def __init__(self,ventana_filtro,menuFunc,tipoCuenta,nombreCuenta):
        def resource_path(relative_path):
          try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
           base_path = sys._MEIPASS
          except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
            base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
          return os.path.join(base_path, relative_path)
        self.menuFunc=menuFunc
        self.tipoCuenta=tipoCuenta
        self.nombreCuenta=nombreCuenta
        self.ventana5 = ventana_filtro
        self.ventana5.title("Pantalla Filtros")
        path = resource_path("Imagenes/Colegio_logo.ico")
        self.ventana5.iconbitmap(path)
        BG2color="#c9daf8"
        self.frame_fullscreen = tk.Frame(self.ventana5, bg=BG2color)
        self.frame_fullscreen.place(x=0, y=0, relwidth=1, relheight=1)
        
    

        imagen_filtro_curso_path = resource_path("imagenes/filtro_curso.png")
        imagen_filtro_dia_path = resource_path("imagenes/filtro_dia.png")
        imagen_filtro_profe_path = resource_path("imagenes/filtro_profe.png")
        imagen_volver_path = resource_path("imagenes/volver.png")


        self.imagen_filtro_curso = ImageTk.PhotoImage(Image.open(imagen_filtro_curso_path).resize((20, 20)))
        self.imagen_filtro_dia = ImageTk.PhotoImage(Image.open(imagen_filtro_dia_path).resize((20, 20)))
        self.imagen_filtro_profe = ImageTk.PhotoImage(Image.open(imagen_filtro_profe_path).resize((20, 20)))
        self.imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))
        
        tk.Label(self.frame_fullscreen,text="Pestaña de filtros",bg="#c9daf8",font=("Monaco", 24, "bold")).place(relx = 0.5, rely = 0.1, anchor ='n')
        tk.Button(self.frame_fullscreen, text="Volver",image=self.imagen_volver,compound="left",height=30,width=200,borderwidth=1,relief="solid",command=lambda: self.volver_al_menu(menuFunc,tipoCuenta,nombreCuenta)).place(relx = 0.5, rely = 0.8, anchor ='n')
        tk.Button(self.frame_fullscreen, text="Filtrar por curso",image=self.imagen_filtro_curso,borderwidth=1,relief="solid",compound="left",height=30 , width=400, command=self.curso_botones_filtro).place(relx = 0.5, rely = 0.3, anchor ='n')
        tk.Button(self.frame_fullscreen, text="Filtrar por profesor", image=self.imagen_filtro_profe,borderwidth=1,relief="solid",compound="left",height=30 , width=400,command=self.filtro_profesor).place(relx = 0.5, rely = 0.5, anchor ='n')
        tk.Button(self.frame_fullscreen, text="Filtrar por día",image=self.imagen_filtro_dia,borderwidth=1,relief="solid",compound="left",height=30 , width=400, command=self.filtro_dia).place(relx = 0.5, rely = 0.7, anchor ='n')
        BG2color = "#6D9EEB"
        BG2 = tk.Frame(self.ventana5, bg=BG2color, width=512, height=32)
        BG2.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)
        etiqueta_derecha = tk.Label(BG2, text="©5to1ra & 5to3ra - 2023", bg=BG2color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')
    def eliminar(self):
        for elemento in self.ventana5.winfo_children():
            elemento.destroy()
    def volver_al_menu(self,menuFunc,tipoCuenta,nombreCuenta):
        self.eliminar()
        menuFunc(tipoCuenta,nombreCuenta)
    def curso_botones_filtro(self):
        def resource_path(relative_path):
          try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
           base_path = sys._MEIPASS
          except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
            base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
          return os.path.join(base_path, relative_path)
        self.ventana6 = tk.Toplevel()
        self.ventana6.title("Pantalla Principal")
        path = resource_path("Imagenes/Colegio_logo.ico")
        self.ventana6.iconbitmap(path)
        tk.Button(self.ventana6, text="Ciclo basico",borderwidth=1,relief="solid", command=lambda: self.filtro_curso(0)).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(self.ventana6, text="Ciclo superior",borderwidth=1,relief="solid", command=lambda: self.filtro_curso(1)).grid(row=2, column=0, padx=2, pady=2)
    def filtro_curso(self,ciclo):
        if ciclo==0:
            self.ventana6.destroy()
            self.eliminar()
            ventana_horario2= Pestaña_filtro(self.ventana5,self.menuFunc,self.tipoCuenta,self.nombreCuenta)
            ventana_horario2.widgets()
            ventana_horario2.agregar_ciclo_basico()
            ventana_horario2.treeview_filter()
            ventana_horario2.ejecutar()
        elif ciclo==1:
            self.ventana6.destroy()
            self.eliminar()
            ventana_horario2= Pestaña_filtro(self.ventana5,self.menuFunc,self.tipoCuenta,self.nombreCuenta)
            ventana_horario2.widgets()
            ventana_horario2.agregar_ciclo_superior()
            ventana_horario2.treeview_filter()
            ventana_horario2.ejecutar()
    def filtro_profesor(self):
        self.eliminar()
        ventana_horario4= Pestaña_filtro(self.ventana5,self.menuFunc,self.tipoCuenta,self.nombreCuenta)
        ventana_horario4.widgets()
        ventana_horario4.agregar_profesor()
        ventana_horario4.treeview_filter()
        ventana_horario4.ejecutar()
    def filtro_dia(self):
        self.eliminar()
        ventana_horario3= Pestaña_filtro(self.ventana5,self.menuFunc,self.tipoCuenta,self.nombreCuenta)
        ventana_horario3.widgets()
        ventana_horario3.agregar_dia()
        ventana_horario3.treeview_filter()
        ventana_horario3.ejecutar()
        
    
class Pestaña_filtro():
    
    def __init__(self,ventana_filtro,menuFunc,tipoCuenta,nombreCuenta):
        self.menuFunc=menuFunc
        self.tipoCuenta=tipoCuenta
        self.nombreCuenta=nombreCuenta
        self.ventana_filtro=ventana_filtro
        self.ventana_filtro.title("Filtro")
        self.ventana_filtro.geometry("900x500")
        self.frame_fullscreen = ttk.Frame(self.ventana_filtro)
        self.frame_fullscreen.place(x=0, y=0, relwidth=1, relheight=1)
        self.query=""
        self.techer = None
        self.label_dia = None
        self.año = None
        self.division = None
        self.dia = None
        self.configuracion_widgets()
    
    def eliminar(self):
        for elemento in self.ventana_filtro.winfo_children():
            elemento.destroy()
    def configuracion_widgets(self):
        """
        Configurar los widgets para la interfaz de usuario.
       Esta función configura varios widgets `ttk.LabelFrame` y configura sus posiciones de cuadrícula en la ventana rootmodification.
       También configura el peso de las columnas y filas en los widgets rootmodification y frame_superior.
       Finalmente, llama a la función `widgets` para insertar los widgets.
       """
        self.frame_superior=ttk.LabelFrame(self.frame_fullscreen)
        self.frame_inferior=ttk.LabelFrame(self.frame_fullscreen)
        self.frame_derecha=ttk.LabelFrame(self.frame_superior)
        self.frame_izquierda=ttk.LabelFrame(self.frame_superior)
        
        
        self.frame_superior.grid(row=0, column=0, sticky="nsew")
        self.frame_inferior.grid(row=1, column=0,sticky="nsew")
        self.frame_derecha.grid(row=0, column=1,sticky="nsew")
        self.frame_izquierda.grid(row=0, column=0,sticky="nsew")
        self.frame_fullscreen.columnconfigure(0, weight=1)
        self.frame_fullscreen.rowconfigure(0, weight=1)
        self.frame_fullscreen.rowconfigure(1, weight=6)
        
        self.frame_superior.columnconfigure(0, weight=10)
        self.frame_superior.columnconfigure(1, weight=2)
        self.frame_superior.rowconfigure(0, weight=1)
        self.frame_derecha.columnconfigure(0, weight=1)
        self.frame_derecha.columnconfigure(1, weight=2)
        self.frame_derecha.rowconfigure(0, weight=1)
        self.frame_derecha.rowconfigure(1, weight=3)
        self.frame_derecha.rowconfigure(2, weight=1)
        self.frame_derecha.rowconfigure(3, weight=1)
    
    def widgets(self):
        def resource_path(relative_path):
          try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
           base_path = sys._MEIPASS
          except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
            base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
          return os.path.join(base_path, relative_path)
        self.variable_check = tk.StringVar()

        imagen_volver_path = resource_path("imagenes/volver.png")
        imagen_pdf_path = resource_path("imagenes/PDF.png")
        self.imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))
        self.imagen_pdf = ImageTk.PhotoImage(Image.open(imagen_pdf_path).resize((20,20)))
        self.variable_check.set("")
        style = ttk.Style()
        style.configure("Frame.TFrame", background="white")
        ttk.Label(self.frame_derecha, text="Filtros",anchor="w").grid(column=0, row=0,sticky="news")
        ttk.Button(self.frame_derecha,text="Volver",image=self.imagen_volver,compound="left",command=self.volver).grid(column=1, row=0, sticky="news",padx=(10,0))
        self.frame_variables=ttk.LabelFrame(self.frame_derecha)
        self.frame_variables.grid(column=0, row=1,columnspan=2,sticky="news")
        self.frame_variables.columnconfigure(0, weight=1)
        self.frame_variables.rowconfigure(0, weight=1)
        self.frame_variables.rowconfigure(1, weight=1)
        ttk.Button(self.frame_derecha,text="Exportar a PDF",image=self.imagen_pdf,compound="left",command=self.exportar_a_pdf).grid(column=0, row=3, sticky="news",columnspan=2)
    def agregar_ciclo_basico(self):
        ttk.Button(self.frame_derecha,text="Filtrar",command=self.filtrar_division).grid(column=0, row=2, sticky="news",columnspan=2)   
        ttk.Label(self.frame_izquierda, text="Curso").grid(column=0, row=0)
        ttk.Label(self.frame_izquierda, text="Division").grid(column=0, row=1)
        self.frame_izquierda.rowconfigure(0, weight=1)
        self.frame_izquierda.rowconfigure(1, weight=1)
        for x in range(0, 3):
            if x==0:
                ttk.Button(self.frame_izquierda, text=f"{x+1}°", command=lambda r=x+1: self.boton_agregar_año(r)).grid(column=x+1, row=0,columnspan=2, sticky="ew")
            else:
                ttk.Button(self.frame_izquierda, text=f"{x+1}°", command=lambda r=x+1: self.boton_agregar_año(r)).grid(column=1+x*2, row=0,columnspan=2, sticky="ew")
        divisiones = ["A", "B", "C", "D", "E", "F"]
        for x in range(7):
            self.frame_izquierda.columnconfigure(x, weight=1)
        for x, division in enumerate(divisiones):
            ttk.Button(self.frame_izquierda, text=f"{division}",command=lambda y=division: self.boton_agregar_division(y)).grid(column=x+1, row=1, sticky="ew")
    def volver(self):
        self.eliminar()
        menu_filtros(self.ventana_filtro,self.menuFunc,self.tipoCuenta,self.nombreCuenta)

    def agregar_ciclo_superior(self):
        ttk.Button(self.frame_derecha,text="Filtrar",command=self.filtrar_division).grid(column=0, row=2, sticky="news",columnspan=2)
        ttk.Label(self.frame_izquierda, text="Curso").grid(column=0, row=0)
        ttk.Label(self.frame_izquierda, text="Division").grid(column=0, row=1)
        self.frame_izquierda.rowconfigure(0, weight=1)
        self.frame_izquierda.rowconfigure(1, weight=1)
        for x in range(4, 8):
            self.frame_izquierda.columnconfigure(x-1, weight=1)
            if x == 8:
                ttk.Button(self.frame_izquierda, text=f"{x}°", command=lambda r=x: self.boton_agregar_año(r)).grid(column=6, row=0,columnspan=2,sticky="ew")
            else:
                ttk.Button(self.frame_izquierda, text=f"{x}°", command=lambda r=x: self.boton_agregar_año(r)).grid(column=int(2*(x-3.5)), row=0,columnspan=2,sticky="ew")
            
        for x in range(0,6):
            self.frame_izquierda.columnconfigure(x, weight=1)
            ttk.Button(self.frame_izquierda, text=f"{x+1}°", command=lambda r=x+1: self.boton_agregar_division(r)).grid(column=x+1, row=1,sticky="ew")
    def agregar_dia(self):
        ttk.Button(self.frame_derecha,text="Filtrar",command=self.filtrar_dia).grid(column=0, row=2, sticky="news",columnspan=2)
        numero_a_dia = {
                1: "Lunes",
                2: "Martes",
                3: "Miércoles",
                4: "Jueves",
                5: "Viernes"
        }
        ttk.Label(self.frame_izquierda, text="Dia de la semana").grid(column=0, row=0)
        for x in range(0,5):
            self.frame_izquierda.columnconfigure(x, weight=1)
            ttk.Button(self.frame_izquierda, text=f"{numero_a_dia[x+1]}°", command=lambda r=numero_a_dia[x+1]: self.boton_agregar_dia(r)).grid(column=x+1, row=0,sticky="ew")
    def filtrar_dia(self):
        try:
            self.conectar_a_mysql()
            self.my_treeview.delete(*self.my_treeview.get_children())
            dia_a_numero = {
            "Lunes": 1,
            "Martes": 2,
            "Miércoles": 3,
            "Jueves": 4,
            "Viernes": 5
            }
            numero_a_dia = {
                1: "Lunes",
                2: "Martes",
                3: "Miércoles",
                4: "Jueves",
                5: "Viernes"
            }
            self.dia = dia_a_numero[self.dia]
            self.cursor.execute("SELECT * FROM horarios WHERE dia =%s", (self.dia,))
            resultados = self.cursor.fetchall()
            resultados = [list(row) for row in resultados]
            for i, elemento in enumerate(resultados):
                dia_numero = elemento[10]  # El día está en el índice 10 según tu código
                dia_nombre = numero_a_dia.get(dia_numero, "desconocido")
                resultados[i][10] = dia_nombre
            for x in resultados:
                self.my_treeview.insert(parent='', index='end', values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9],x[10]), tags=(x[1],))
            messagebox.showinfo("Información", "Filtro aplicado")
        except mysql.connector.Error as err:
            print("Error al conectar a MySQL: {}".format(err))
        finally:
            self.desconectar_de_mysql()
    def boton_agregar_dia(self, dia):
        self.dia=dia
        if self.label_dia:
            self.label_dia.destroy()
        self.label_dia=ttk.Label(self.frame_variables, text=f"Dia: {self.dia}")
        self.label_dia.grid(column=0, row=0)
    def exportar_a_pdf(self):
        if self.año and self.division:
            query="""SELECT * FROM horarios WHERE Año={} AND Division="{}" """.format(self.año, self.division)
        elif self.techer:
            query="""SELECT * FROM horarios WHERE Profesor={}""".format(self.techer)
        elif self.dia:
            query="""SELECT * FROM horarios WHERE Dia={}""".format(self.dia)
        else:
            messagebox.showerror("Error", "Porfavor, seleccionar un filtro")
        pdf2=PDF_filtro("""{}""".format(query))
    def agregar_profesor(self):
        ttk.Button(self.frame_derecha,text="Filtrar",command=self.filtrar_profesor).grid(column=0, row=2, sticky="news",columnspan=2)
        self.frame_izquierda.columnconfigure(0, weight=1)
        self.frame_izquierda.rowconfigure(0, weight=1)
        self.frame_izquierda.rowconfigure(1, weight=1)
        self.conectar_a_mysql()
        self.cursor.execute("SELECT nombre, apellido FROM profesores")
        self.profesor = self.cursor.fetchall()
        self.opciones_profesor = [""] + [f"{nombre} {apellido}" for nombre, apellido in self.profesor]
        self.desconectar_de_mysql()
        self.entry_profesor = AutocompleteEntry(self.opciones_profesor, self.frame_izquierda)
        self.entry_profesor.grid(row=1, column=0,sticky="ew")
        self.entry_profesor.bind('<FocusOut>', lambda event: self.validar_profesor(event, self.entry_profesor))
        ttk.Label(self.frame_izquierda, text="Profesor").grid(column=0, row=0)
        ttk.Button(self.frame_izquierda,text="Añadir",command=self.añadir_profesor).grid(column=0, row=2,columnspan=2)
        
    def añadir_profesor(self):
        if self.techer:
            self.techer.destroy()
        self.profesor_filtrar = self.entry_profesor.get()
        self.techer=ttk.Label(self.frame_variables, text=f"Profesor: {self.profesor_filtrar}")
        self.techer.grid(column=0, row=0)
    def validar_profesor(self, event, entry_widget):
        widget_con_enfoque = self.ventana_filtro.focus_get()
        # Verifica si el widget con enfoque es un Listbox
        if isinstance(widget_con_enfoque, tk.Listbox):
            return
        entrada = entry_widget.get()
        if not entrada in self.opciones_profesor:
            messagebox.showerror("Error", "El profesor no existe")
            entry_widget.delete(0, tk.END)
    def filtrar_profesor(self):
        try:
            self.conectar_a_mysql()
            self.my_treeview.delete(*self.my_treeview.get_children())
            numero_a_dia = {
                1: "Lunes",
                2: "Martes",
                3: "Miércoles",
                4: "Jueves",
                5: "Viernes"
            }
            self.cursor.execute("SELECT * FROM horarios WHERE profesor =%s", (self.profesor_filtrar,))
            resultados = self.cursor.fetchall()
            resultados = [list(row) for row in resultados]
            for i, elemento in enumerate(resultados):
                dia_numero = elemento[10]  # El día está en el índice 10 según tu código
                dia_nombre = numero_a_dia.get(dia_numero, "desconocido")
                resultados[i][10] = dia_nombre
            for x in resultados:
                self.my_treeview.insert(parent='', index='end', values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9],x[10]), tags=(x[1],))
            messagebox.showinfo("Información", "Filtro aplicado")
            
        except Exception as e:
            messagebox.showerror("Error", "Error al filtrar, debe seleccionar un profesor")
            print(e)
            self.cnx.rollback()
        finally:
            self.desconectar_de_mysql()
    def treeview_filter(self):
        self.frame = self.frame_inferior
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")
        self.my_treeview = ttk.Treeview(self.frame,yscrollcommand=self.scrollbar.set, selectmode="extended")
        self.my_treeview.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.my_treeview.yview)
        self.my_treeview["columns"] = ("ID","Numero de aula","Tipo de aula","Horario llegada","Horario salida","Espacio Curricular","Año","Division","Grupo","Profesor","Dia")
        self.my_treeview.column("#0", width=0, stretch=0)
        self.my_treeview.column("ID", anchor="n", width=1)
        self.my_treeview.column("Numero de aula", anchor="center", width=20)
        self.my_treeview.column("Tipo de aula", anchor="center", width=30)
        self.my_treeview.column("Horario llegada", anchor="center", width=40)
        self.my_treeview.column("Horario salida", anchor="center", width=40)
        self.my_treeview.column("Espacio Curricular", anchor="center", width=40)
        self.my_treeview.column("Año", anchor="center", width=20)
        self.my_treeview.column("Division", anchor="center", width=20)
        self.my_treeview.column("Grupo", anchor="center", width=20)
        self.my_treeview.column("Profesor", anchor="center", width=20)
        self.my_treeview.column("Dia", anchor="center", width=20)

        self.my_treeview.heading("#0", text="", anchor="w")
        self.my_treeview.heading("Numero de aula", text="Numero de aula", anchor="center")
        self.my_treeview.heading("Tipo de aula", text="Tipo de aula", anchor="center")
        self.my_treeview.heading("Horario llegada", text="Horario llegada", anchor="center")
        self.my_treeview.heading("Horario salida", text="Horario salida", anchor="center")
        self.my_treeview.heading("Espacio Curricular", text="Espacio Curricular", anchor="center")
        self.my_treeview.heading("Año", text="Año", anchor="center")
        self.my_treeview.heading("Division", text="Division", anchor="center")
        self.my_treeview.heading("Grupo", text="Grupo", anchor="center")
        self.my_treeview.heading("Profesor", text="Profesor", anchor="center")
        self.my_treeview.heading("Dia", text="Dia", anchor="center")
    def boton_agregar_año(self, x):
        self.año = x
        ttk.Label(self.frame_variables, text=f"Año:     {self.año}").grid(sticky="w",column=0, row=0)

    def boton_agregar_division(self, y):
        self.division = y
        ttk.Label(self.frame_variables, text=f"Division:    {self.division}").grid(sticky="w",column=0, row=1)

    def filtrar_division(self):
        try:
            self.my_treeview.delete(*self.my_treeview.get_children())
            numero_a_dia = {
                1: "Lunes",
                2: "Martes",
                3: "Miércoles",
                4: "Jueves",
                5: "Viernes"
            }
            self.conectar_a_mysql()
            self.cursor.execute("SELECT * FROM horarios WHERE Año=%s AND Division=%s", (self.año, self.division))
            resultados = self.cursor.fetchall()
            resultados = [list(row) for row in resultados]
            for i, elemento in enumerate(resultados):
                dia_numero = elemento[10]  # El día está en el índice 10 según tu código
                dia_nombre = numero_a_dia.get(dia_numero, "desconocido")
                resultados[i][10] = dia_nombre
            for x in resultados:
                self.my_treeview.insert(parent='', index='end', values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9],x[10]), tags=(x[1],))
            messagebox.showinfo("Información", "Filtro aplicado")
        except AttributeError:
            messagebox.showerror("Error", "Debe seleccionar un curso y una división")
        finally:
            self.desconectar_de_mysql()
    def ejecutar(self):
        self.ventana_filtro.mainloop()
        
    def conectar_a_mysql(self):
        try:
                self.cnx = mysql.connector.connect(
                    host='eestn1.com.ar',
                    user='tecnica1',
                    password='z%51#q57A7BR',
                    database='tec_boletines2023',
                    port=3306
                )
                self.cursor = self.cnx.cursor()
        except Exception as e:
                print(e)
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                self.cnx.rollback()
                
    def desconectar_de_mysql(self):
        self.cursor.close()
        self.cnx.close()

if __name__ == "__main__":
    ventana_horario = tk.Tk()
    ventana_horario2= menu_filtros(ventana_horario)
    ventana_horario.mainloop()
