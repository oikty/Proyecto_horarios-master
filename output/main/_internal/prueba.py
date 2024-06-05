import mysql.connector
cnx = mysql.connector.connect(
    host='eestn1.com.ar',
    user='tecnica1',
    password='z%51#q57A7BR',
    database='tec_boletines2023',
    port=3306
    )
# Crear un cursor para ejecutar consultas
cursor = cnx.cursor()
resultado=cursor.execute("SELECT * FROM profesores")
cursor.fetchall()
print(resultado)
cursor.close()
cnx.close()
