function displayErrorMessage(errorMessage) {
    const errorReport = document.querySelector("#errorReport");
    errorReport.innerHTML = JSON.parse(errorMessage).error;
}

function postToLoginEndpoint(event) {
    event.preventDefault();

    const credentials = {
        "username" : this.elements.username.value,
        "password" : this.elements.password.value
    }
    const url = "https://reqres.in/api/login" // mock api service
    const xhr = new XMLHttpRequest();

    console.log("User credentials:\n" + JSON.stringify(credentials)");

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("LOGIN SUCCESS!");
                console.log("Server response:\n" + this.response);
                token = JSON.parse(this.response).token;
                localStorage.setItem("token", token);
                window.location.replace("home.html");
            } else {
                console.error("LOGIN FAILURE!");
                console.error("Server status: " + this.status);
                console.error("Server response:\n" + this.response);
                displayErrorMessage(this.response);
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
