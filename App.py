from flask import Flask, request, render_template, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configura tu conexión a la base de datos
conexion_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ACT_40000029135\\ESTADISTICAS;"
    "DATABASE=Estadistica;"
    "Trusted_Connection=yes;"
)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# CRUD para AccionesComerciales
@app.route('/acciones', methods=['GET', 'POST'])
def acciones():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        
        with pyodbc.connect(conexion_str) as conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT MAX(CODAccionComercial) FROM AccionesComerciales")
                max_codigo = cursor.fetchone()[0]
                nuevo_codigo = max_codigo + 1 if max_codigo is not None else 1
                
                cursor.execute("INSERT INTO AccionesComerciales (CODAccionComercial, Descripcion) VALUES (?, ?)", (nuevo_codigo, descripcion))
                conexion.commit()
            except Exception as e:
                print(f"Error al insertar acción comercial: {e}")
                return redirect(url_for('acciones'))  # Redirigir en caso de error
        
        return redirect(url_for('acciones'))

    with pyodbc.connect(conexion_str) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM AccionesComerciales")
        acciones = cursor.fetchall()
    
    return render_template('acciones.html', acciones=acciones)

@app.route('/acciones/edit/<int:codaccion>', methods=['GET', 'POST'])
def edit_accion(codaccion):
    with pyodbc.connect(conexion_str) as conexion:
        cursor = conexion.cursor()
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            cursor.execute("UPDATE AccionesComerciales SET Descripcion = ? WHERE CODAccionComercial = ?", (descripcion, codaccion))
            conexion.commit()
            return redirect(url_for('acciones'))

        cursor.execute("SELECT * FROM AccionesComerciales WHERE CODAccionComercial = ?", (codaccion,))
        accion = cursor.fetchone()
    return render_template('edit_accion.html', accion=accion)

@app.route('/acciones/delete/<int:codaccion>', methods=['POST'])
def delete_accion(codaccion):
    with pyodbc.connect(conexion_str) as conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM AccionesComerciales WHERE CODAccionComercial = ?", (codaccion,))
        conexion.commit()
    return redirect(url_for('acciones'))

# CRUD para ClienteAccionComercial
@app.route('/clientes_accion', methods=['GET', 'POST'])
def clientes_accion():
    if request.method == 'POST':
        codcliente = request.form['codcliente']
        codaccion = request.form['codaccion']
        with pyodbc.connect(conexion_str) as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO ClienteAccionComercial (CODCLIENTE, CODAccionComercial) VALUES (?, ?)", (codcliente, codaccion))
            conexion.commit()
        return redirect(url_for('clientes_accion'))

    with pyodbc.connect(conexion_str) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ClienteAccionComercial")
        clientes_accion = cursor.fetchall()
    return render_template('clientes_accion.html', clientes_accion=clientes_accion)

@app.route('/clientes_accion/edit/<string:codcliente>', methods=['GET', 'POST'])
def edit_cliente_accion(codcliente):
    with pyodbc.connect(conexion_str) as conexion:
        cursor = conexion.cursor()
        if request.method == 'POST':
            nuevo_codcliente = request.form['codcliente']
            codaccion = request.form['codaccion']
            cursor.execute("UPDATE ClienteAccionComercial SET CODCLIENTE = ?, CODAccionComercial = ? WHERE CODCLIENTE = ?", (nuevo_codcliente, codaccion, codcliente))
            conexion.commit()
            return redirect(url_for('clientes_accion'))

        cursor.execute("SELECT * FROM ClienteAccionComercial WHERE CODCLIENTE = ?", (codcliente,))
        cliente_accion = cursor.fetchone()
    return render_template('edit_cliente_accion.html', cliente_accion=cliente_accion)

@app.route('/clientes_accion/delete/<string:codcliente>', methods=['POST'])
def delete_cliente_accion(codcliente):
    with pyodbc.connect(conexion_str) as conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ClienteAccionComercial WHERE CODCLIENTE = ?", (codcliente,))
        conexion.commit()
    return redirect(url_for('clientes_accion'))

if __name__ == '__main__':
    app.run(debug=True)