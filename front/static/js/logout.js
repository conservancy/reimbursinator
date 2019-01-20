function postToLogoutEndpoint(event) {
    event.preventDefault();

    const token = localStorage.getItem("token");
    const url = "https://reqres.in/api/logout" // mock api service
    const xhr = new XMLHttpRequest();

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Authorization", `Token  ${token}`);
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("LOGOUT SUCCESS!");
                console.log(`Server response:\n${this.response}`);
                localStorage.removeItem("token");
                window.location.replace("index.html");
            } else {
                console.log("LOGOUT FAILURE!");
                console.log(`Server status: ${this.status}`);
                console.log(`Server response:\n${this.response}`);
            }
        }
    };

    xhr.onerror = function() {
        alert("Error connecting to authentication server!");
    };

    xhr.send();
}

const logoutLinks = document.querySelectorAll(".log-out-link");
logoutLinks[0].addEventListener("click", postToLogoutEndpoint);
logoutLinks[1].addEventListener("click", postToLogoutEndpoint);
