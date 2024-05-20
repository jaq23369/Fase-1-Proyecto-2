from flask import Flask, jsonify, request # type: ignore
from neo4j import GraphDatabase # type: ignore

app = Flask(__name__)

class HealthRecommendationSystem:
    def __init__(self, uri, user, password):
        self._conexion = GraphDatabase.driver(uri, auth=(user, password))

    def guardarInicioSesion(self, usuario):
        with self._conexion.session() as sesion:
            sesion.run("MERGE (u:Usuario {nombre: $nombre}) "
                       "MERGE (l:InicioSesion {fecha: timestamp()}) "
                       "MERGE (u)-[:INICIO_SESION]->(l)", nombre=usuario)

    def close(self):
        self._conexion.close()

def guardarInicioSesion(self, usuario):
    with self._conexion.session() as sesion:
        sesion.run("MERGE (u:Usuario {nombre: $nombre}) "
                   "MERGE (l:InicioSesion {fecha: timestamp()}) "
                   "MERGE (u)-[:INICIO_SESION]->(l)", nombre=usuario)
    print(f"Inicio de sesión guardado para el usuario: {usuario}")


@app.route('/login', methods=['POST'])
def login():
    # Obtener el nombre de usuario del formulario o datos JSON de la solicitud
    nombre_usuario = request.json.get('username')
    
    # Guardar el inicio de sesión en la base de datos Neo4j
    uri = "41b0db32.databases.neo4j.io:7687"  # URI de la base de datos Neo4j
    user = "DBMSRecomendaciones"                  # Usuario de la base de datos Neo4j
    password = "Proyecto23501"      # Contraseña de la base de datos Neo4j
    sistema = HealthRecommendationSystem(uri, user, password)
    sistema.guardarInicioSesion(nombre_usuario)
    sistema.close()

    return jsonify({'message': 'Inicio de sesión guardado exitosamente'})

if __name__ == "__main__":
    app.run(debug=True)
