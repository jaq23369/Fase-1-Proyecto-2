class RegistroDatos {
    constructor() {
        this.registroForm = document.querySelector("#registroForm");
        this.init();
    }

    init() {
        this.registroForm.addEventListener("submit", this.handleRegistro.bind(this));
    }

    handleRegistro(event) {
        event.preventDefault(); // Evitar que el formulario se envíe

        // Capturar los valores del formulario de registro de datos
        const name = document.getElementById("name").value;
        const age = document.getElementById("age").value;
        const gender = document.getElementById("gender").value;
        const weight = document.getElementById("weight").value;
        const height = document.getElementById("height").value;
        const activityLevel = document.getElementById("activity-level").value;
        const fitnessGoal = document.getElementById("fitness-goal").value;
        const healthConditions = document.getElementById("health-conditions").value;

        // Mostrar los valores capturados en la consola (simulado)
        console.log("Nombre:", name);
        console.log("Edad:", age);
        console.log("Género:", gender);
        console.log("Peso:", weight);
        console.log("Altura:", height);
        console.log("Nivel de Actividad:", activityLevel);
        console.log("Objetivo Fitness:", fitnessGoal);
        console.log("Condiciones de Salud:", healthConditions);

        // Aquí iría el código para enviar los datos al servidor con Fetch API
        // Por ejemplo:
        this.sendDataToServer(name, age, gender, weight, height, activityLevel, fitnessGoal, healthConditions);
    }

    sendDataToServer(name, age, gender, weight, height, activityLevel, fitenessGoal, healthConditions) {
        // Enviar los datos al servidor utilizando Fetch API
        fetch('URL_DEL_ENDPOINT_PROPORCIONADO_POR_EL_BACKEND', { // Reemplaza 'URL_DEL_ENDPOINT_PROPORCIONADO_POR_EL_BACKEND' con la URL del endpoint proporcionado por el backend
            method: 'PUT', // Utilizando el método PUT
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(response => {
            if (response.ok) {
                console.log('Datos enviados exitosamente al servidor.');
                // Aquí podrías redirigir al usuario a otra página o realizar otras acciones después de guardar los datos
            } else {
                console.error('Error al enviar datos al servidor.');
                // Aquí podrías mostrar un mensaje de error al usuario si la solicitud falla
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
            // Aquí podrías mostrar un mensaje de error al usuario si hay un error de red
        });
    }
}

// Instanciar la clase RegistroDatos cuando se cargue el DOM
document.addEventListener("DOMContentLoaded", function() {
    new RegistroDatos();
});
