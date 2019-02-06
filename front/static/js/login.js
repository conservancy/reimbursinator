function postToLoginEndpoint(event) {
    event.preventDefault();

    const credentials = {
        "email" : this.elements.email.value,
        "password" : this.elements.password.value
    }
    const url = "https://" + window.location.hostname + ":8444/api/v1/account/login/";
    const xhr = new XMLHttpRequest();

    console.log("Attempting a connection to the following endpoint: " + url);
    console.log("User credentials:\n" + JSON.stringify(credentials));

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("LOGIN SUCCESS!");
                console.log("Server response:\n" + this.response);
                token = JSON.parse(this.response).key;
                localStorage.setItem("token", token);
                window.location.replace("home.html");
            } else {
                document.getElementById("errorLogin").innerHTML = "Incorrect user name or password";
                console.error("LOGIN FAILURE!");
                console.error("Server status: " + this.status);
                console.error("Server response:\n" + this.response);
            }
        }
    };

    xhr.onerror = function() {
        alert("Error connecting to the authentication server!");
    };

    xhr.send(JSON.stringify(credentials));
}

const form = document.querySelector("form");
form.addEventListener("submit", postToLoginEndpoint);
