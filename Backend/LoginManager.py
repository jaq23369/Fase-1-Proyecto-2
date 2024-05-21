from flask import Flask, jsonify, request  # Importar módulos de Flask
from neo4j import GraphDatabase  # Importar driver de Neo4j
from neo4j.exceptions import ServiceUnavailable, AuthError, ConfigurationError  # Importar excepciones de Neo4j




# Inicializar aplicación Flask
app = Flask(__name__)

# Clase para el Sistema de Recomendaciones de Salud
class HealthRecommendationSystem:
    def __init__(self, uri, user, password):
        try:
            # Inicializar conexión con Neo4j
            self._conexion = GraphDatabase.driver(uri, auth=(user, password))
        except (ServiceUnavailable, AuthError, ConfigurationError) as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise

    def guardarInicioSesion(self, usuario):
        try:
            # Guardar el inicio de sesión en la base de datos
            with self._conexion.session() as sesion:
                sesion.run("MERGE (u:Usuario {nombre: $nombre}) "
                           "MERGE (l:InicioSesion {fecha: timestamp()}) "
                           "MERGE (u)-[:INICIO_SESION]->(l)", nombre=usuario)
        except Exception as e:
            print(f"Error al guardar inicio de sesión: {e}")
            raise

    def obtenerUsuario(self, nombre):
        try:
            # Obtener los detalles de un usuario
            with self._conexion.session() as sesion:
                resultado = sesion.run("MATCH (u:Usuario {nombre: $nombre}) RETURN u", nombre=nombre)
                usuario = resultado.single()
                return usuario["u"] if usuario else None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            raise

    def actualizarUsuario(self, nombre, nuevos_datos):
        try:
            # Actualizar la información del usuario
            with self._conexion.session() as sesion:
                sesion.run("MATCH (u:Usuario {nombre: $nombre}) SET u += $nuevos_datos", nombre=nombre, nuevos_datos=nuevos_datos)
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            raise

    def eliminarUsuario(self, nombre):
        try:
            # Eliminar un usuario
            with self._conexion.session() as sesion:
                sesion.run("MATCH (u:Usuario {nombre: $nombre}) DETACH DELETE u", nombre=nombre)
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            raise

    def crearUsuario(self, datos):
        try:
            # Crear un nuevo usuario
            with self._conexion.session() as sesion:
                sesion.run("CREATE (u:Usuario $datos)", datos=datos)
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise

    def close(self):
        try:
            # Cerrar conexión con Neo4j
            self._conexion.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
            raise

@app.route('/register', methods=['POST'])
def register():
    usuario_data = request.json
    nombre = usuario_data.get('username')

    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"
    user = "neo4j"
    password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"
    sistema = HealthRecommendationSystem(uri, user, password)
    sistema.crearUsuario(nombre, usuario_data)
    sistema.close()

    return jsonify({'message': 'Usuario registrado exitosamente'})





@app.route('/login', methods=['POST'])
def login():
    nombre_usuario = request.form.get('username')  # Obtener el nombre de usuario del formulario
    password = request.form.get('password')  # Obtener la contraseña del formulario

    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"  # URI de la base de datos Neo4j
    user = "neo4j"  # Usuario de la base de datos Neo4j
    password_db = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"  # Contraseña de la base de datos Neo4j

    sistema = HealthRecommendationSystem(uri, user, password_db)
    usuario = sistema.obtenerUsuario(nombre_usuario)  # Buscar al usuario en la base de datos

    if usuario and usuario.get("password") == password:  # Verificar si el usuario y la contraseña coinciden
        sistema.guardarInicioSesion(nombre_usuario)  # Guardar inicio de sesión en la base de datos
        sistema.close()
        return jsonify({'message': 'Inicio de sesión guardado exitosamente'})
    else:
        sistema.close()
        return jsonify({'message': 'Nombre de usuario o contraseña incorrectos'}), 401




# Endpoint para obtener detalles de un usuario (GET)
@app.route('/login', methods=['GET'])
def obtener_usuario(nombre):
    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"
    user = "neo4j"
    password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"
    sistema = HealthRecommendationSystem(uri, user, password)
    usuario = sistema.obtenerUsuario(nombre)
    sistema.close()
    if usuario:
        return jsonify({'usuario': dict(usuario)})
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

# Endpoint para actualizar un usuario (PUT)
@app.route('/usuario/<nombre>', methods=['PUT'])
def actualizar_usuario(nombre):
    nuevos_datos = request.json
    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"
    user = "neo4j"
    password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"
    sistema = HealthRecommendationSystem(uri, user, password)
    sistema.actualizarUsuario(nombre, nuevos_datos)
    sistema.close()
    return jsonify({'message': 'Usuario actualizado exitosamente'})

# Endpoint para eliminar un usuario (DELETE)
@app.route('/usuario/<nombre>', methods=['DELETE'])
def eliminar_usuario(nombre):
    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"
    user = "neo4j"
    password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"
    sistema = HealthRecommendationSystem(uri, user, password)
    sistema.eliminarUsuario(nombre)
    sistema.close()
    return jsonify({'message': 'Usuario eliminado exitosamente'})

# Ejecutar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
