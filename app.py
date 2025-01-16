# Importar librerias nesesarias 
from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui' # Para usar Flask

# Cargar datos de estudiantes
def cargar_estudiantes():
    try: # Intentar abrir el archivo estudiantes.json
        with open('data/estudiantes.json', 'r') as f: # Abrir el archivo en modo lectura
            return json.load(f)
    except FileNotFoundError: # si el archivo no Existe retornar una lista vacia
        return []

# Guardar datos de estudiantes
def guardar_estudiantes(estudiantes):
    with open('data/estudiantes.json', 'w') as f: # abrir el archivo en modo de 'w' escritura
        json.dump(estudiantes, f, indent=4)

# Ruta inicial (para la pagina de inicio)
@app.route('/') # / para pagina de inicio de caulquier servidor 
def index():
    return render_template('index.html') # Renderizar la plantilla index.html

@app.route('/lista', methods=['GET', 'POST']) # Aceptar metodo Get (obtener datos del servidor) el metodo post (enviar datos al servidor)
def lista_estudiantes(): 
    estudiantes = cargar_estudiantes()
    # 'if' nos permite ejecutar un bloque de código si se cumple una determinada condición
    if request.method == 'POST': # si se envio un formulario
        nuevo_estudiante = { # crear un diccionario con los datos del nuevo estudiante
            'id': len(estudiantes) + 1,
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'presente': False
        }
        estudiantes.append(nuevo_estudiante) # Agregar al estudiante a la nueva lista de estudiantes 
        guardar_estudiantes(estudiantes) # Guarda la lista de estudiantes en el archivo estudiantes.json
    
    return render_template('lista.html', estudiantes=estudiantes) # Renderizar la plantilla lista.html con la lista de estudiantes

@app.route('/marcar_asistencia', methods=['POST']) # Acepta solo metodos post 
def marcar_asistencia():
    estudiante_id = int(request.form['id']) #'id' crea un identificador automatico (obtener el id del estudiante a marcar)
    estudiantes = cargar_estudiantes()
    
    for estudiante in estudiantes: 
        if estudiante['id'] == estudiante_id:
            estudiante['presente'] = not estudiante['presente'] # Cambiar el valor de la clave 'presente' del estudiante
            estudiante['hora_registro'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Agregarla hora y fecha del registro
    
    guardar_estudiantes(estudiantes)
    return jsonify(success=True) # Retornar un objeto json con la clave 'success y el valor true

@app.route('/registro_asistencia')
def registro_asistencia():
    estudiantes = cargar_estudiantes()
    presentes = [e for e in estudiantes if e.get('presente', False)]
    return render_template('registro.html', presentes=presentes)

if __name__ == '__main__': # si el script se ejecuta directamente 
    app.run(debug=True) # Iniciar la aplicación en modo debug