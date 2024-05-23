from flask import Flask, jsonify, request, redirect, url_for
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError, ConfigurationError

app = Flask(__name__)

    def guardarInicioSesion(self, usuario):
        try:
            with self._conexion.session() as sesion:
                sesion.run("MERGE (u:Usuario {nombre: $nombre}) "
                           "MERGE (l:InicioSesion {fecha: timestamp()}) "
                           "MERGE (u)-[:INICIO_SESION]->(l)", nombre=usuario)
                # Guarda el inicio de sesión del usuario en la base de datos.
        except Exception as e:
            print(f"Error al guardar inicio de sesión: {e}")
            raise

    def obtenerUsuario(self, nombre):
        try:
            with self._conexion.session() as sesion:
                resultado = sesion.run("MATCH (u:Usuario {nombre: $nombre}) RETURN u", nombre=nombre)
                return usuario["u"] if usuario else None
                # Obtiene los datos del usuario desde la base de datos.
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            raise

    def actualizarUsuario(self, nombre, nuevos_datos):
        try:
            with self._conexion.session() as sesion:
                sesion.run("MATCH (u:Usuario {nombre: $nombre}) SET u += $nuevos_datos", nombre=nombre, nuevos_datos=nuevos_datos)
                # Actualiza los datos del usuario en la base de datos.
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            raise

    def eliminarUsuario(self, nombre):
        try:
            with self._conexion.session() as sesion:
                sesion.run("MATCH (u:Usuario {nombre: $nombre}) DETACH DELETE u", nombre=nombre)
                # Elimina el usuario de la base de datos.
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            raise

    def crearUsuario(self, datos):
        try:
            with self._conexion.session() as sesion:
                sesion.run("CREATE (u:Usuario $datos)", datos=datos)
                # Crea un nuevo usuario en la base de datos.
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise

    def close(self):
        try:
            self._conexion.close()
            # Cierra la conexión con la base de datos.
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
            raise


@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        uri = "neo4j+s://b23ec4d0.databases.neo4j.io"
        user = "neo4j"
        password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"
        sistema = HealthRecommendationSystem(uri, user, password)
        sistema.close()
        return jsonify({'message': 'Conexión exitosa a Neo4j'}), 200
        # Endpoint para probar la conexión con la base de datos.
    except Exception as e:
        return jsonify({'message': f'Error al conectar a Neo4j: {e}'}), 500


@app.route('/register', methods=['POST'])
def register():
    usuario_data = request.json
    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"
    user = "neo4j"
    password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"
    sistema = HealthRecommendationSystem(uri, user, password)
    sistema.crearUsuario(usuario_data)
    sistema.close()
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    # Endpoint para registrar un nuevo usuario.

@app.route('/login', methods=['POST'])
def login():
    nombre_usuario = request.json.get('username')
    password = request.json.get('password')

    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"
    user = "neo4j"
    password_db = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"

    sistema = HealthRecommendationSystem(uri, user, password_db)
    usuario = sistema.obtenerUsuario(nombre_usuario)

    if usuario and usuario.get("password") == password:
        sistema.guardarInicioSesion(nombre_usuario)
        sistema.close()
        return jsonify({'message': 'Inicio de sesión exitoso', 'redirect': 'recomendaciones.html'}
        # Verifica el inicio de sesión del usuario y guarda el registro del inicio de sesión.
    else:
        sistema.close()
        return jsonify({'message': 'Nombre de usuario o contraseña incorrectos'}), 401
        # Responde con un error si las credenciales son incorrectas.

if __name__ == "__main__":
    app.run(debug=True)
    # Ejecuta la aplicación Flask en modo de depuración.

