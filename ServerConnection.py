import pyodbc

conexion_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ACT_40000029135\\ESTADISTICAS;"  # Asegúrate de que este puerto esté habilitado
    "DATABASE=Estadistica;"
    "Trusted_Connection=yes;"
)


try:
    # Conectar a la base de datos
    conexion = pyodbc.connect(conexion_str)
    print("Conexión exitosa.")

    # Crear un cursor para ejecutar consultas
    cursor = conexion.cursor()

    # Ejemplo de una consulta
    cursor.execute("SELECT * FROM ClienteAccionComercial")  # Cambia 'tu_tabla' por el nombre real de tu tabla

    # Recuperar los resultados
    for fila in cursor.fetchall():
        print(fila)

except Exception as e:
    print("Error al conectar:", e)

finally:
    # Cerrar la conexión
    if 'conexion' in locals():
        conexion.close()