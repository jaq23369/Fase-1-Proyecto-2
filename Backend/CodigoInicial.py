from neo4j import GraphDatabase  # type: ignore


class HealthRecommendationSystem:
    def __init__(self, uri, user, password):
        self._conexion = GraphDatabase.driver(uri, auth=(user, password))

    def solicitarSexoUsuario(self):
        return input("Indique su sexo (Hombre/Mujer): ")

    def realizarEncuesta(self, sexo):
        datos_generales = self.preguntasGenerales()
        if sexo == 'Hombre':
            datos_especificos = self.preguntasEspecificasHombres()
        elif sexo == 'Mujer':
            datos_especificos = self.preguntasEspecificasMujeres()
        return {**datos_generales, **datos_especificos}

    def preguntasGenerales(self):
        datos = {}
        datos['edad'] = input("Ingrese su edad: ")
        datos['peso'] = input("Ingrese su peso: ")
        # Continuar con otras preguntas generales
        return datos

    def preguntasEspecificasHombres(self):
        datos = {}
        datos['nivel_actividad'] = input("Nivel de actividad física (bajo/medio/alto): ")
        # Continuar con otras preguntas específicas para hombres
        return datos

    def preguntasEspecificasMujeres(self):
        datos = {}
        datos['nivel_actividad'] = input("Nivel de actividad física (bajo/medio/alto): ")
        # Continuar con otras preguntas específicas para mujeres
        return datos

    def generarRecomendaciones(self, datos_usuario):
        with self._conexion.session() as sesion:
            # Aquí iría la lógica para consultar la base de datos y obtener las recomendaciones
            recomendaciones = "Recomendaciones basadas en tus respuestas y preferencias."
            print("Tus recomendaciones personalizadas son: ")
            print(recomendaciones)

    def close(self):
        self._conexion.close()

if __name__ == "__main__":
    uri = "bolt://localhost:7687"  # URI de la base de datos Neo4j
    user = "neo4j"                  # Usuario de la base de datos Neo4j
    password = "No me recuerdo de la contraseña jsjsjs"      # Contraseña de la base de datos Neo4j

    sistema = HealthRecommendationSystem(uri, user, password)
    sexo = sistema.solicitarSexoUsuario()
    datos_usuario = sistema.realizarEncuesta(sexo)
    sistema.generarRecomendaciones(datos_usuario)
    sistema.close()

