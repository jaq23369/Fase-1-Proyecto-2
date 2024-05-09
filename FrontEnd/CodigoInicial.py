from neo4j import GraphDatabase # type: ignore

class HealthRecommendationSystem:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def solicitarSexoUsuario(self):
        return input("Indique su sexo (Hombre/Mujer): ")

    def realizarEncuesta(self, sexo):
        datos = {}
        datos['edad'] = input("Ingrese su edad: ")
        datos['peso'] = input("Ingrese su peso: ")
        if sexo == 'Hombre':
            datos['nivel_actividad'] = input("Nivel de actividad física para hombres (bajo/medio/alto): ")
        elif sexo == 'Mujer':
            datos['nivel_actividad'] = input("Nivel de actividad física para mujeres (bajo/medio/alto): ")
        return datos

    def generarRecomendaciones(self, datos_usuario):
        with self.driver.session() as session:
            resultado = session.write_transaction(self._crear_y_obtener_recomendaciones, datos_usuario)
            print("Tus recomendaciones personalizadas son: ")
            for record in resultado:
                print(record["recomendacion"])

    @staticmethod
    def _crear_y_obtener_recomendaciones(tx, datos_usuario):
        query = (
            "CREATE (u:Usuario {edad: $edad, peso: $peso, nivel_actividad: $nivel_actividad}) "
            "RETURN u"
        )
        resultado = tx.run(query, datos_usuario)
        return resultado.single()

if __name__ == "__main__":
    uri = "neo4j://localhost:8080/v1/users"  # URL local que usaremos 
    user = "Users"                  # Usuarios
    password = "ProyectoA23501"           # Contraseña

    sistema = HealthRecommendationSystem(uri, user, password)
    sexo = sistema.solicitarSexoUsuario()
    datos_usuario = sistema.realizarEncuesta(sexo)
    sistema.generarRecomendaciones(datos_usuario)
    sistema.close()
