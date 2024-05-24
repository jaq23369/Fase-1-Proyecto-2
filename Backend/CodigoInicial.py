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
            print("Conexion exitosa")
        except (ServiceUnavailable, AuthError, ConfigurationError) as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise
    
    def close(self):
        self._conexion.close()

    def node_to_dict(self, node):
        return dict(node)

    def guardarUsuario(self, usuario, password):
        try:
            with self._conexion.session() as sesion:
                sesion.run("CREATE (u:Usuario {nombre: $nombre, password: $password})",
                        nombre=usuario, password=password)
                result = sesion.run("MATCH (u:Usuario {nombre: $nombre}) RETURN u, id(u) AS id",
                                    nombre=usuario)
                user_record = result.single()
                if user_record:
                    usuario_detalle = user_record["u"]
                    usuario_detalle = self.node_to_dict(usuario_detalle)  # Convert Node to dict
                    usuario_detalle['id'] = user_record['id']
                    print(f"Usuario creado: {usuario_detalle}")
                    return usuario_detalle
                else:
                    raise Exception("Usuario no encontrado después de la creación.")
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

    def actualizarUsuario(self, id, data):
        try:
            id = int(id)
            
            with self._conexion.session() as sesion:
                sesion.run("""
                    MATCH (u:Usuario)
                    WHERE id(u) = $user_id
                    SET u.nombre = $nombre,
                        u.edad = $edad,
                        u.genero = $genero,
                        u.peso = $peso,
                        u.altura = $altura,
                        u.nivel_actividad = $nivel_actividad,
                        u.objetivo_fitness = $objetivo_fitness,
                        u.condiciones_salud = $condiciones_salud
                    RETURN u
                """, user_id=id, **data)
                result = sesion.run("MATCH (u:Usuario) WHERE id(u) = $user_id RETURN u", user_id=id)
                user_record = result.single()
                
                if user_record:
                    usuario_detalle = user_record["u"]
                    usuario_detalle = self.node_to_dict(usuario_detalle)
                    print(f"Usuario actualizado: {usuario_detalle}")
                    return usuario_detalle
                else:
                    raise Exception("Usuario no encontrado después de la actualización.")
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
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
    usuario_detalle = sistema.guardarUsuario(nombre_usuario, password)
    sistema.close()
    return jsonify({'message': 'Usuario registrado exitosamente', 'user': usuario_detalle}), 201

@app.route('/updateuser', methods=['POST'])
def update_user():
    print("Solicitud de actualización recibida")
    datos = request.json
    print(f"Datos recibidos: {datos}")
    user_id = datos.get('id')
    update_data = {
        'nombre': datos.get('name'),
        'edad': datos.get('age'),
        'genero': datos.get('gender'),
        'peso': datos.get('weight'),
        'altura': datos.get('height'),
        'nivel_actividad': datos.get('activity-level'),
        'objetivo_fitness': datos.get('fitness-goal'),
        'condiciones_salud': datos.get('health-conditions')
    }
    print("DATA NASHE: ",update_data)
    uri = "neo4j+s://beb2a93f.databases.neo4j.io"
    user = "neo4j"
    password_db = "mcB_Lw8n3MWqQmrXxYtk-D3toXxXthYE8hnME-yOdQk"

    sistema = HealthRecommendationSystem(uri, user, password_db)
    try:
        usuario_detalle = sistema.actualizarUsuario(user_id, update_data)
        response = jsonify({'message': 'Usuario actualizado exitosamente', 'user': usuario_detalle}), 200
    except Exception as e:
        response = jsonify({'message': f'Error al actualizar usuario: {e}'}), 500
    sistema.close()
    return response

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Server is running!'}), 200

if __name__ == "__main__":
    app.run(port=5000)
