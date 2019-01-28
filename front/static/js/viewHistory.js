// Hack to change endpoint url for each OS
function getEndpointDomain() {
    let OSName;
    let domain;

    if (navigator.appVersion.indexOf("Win") !== -1)
        OSName = "Windows";
    else if (navigator.appVersion.indexOf("Mac") !== -1)
        OSName = "MacOS";
    else if (navigator.appVersion.indexOf("X11") !== -1)
        OSName = "UNIX";
    else if (navigator.appVersion.indexOf("Linux") !== -1)
        OSName = "Linux";
    else
        OSName = "Unknown OS";

    console.log(`Detected operating system: ${OSName}`);

    if (OSName === "Windows") {
        domain = "https://192.168.99.100:8444/";
    } else {
        domain = "https://localhost:8444/"
    }

    return domain;
}

function displayListOfReports(listOfReports) {
    const cardBody = document.querySelector(".card-body");
    const table = document.createElement("table");
    const reports = listOfReports.reports;
    let rowsInserted = 0;

    for (let i = 0; i < reports.length; i++) {
            let title = reports[i].title;
            let dateCreated = new Date(reports[i].date_created).toLocaleDateString("en-US");
            let state = reports[i].state;
            let dateSubmitted = (state === "created") ? "TBD": new Date(reports[i].date_submitted).toLocaleDateString("en-US");
            let bodyRow = table.insertRow(i); 
            
            bodyRow.insertCell(0).innerHTML = title;
            bodyRow.insertCell(1).innerHTML = dateCreated; 
            bodyRow.insertCell(2).innerHTML = state;
            bodyRow.insertCell(3).innerHTML = dateSubmitted;
            rowsInserted++;
    }

    if (rowsInserted === 0) {
        // Empty report list
        const p = document.createElement("p");
        p.innerHTML = "No reports found.";
        cardBody.appendChild(p);
    } else {
        // Create table header, add to table, and append result to the card body
        const thead = document.createElement("thead");
        const tr = document.createElement("tr");

        const headTitle = document.createElement("th");
        headTitle.innerHTML = "Title";
        tr.appendChild(headTitle);

        const headDateCreated = document.createElement("th");
        headDateCreated.innerHTML = "Date Created";
        tr.appendChild(headDateCreated);

        const headState = document.createElement("th");
        headState.innerHTML = "State";
        tr.appendChild(headState);

        const headDateSubmitted = document.createElement("th")
        headDateSubmitted.innerHTML = "Date Submitted";
        tr.appendChild(headDateSubmitted);

        thead.appendChild(tr);
        table.prepend(thead);
        table.classList.add("table", "table-striped", "table-responsive-sm");
        cardBody.appendChild(table);
    }
}

function getReportHistory(event) {
    const token = localStorage.getItem("token");
    const url = getEndpointDomain() + "backend/list_report";
    const xhr = new XMLHttpRequest();

    console.log(`Attempting a connection to the following endpoint: ${url}`);

    xhr.open("GET", url, true);
    //xhr.setRequestHeader("Authorization", `Token  ${token}`);
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("GET list_report SUCCESS!");
                console.log(`Server response:\n${this.response}`);
                listOfReports = JSON.parse(this.response);
                displayListOfReports(listOfReports);
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

document.addEventListener("DOMContentLoaded", getReportHistory);
