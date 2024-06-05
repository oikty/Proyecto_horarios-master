from fpdf import FPDF
import mysql.connector
import os
from win10toast import ToastNotifier
from tkinter import Tk, filedialog
#import datetime

#Hecho por Valentino signorello
class PDF(FPDF):
    def __init__(self, tipo_de_aula, numero_de_aula):
        super().__init__(orientation='L', unit='mm', format='A3')
        self.tipo_de_aula = tipo_de_aula
        self.numero_de_aula = numero_de_aula
        self.add_page()
        self.tabla() 

       
    def header(self):
        url="https://eestn1tfeb.blogspot.com"
        self.set_font("Times", "B", 25)
        self.cell(395, 15, "Escuela Técnica N°1: Manuel Belgrano", border=1,align="C", ln=True,link=url)
        self.ln(5)

       
    def tabla(self):
        try:
            # Conexión a la base de datos
            self.cnx = mysql.connector.connect(
            host='eestn1.com.ar',
            user='tecnica1',
            password='z%51#q57A7BR',
            database='tec_boletines2023',
            port=3306
            )
            self.cursor = self.cnx.cursor()
            self.cursor.execute("""SELECT * FROM horarios WHERE Numero_aula=%s AND tipo_de_aula=%s ORDER BY Horario_e""",
                                (self.numero_de_aula, self.tipo_de_aula))
            self.VALORES = self.cursor.fetchall()

            self.dias_a_numeros = {"Lunes": 1, "Martes": 2, "Miercoles": 3, "Jueves": 4, "Viernes": 5}
            horarios_por_dia = {dia: [] for dia in self.dias_a_numeros.keys()}
            print(horarios_por_dia)
            for valor in self.VALORES:
                dia_numero = valor[10]
                dia_texto = list(self.dias_a_numeros.keys())[dia_numero - 1]
                horarios_por_dia[dia_texto].append(valor)

        except mysql.connector.Error as err:
            print("Error al conectarse a MySQL: {}".format(err))
            self.cursor.close()
            self.cnx.close()
            return

    
        # Encabezados
        self.set_fill_color(81, 112, 238)  
        self.cell(395,10, "Horarios", border=1,align='C',fill=1,ln=1)
        #cambiar fuente a la normal
        self.set_font("Arial", size=10)
        #y color
        self.set_fill_color(12, 171, 196)
        self.cell(30, 10, "Dia", border=1, align='C', fill=1)
        self.cell(35, 10, "Numero de aula", border=1, align='C', fill=1)
        self.cell(40, 10, "Tipo de aula", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario entrada", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario salida", border=1, align='C', fill=1)
        self.cell(85, 10, "Espacio curricular", border=1, align='C', fill=1)
        self.cell(15, 10, "Año", border=1, align='C', fill=1)
        self.cell(15, 10, "Division", border=1, align='C', fill=1)
        self.cell(15, 10, "Grupo", border=1, align='C', fill=1)
        self.cell(80, 10, "Profesor", border=1, align='C', fill=1)
        self.ln()

        self.set_fill_color(220, 220, 220)
        dia_antes=None
        fila_nueva=True
        self.c = 0 
       
        

        for dia, horarios in horarios_por_dia.items():
         if horarios:
            if dia == dia_antes:
                  self.cell(25,10, "",border=1,align='C',fill=0)

            else:
                fila_nueva=True
                self.cell(30,10 * len(horarios) ,str(dia),border=1,align='C',fill=0)
                dia_antes = dia

            
            
            for valor in horarios:
                
                if not fila_nueva:
                 self.cell(30, 10, "", border=0, align='C', fill=0)
                else:
                 fila_nueva = False  

                #hora_entrada = valor[3].strftime("%H:%M")
                #hora_salida = valor[4].strftime("%H:%M")
                #

                self.cell(35, 10, str(valor[1]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[2]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[3]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[4]), border=1, align='C', fill=1)
                self.cell(85, 10, str(valor[5]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[6]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[7]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[8]), border=1, align='C', fill=1)
                self.cell(80, 10, str(valor[9]), border=1, align='C', fill=1)
                self.ln()
                if self.c % 2 == 0:
                        self.set_fill_color(255, 255, 255)  
                else:
                        self.set_fill_color(220, 220, 220)  

                self.c += 1 
                 
    def guardar_pdf(self):
        nombre_archivo = f"Horario {self.tipo_de_aula} {self.numero_de_aula}.pdf"
        ruta_descargas = os.path.expanduser("~/Downloads")

        # Generar un nombre de archivo único si ya existe
        contador = 1
        ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
        while os.path.exists(ruta_pdf_descargas):
            nombre_archivo = f"Horario {self.tipo_de_aula} {self.numero_de_aula} ({contador}).pdf"
            ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
            contador += 1

        self.output(ruta_pdf_descargas)
        os.startfile(ruta_pdf_descargas)
        

