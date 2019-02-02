function postToLogoutEndpoint(event) {
    event.preventDefault();

    const token = localStorage.getItem("token");
    const url = "https://reqres.in/api/logout" // mock api service
    const xhr = new XMLHttpRequest();

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Authorization", "Token  " + token);
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("LOGOUT SUCCESS!");
                console.log("Server response:\n" + this.response);
                localStorage.removeItem("token");
                window.location.replace("index.html");
            } else {
                console.error("LOGOUT FAILURE!");
                console.error("Server status: " + this.status);
                console.error("Server response:\n" + this.response);
            }
        }
    };

    xhr.onerror = function() {
        alert("Error connecting to authentication server!");
    };

    xhr.send();
}

const logoutLink = document.querySelector(".log-out-link");
logoutLink.addEventListener("click", postToLogoutEndpoint);
