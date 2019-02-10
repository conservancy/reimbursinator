const password1 = document.getElementById("password1");
const password2 = document.getElementById("password2");

function validatePassword() {
    if (password1.value != password2.value) {
        password2.setCustomValidity("Passwords don't match");
    } else {
        password2.setCustomValidity('');
    }
}
password1.onchange = validatePassword;
password2.onkeyup = validatePassword;

function validateEmail(email) {
    if (email.validity.patternMismatch) {
        email.setCustomValidity('Please input correct email');
    } else {
        email.setCustomValidity('');
    }
}

function postToRegistrationEndpoint(event) {
    event.preventDefault();

    const credentials = {
        "email" : this.elements.email.value,
        "first_name" : this.elements.first_name.value,
        "last_name" : this.elements.last_name.value,
        "password1" : this.elements.password1.value,
        "password2" : this.elements.password2.value
    }
    const url = "https://" + window.location.hostname + ":8444/api/v1/account/register/";
    const xhr = new XMLHttpRequest();

    console.log("Attempting a connection to the following endpoint: " + url);
    console.log("User credentials:\n" + JSON.stringify(credentials));

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 201) {
                console.log("REGISTRATION SUCCESS!");
                console.log("Server response:\n" + this.response);
                token = JSON.parse(this.response).key;
                localStorage.setItem("token", token);
                window.location.replace("home.html");
            } else {
                console.error("REGISTRATION FAILURE!");
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
form.addEventListener("submit", postToRegistrationEndpoint);