class PDF_filtro(FPDF):
    def __init__(self, query):
        super()._init_(orientation='L', unit='mm', format='A3')
        self.query = query
        self.add_page()
        self.tabla()
    
    def header(self):
        url="https://eestn1tfeb.blogspot.com"
        self.set_font("Times", "B", 25)
        self.cell(285, 15, "Escuela Técnica N°1: Manuel Belgrano", border=1,align="C", ln=True,link=url)
        self.ln(5)
         
    def tabla(self):
        try:
            # Conexión a la base de datos
            self.cnx = mysql.connector.connect(
                host='eestn1.com.ar',
                user='tecnica1',
                password='z%51#q57A7BR',
                database='tec_boletines2023',
                port=3306
            )
            self.cursor = self.cnx.cursor()
            self.cursor.execute(self.query)
            self.VALORES = self.cursor.fetchall()

            self.dias_a_numeros = {"Lunes": 1, "Martes": 2, "Miercoles": 3, "Jueves": 4, "Viernes": 5}
            horarios_por_dia = {dia: [] for dia in self.dias_a_numeros.keys()}
            print(horarios_por_dia)
            for valor in self.VALORES:
                dia_numero = valor[10]
                dia_texto = list(self.dias_a_numeros.keys())[dia_numero - 1]
                horarios_por_dia[dia_texto].append(valor)

        except mysql.connector.Error as err:
            print("Error al conectarse a MySQL: {}".format(err))
            self.cursor.close()
            self.cnx.close()
            return

        # Encabezados
        self.set_fill_color(81, 112, 238)  
        self.cell(350,10, "Horarios", border=1,align='C',fill=1,ln=1)
        
        #cambiar fuente a la normal
        self.set_font("Arial", size=10)
        #y color
        self.set_fill_color(12, 171, 196)
        self.cell(20, 10, "Dia", border=1, align='C', fill=1)
        self.cell(25, 10, "Numero de aula", border=1, align='C', fill=1)
        self.cell(25, 10, "Tipo de aula", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario entrada", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario salida", border=1, align='C', fill=1)
        self.cell(40, 10, "Espacio curricular", border=1, align='C', fill=1)
        self.cell(15, 10, "Año", border=1, align='C', fill=1)
        self.cell(15, 10, "Division", border=1, align='C', fill=1)
        self.cell(15, 10, "Grupo", border=1, align='C', fill=1)
        self.cell(45, 10, "Profesor", border=1, align='C', fill=1)
        self.ln()

        self.set_fill_color(220, 220, 220)
        
        dia_antes=None
        fila_nueva=True
        self.c = 0 
       
        for dia, horarios in horarios_por_dia.items():
         if horarios:
            if dia == dia_antes:
                  self.cell(25,10, "",border=1,align='C',fill=0)

            else:
                fila_nueva=True
                self.cell(40,10 * len(horarios) ,str(dia),border=1,align='C',fill=0)
                dia_antes = dia

            
            
            for valor in horarios:
                if not fila_nueva:
                 self.cell(25, 10, "", border=0, align='C', fill=0)
                else:
                 fila_nueva = False  

                self.cell(25, 10, str(valor[1]), border=1, align='C', fill=1)
                self.cell(25, 10, str(valor[2]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[3]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[4]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[5]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[6]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[7]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[8]), border=1, align='C', fill=1)
                self.cell(45, 10, str(valor[9]), border=1, align='C', fill=1)
                self.ln()
                if self.c % 2 == 0:
                        self.set_fill_color(255, 255, 255)  
                else:
                        self.set_fill_color(220, 220, 220)  

                self.c += 1  
                
    def guardar_pdf(self):
        nombre_archivo = f"Horario {self.tipo_de_aula} {self.numero_de_aula}.pdf"
        ruta_descargas = os.path.expanduser("~/Downloads")

        # Generar un nombre de archivo único si ya existe
        contador = 1
        ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
        while os.path.exists(ruta_pdf_descargas):
            nombre_archivo = f"Horario {self.tipo_de_aula} {self.numero_de_aula} ({contador}).pdf"
            ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
            contador += 1

        self.output(ruta_pdf_descargas)
        os.startfile(ruta_pdf_descargas)
    
        
        #notifiacion
        toast = ToastNotifier()
        mensaje_personalizado = "Esto puede tardar un momento"
        toast.show_toast("Generando PDF en segundo plano...",mensaje_personalizado, duration=10)

if __name__ == '__main__':
    app = PDF("Laboratorio", 10)
    app.guardar_pdf()