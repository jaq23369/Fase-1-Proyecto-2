from flask import Flask, jsonify, request
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError, ConfigurationError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS en tu aplicación Flask

class HealthRecommendationSystem:
    def __init__(self, uri, user, password):
        try:
            self._conexion = GraphDatabase.driver(uri, auth=(user, password))
        except (ServiceUnavailable, AuthError, ConfigurationError) as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise

    def close(self):
        self._conexion.close()

    def guardarUsuario(self, usuario, password):
        try:
            with self._conexion.session() as sesion:
                sesion.run("CREATE (u:Usuario {nombre: $nombre, password: $password})",
                           nombre=usuario, password=password)
        except Exception as e:
            print(f"Error al guardar usuario: {e}")
            raise

    def obtenerUsuario(self, nombre):
        try:
            with self._conexion.session() as sesion:
                resultado = sesion.run("MATCH (u:Usuario {nombre: $nombre}) RETURN u", nombre=nombre)
                usuario = resultado.single()
                return usuario["u"] if usuario else None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            raise

@app.route('/register', methods=['POST'])
def register():
    print("Solicitud de registro recibida")
    datos = request.json
    print(f"Datos recibidos: {datos}")
    nombre_usuario = datos.get('username')
    password = datos.get('password')

    uri = "neo4j+s://beb2a93f.databases.neo4j.io"
    user = "neo4j"
    password_db = "mcB_Lw8n3MWqQmrXxYtk-D3toXxXthYE8hnME-yOdQk"

    sistema = HealthRecommendationSystem(uri, user, password_db)
    sistema.guardarUsuario(nombre_usuario, password)
    sistema.close()
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

if __name__ == "__main__":
    app.run(port=5000)

