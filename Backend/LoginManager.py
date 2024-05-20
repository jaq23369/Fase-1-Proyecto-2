from flask import Flask, jsonify, request  # Importar módulos de Flask
from neo4j import GraphDatabase  # Importar driver de Neo4j

# Inicializar aplicación Flask
app = Flask(__name__)

# Clase para el Sistema de Recomendaciones de Salud
class HealthRecommendationSystem:
    def __init__(self, uri, user, password):
        # Inicializar conexión con Neo4j
        self._conexion = GraphDatabase.driver(uri, auth=(user, password))

    def guardarInicioSesion(self, usuario):
        # Guardar el inicio de sesión en la base de datos
        with self._conexion.session() as sesion:
            sesion.run("MERGE (u:Usuario {nombre: $nombre}) "
                       "MERGE (l:InicioSesion {fecha: timestamp()}) "
                       "MERGE (u)-[:INICIO_SESION]->(l)", nombre=usuario)

    def obtenerUsuario(self, nombre):
        # Obtener los detalles de un usuario
        with self._conexion.session() as sesion:
            resultado = sesion.run("MATCH (u:Usuario {nombre: $nombre}) RETURN u", nombre=nombre)
            usuario = resultado.single()
            return usuario["u"] if usuario else None

    def actualizarUsuario(self, nombre, nuevos_datos):
        # Actualizar la información del usuario
        with self._conexion.session() as sesion:
            sesion.run("MATCH (u:Usuario {nombre: $nombre}) SET u += $nuevos_datos", nombre=nombre, nuevos_datos=nuevos_datos)

    def eliminarUsuario(self, nombre):
        # Eliminar un usuario
        with self._conexion.session() as sesion:
            sesion.run("MATCH (u:Usuario {nombre: $nombre}) DETACH DELETE u", nombre=nombre)

    def close(self):
        # Cerrar conexión con Neo4j
        self._conexion.close()

# Endpoint para manejar inicios de sesión (POST)
@app.route('/login', methods=['POST'])
def login():
    nombre_usuario = request.json.get('username')
    
    # Guardar el inicio de sesión en la base de datos Neo4j
    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"  # URI de la base de datos Neo4j
    user = "neo4j"  # Usuario de la base de datos Neo4j
    password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"  # Contraseña de la base de datos Neo4j
    sistema = HealthRecommendationSystem(uri, user, password)
    sistema.guardarInicioSesion(nombre_usuario)
    sistema.close()

    return jsonify({'message': 'Inicio de sesión guardado exitosamente'})

# Endpoint para obtener detalles de un usuario (GET)
@app.route('/usuario/<nombre>', methods=['GET'])
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

