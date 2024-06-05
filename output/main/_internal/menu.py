#menu.py

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import Funcionalidad_parte_principal as FPP
from boletines import boletines1
import Pestaña_filtro as PF
import Aulas
from alumnos import alumnos1
from inasistencias import inasistencias1
from cuentas import cuentas1
import Profesores,os,sys


class menu1:
    
    def __init__(self,tk):
        self.boletines = boletines1(tk)
        self.alumnos = alumnos1(tk)
        self.inasistencias = inasistencias1(tk)
        self.cuentas = cuentas1(tk)
        tk.title("Menu")
    def resource_path(relative_path):
      try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
       base_path = sys._MEIPASS
      except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
       base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
      return os.path.join(base_path, relative_path)        
    def crear(self,tk,tipoCuenta,nombreCuenta,cerrarSesion,menuFunc):

        def eliminar():
            for elemento in tk.winfo_children():
                elemento.destroy()

        def administrar_boletines():
            eliminar()
            self.boletines.crear(tk,tipoCuenta,nombreCuenta,menuFunc)
            return
           #ejecutar modulo para administrar los boletines

        def administrar_asistencias():
            eliminar()
            self.inasistencias.crear(tk,tipoCuenta,nombreCuenta,menuFunc)
            return
            #ejecutar modulo para administrar las asistencias

        def administrar_alumnos():
            eliminar()
            def alumnosFunc(tk,tipoCuenta,nombreCuenta,menuFunc,alumnosFunc):
                self.alumnos.crear(tk,tipoCuenta,nombreCuenta,menuFunc,alumnosFunc)
            alumnosFunc(tk,tipoCuenta,nombreCuenta,menuFunc,alumnosFunc)
            return
            #ejecutar modulo del ingreso de alumnos
        def horarios(tk):
            eliminar()
            menu_horarios=FPP.menu_horarios()
            menu_horarios.horarios(tk,menuFunc,tipoCuenta,nombreCuenta)
        def administrar_cuentas():
            eliminar()
            def cuentasFunc(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc):
                self.cuentas.crear(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)
            cuentasFunc(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)
            return
        def administrar_materias(tk):
            eliminar()
            Profesores.botones_docentes(tk,menuFunc,tipoCuenta,nombreCuenta)

        def administrar_filtros(tk):
            eliminar()
            PF.menu_filtros(tk,menuFunc,tipoCuenta,nombreCuenta)

        def administrar_aulas(tk):
            eliminar()
            Aulas.botones_aulas(tk,menuFunc,tipoCuenta,nombreCuenta)

        def cerrar_sesion():
            eliminar()
            cerrarSesion()
            return
        
        BGcolor="#c9daf8"
        BG1color="#212121"
        BG2color="#6D9EEB"
        tk.configure(bg=BGcolor)

        tk.grid_columnconfigure(0, weight=1)
        
        BG2 = Frame(tk, bg=BG2color,width=512,height=32)
        #BG1 = Frame(tk, bg=BG1color,width=80,height=256)
        #BG1.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=0.1, relheight=1.0)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)
        imagen_administrar_boletin_path = menu1.resource_path("imagenes/administrar_boletin.png")
        self.imagen_administrar_boletin = ImageTk.PhotoImage(Image.open(imagen_administrar_boletin_path).resize((20, 20), Image.LANCZOS))

        imagen_administrar_horario_path = menu1.resource_path("imagenes/administrar_horario.png")
        self.imagen_administrar_horario = ImageTk.PhotoImage(Image.open(imagen_administrar_horario_path).resize((20, 20), Image.LANCZOS))

        imagen_administrar_asistencia_path = menu1.resource_path("imagenes/administrador_de_asistencia.png")
        self.imagen_administrar_asistencia = ImageTk.PhotoImage(Image.open(imagen_administrar_asistencia_path).resize((20, 20), Image.LANCZOS))

        imagen_administrar_alumnos_path = menu1.resource_path("imagenes/administrar_alumnos.png")
        self.imagen_administrar_alumnos = ImageTk.PhotoImage(Image.open(imagen_administrar_alumnos_path).resize((25, 25), Image.LANCZOS))

        imagen_administrar_cuentas_path = menu1.resource_path("imagenes/administrar_cuentas.png")
        self.imagen_administrar_cuentas = ImageTk.PhotoImage(Image.open(imagen_administrar_cuentas_path).resize((20, 20), Image.LANCZOS))

        imagen_materia_path = menu1.resource_path("imagenes/materia.png.jpg")
        self.imagen_materia = ImageTk.PhotoImage(Image.open(imagen_materia_path).resize((25, 25), Image.LANCZOS))

        imagen_cerrar_sesion_path = menu1.resource_path("imagenes/cerrar_sesion.png")
        self.imagen_cerrar_sesion = ImageTk.PhotoImage(Image.open(imagen_cerrar_sesion_path).resize((20, 20), Image.LANCZOS))

        imagen_aula_path = menu1.resource_path("imagenes/aulas.png")
        self.imagen_aula = ImageTk.PhotoImage(Image.open(imagen_aula_path).resize((20, 20), Image.LANCZOS))

        imagen_filtro_path = menu1.resource_path("imagenes/filtrar.png")
        self.imagen_filtro = ImageTk.PhotoImage(Image.open(imagen_filtro_path).resize((20, 20), Image.LANCZOS))

        gridposicion = Label(tk, text="", font=('Arial',0), bg=BGcolor)
        gridposicion.grid(row=10,column=1, columnspan=2, padx=9999, pady=(0, 0 ))

        fuente_grande = ('Arial', 30, "bold")
        etiqueta_bienvenida = Label(tk, text="¡Bienvenido, "+nombreCuenta+"!", font=fuente_grande, bg=BGcolor)
        etiqueta_bienvenida.grid(row=0,column=1, columnspan=2, padx=0, pady=(0, 0))

        fuente_chica = ('Arial', 15, "bold")
        etiqueta_bienvenida = Label(tk, text="¿Qué desea hacer hoy?", font=fuente_chica, bg=BGcolor)
        etiqueta_bienvenida.grid(row=1, column=1, columnspan=2,padx=0, pady=(0, 0), ipady=0)


        #Boton Boletines
        boton_boletines = Button(tk, text="Administrar boletines", image=self.imagen_administrar_boletin, compound="left", borderwidth=1, relief="solid", height=30 , width=300, command=administrar_boletines, font=("Helvetica", 16))
        boton_boletines.grid(row=2, column=1, padx=(0, 10), pady=(0, 0), sticky="E")

        #Boton Asistencias
        boton_asistencias = Button(tk, text="Administrar Asistencias",image=self.imagen_administrar_asistencia,compound="left",borderwidth=1,relief="solid",  height=30 , width=300, command=administrar_asistencias, font=("Helvetica", 16))
        boton_asistencias.grid(row=3, column=1, padx=(0, 10), pady=(0, 0), sticky="E")

        #Boton Alumnos
        boton_alumno = Button(tk, text="Administrar alumnos",image=self.imagen_administrar_alumnos,compound="left",borderwidth=1,relief="solid",  height=30 , width=300, command=administrar_alumnos, font=("Helvetica", 16))
        boton_alumno.grid(row=4, column=1, padx=(0, 10), pady=(0,0), sticky="E")

        #Boton Cuentas
        boton_cuentas = Button(tk, text="Cuentas",image=self.imagen_administrar_cuentas,compound="left",borderwidth=1,relief="solid",  height=30 , width=300, command=administrar_cuentas, font=("Helvetica", 16))
        boton_cuentas.grid(row=5, column=1, padx=(0, 10), pady=(0,0), sticky="E")

        #Boton Horarios
        boton_horarios = Button(tk, text="Horarios",image=self.imagen_administrar_horario,compound="left",borderwidth=1,relief="solid",  height=30 , width=300, command=lambda:horarios(tk), font=("Helvetica", 16))
        boton_horarios.grid(row=2, column=2, padx=(10, 0), pady=(0, 0), sticky="W")

        #Boton Materias
        boton_horarios = Button(tk, text="Materias y profesores",image=self.imagen_materia,compound="left",borderwidth=1,relief="solid",  height=30 , width=300, command=lambda:administrar_materias(tk), font=("Helvetica", 16))
        boton_horarios.grid(row=3, column=2, padx=(10, 0), pady=(0, 0), sticky="W")

        #Boton Filtros
        boton_horarios = Button(tk, text="Filtros",image=self.imagen_filtro,compound="left",borderwidth=1,relief="solid",  height=30 , width=300, command=lambda:administrar_filtros(tk), font=("Helvetica", 16))
        boton_horarios.grid(row=4, column=2, padx=(10, 0), pady=(0, 0), sticky="W")

        #Boton Aulas
        boton_horarios = Button(tk, text="Administrar Aulas",image=self.imagen_aula,compound="left",borderwidth=1,relief="solid",  height=30 , width=300, command=lambda:administrar_aulas(tk), font=("Helvetica", 16))
        boton_horarios.grid(row=5, column=2, padx=(10, 0), pady=(0, 0), sticky="W")



        if tipoCuenta == 1: #botones Maestro
            boton_boletines['state'] = NORMAL
            boton_horarios['state'] = NORMAL
            boton_asistencias['state'] = DISABLED
            boton_alumno['state'] = DISABLED
            boton_cuentas['state'] = DISABLED
        if tipoCuenta == 2: #botones Preceptor
            boton_boletines['state'] = NORMAL
            boton_horarios['state'] = NORMAL
            boton_asistencias['state'] = NORMAL
            boton_alumno['state'] = NORMAL
            boton_cuentas['state'] = DISABLED
        if tipoCuenta == 3: #botones Administrador
            boton_boletines['state'] = NORMAL
            boton_horarios['state'] = NORMAL
            boton_asistencias['state'] = NORMAL
            boton_alumno['state'] = NORMAL
            boton_cuentas['state'] = NORMAL

        boton_cerrar_sesion = Button(tk, text="Cerrar Sesión",image=self.imagen_cerrar_sesion,compound="left",borderwidth=1,relief="solid", width=150, height=30, command=cerrar_sesion, bg="light coral", font=("Helvetica", 12))
        boton_cerrar_sesion.place(relx = 0.995, rely = 0.92, anchor ='se')

        etiqueta_derecha = Label(BG2, text="©5to1ra & 5to3ra - 2023", bg=BG2color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        etiqueta_izquierda = Label(BG2, text="", bg=BG2color,font=("Helvetica", 16))
        etiqueta_izquierda.place(relx = 0.0, rely = 0.5, anchor ='w')

        if tipoCuenta==1:
            etiqueta_izquierda.config(text="Profesor")
        elif tipoCuenta==2:
            etiqueta_izquierda.config(text="Preceptor")
        elif tipoCuenta==3:
            etiqueta_izquierda.config(text="Administrador")

        #canvas.tag_raise(rectangulo)