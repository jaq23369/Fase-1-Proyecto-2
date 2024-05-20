from flask import Flask, jsonify, request # type: ignore
from neo4j import GraphDatabase # type: ignore

app = Flask(__name__)

class HealthRecommendationSystem:
    def __init__(self, uri, user, password):
        self._conexion = GraphDatabase.driver(uri, auth=(user, password))
        

    def solicitarSexoUsuario(self):
        return request.args.get('sexo')

    def realizarEncuesta(self, sexo):
        datos_generales = self.preguntasGenerales()
        if sexo == 'Hombre':
            datos_especificos = self.preguntasEspecificasHombres()
        elif sexo == 'Mujer':
            datos_especificos = self.preguntasEspecificasMujeres()
        return {**datos_generales, **datos_especificos}

    def preguntasGenerales(self):
        datos = {}
        datos['edad'] = request.args.get('edad')
        datos['peso'] = request.args.get('peso')
        # Continuar con otras preguntas generales
        return datos

    def preguntasEspecificasHombres(self):
        datos = {}
        datos['nivel_actividad'] = request.args.get('nivel_actividad')
        # Continuar con otras preguntas específicas para hombres
        return datos

    def preguntasEspecificasMujeres(self):
        datos = {}
        datos['nivel_actividad'] = request.args.get('nivel_actividad')
        # Continuar con otras preguntas específicas para mujeres
        return datos

    def generarRecomendaciones(self, datos_usuario):
        with self._conexion.session() as sesion:
            # Aquí iría la lógica para consultar la base de datos y obtener las recomendaciones
            recomendaciones = "Recomendaciones basadas en tus respuestas y preferencias."
            return recomendaciones

    def close(self):
        self._conexion.close()

@app.route('/recomendaciones', methods=['GET'])
def obtener_recomendaciones():
    uri = "neo4j+s://b23ec4d0.databases.neo4j.io"  # URI de la base de datos Neo4j
    user = "neo4j"   # Usuario de la base de datos Neo4j
    password = "Z8ZBUBT-jKZe8k21Ys2ljyAgNVoMjJrUCaQVCckRxXY"      # Contraseña de la base de datos Neo4j

    sistema = HealthRecommendationSystem(uri, user, password)
    sexo = sistema.solicitarSexoUsuario()
    datos_usuario = sistema.realizarEncuesta(sexo)
    recomendaciones = sistema.generarRecomendaciones(datos_usuario)
    sistema.close()
    return jsonify({'recomendaciones': recomendaciones})

if __name__ == "__main__":
    app.run(debug=True)
# 