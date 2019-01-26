function displayListOfUnfinishedReports(listOfReports) {
    const unfinishedDiv = document.querySelector("#Unfinished");
    const unfinishedList = document.createDocumentFragment();

    // Remove any pre-existing children from the unfinishedDiv to avoid
    // duplicating elements each time the unfinished tab is clicked
    while (unfinishedDiv.firstChild) {
        unfinishedDiv.removeChild(unfinishedDiv.firstChild);
    }

    // Add unfinished report information to unfinishedList document fragment
    const reports = listOfReports.reports;
    for (let i = 0; i < reports.length; i++) {
        if (reports[i].hasOwnProperty("state")) {
            if (reports[i].state === "created") { // select unfinished reports
                let p = document.createElement("p");
                let date = new Date(reports[i].date_created).toDateString();
                p.innerHTML = `${reports[i].title}, ${date}`;
                unfinishedList.appendChild(p);
            }
        }
    }

    // Add message if none found
    if (unfinishedList.hasChildNodes() === false) {
        const p = document.createElement("p");
        p.innerHTML = "No unfinished reports found.";
        unfinishedList.appendChild(p);
    }

    // Append unfinishedList document fragment to unfinishedDiv
    unfinishedDiv.appendChild(unfinishedList);
}

function getListOfReports(event) {
    const token = localStorage.getItem("token");
    const url = "https://localhost:8444/backend/list_report"
    const xhr = new XMLHttpRequest();

    xhr.open("GET", url, true);
    xhr.setRequestHeader("Authorization", `Token  ${token}`);
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("GET list_report SUCCESS!");
                console.log(`Server response:\n${this.response}`);
                listOfReports = JSON.parse(this.response);
                displayListOfUnfinishedReports(listOfReports);
            } else {
                console.log("GET list_report FAILURE!");
                console.log(`Server status: ${this.status}`);
                console.log(`Server response:\n${this.response}`);
            }
        }
    };

    xhr.onerror = function() {
        alert("Connection error!");
    };

    xhr.send();
}

const unfinishedLink = document.querySelector("#unfinished-link");
unfinishedLink.addEventListener("click", getListOfReports);
