class Login {
    constructor() {
        this.loginForm = document.getElementById("loginForm");
        this.init();
    }

    init() {
        this.loginForm.addEventListener("submit", this.handleLogin.bind(this));
    }

    handleLogin(event) {
        event.preventDefault(); // Evitar que el formulario se envíe

        // Capturar los valores del formulario
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Guardar los valores en variables (simulado)
        const usuarioGuardado = username;
        const contraseñaGuardada = password;

        // Mostrar los valores guardados (simulado)
        console.log("Usuario guardado:", usuarioGuardado);
        console.log("Contraseña guardada:", contraseñaGuardada);

        // Aquí iría el código para enviar los datos al servidor con Fetch API
        // Por ejemplo:
        this.sendDataToServer(usuarioGuardado, contraseñaGuardada);
    }

    sendDataToServer(username, password) {
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

// Instanciar la clase LoginHandler cuando se cargue el DOM
document.addEventListener("DOMContentLoaded", function() {
    new Login();
});
